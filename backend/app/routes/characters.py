# 导入 Optional，用于类型注解中标记某些字段可能为 None
from typing import Optional

# 导入 FastAPI 路由工具：APIRouter 创建路由分组，Depends 实现依赖注入，HTTPException 抛出 HTTP 错误
from fastapi import APIRouter, Depends, HTTPException
# 导入 Pydantic 的数据模型基类，用于声明请求和响应的数据结构
from pydantic import BaseModel
# 导入 SQLAlchemy 的会话类型，用于数据库操作的类型注解
from sqlalchemy.orm import Session

# 导入数据库会话依赖，FastAPI 通过 Depends(get_db) 自动注入数据库会话
from app.database import get_db
# 导入 JWT 中间件中的用户 ID 获取函数，从令牌中解析出当前登录用户的 ID
from app.middleware.jwt import require_user_id
# 导入用户角色 ORM 模型，对应数据库中的 user_characters 表
from app.models import UserCharacter
# 导入角色模板引擎：list_templates 获取可用角色列表，get_template 获取单个角色模板详情
from app.characters.engine import list_templates, get_template

# 创建角色路由分组，所有端点自动添加 /api/characters 前缀，API 文档中归类到 "characters" 标签下
router = APIRouter(prefix="/api/characters", tags=["characters"])


class CharacterListView(BaseModel):
    """角色列表展示模型，用于返回角色模板的概要信息"""
    id: str                    # 角色模板的唯一标识 ID
    gender: str                # 角色性别：female（女性）或 male（男性）
    personality: str           # 角色性格，如"文静"、"治愈"、"傲娇"等
    name: str                  # 角色显示名称
    description: str           # 角色简短描述，用于在 UI 上展示
    traits: list[str]          # 角色性格特征列表，如 ["温柔", "善解人意", "内向"]


class ChooseRequest(BaseModel):
    """用户选择角色时的请求模型，需要指定性别和性格"""
    gender: str                # 想要的角色性别：female 或 male
    personality: str           # 想要的角色性格：如"治愈"、"文静"、"阳光"等


class CharacterInfo(BaseModel):
    """当前活跃角色的详细信息响应模型"""
    gender: str                # 角色性别
    personality: str           # 角色性格
    custom_name: Optional[str] # 用户给角色自定义的名称，未设置则为 None
    relationship_stage: int    # 关系阶段：0-5 的整数，数字越高关系越亲密
    intimacy_score: float      # 亲密度分数：0.0-1.0 的浮点数，数字越高越亲密


@router.get("/")
async def get_characters(gender: Optional[str] = None):
    """获取所有可选角色模板，支持按性别过滤"""
    # 调用模板引擎获取角色模板列表，如果不传 gender 则返回全部角色
    templates = list_templates(gender)
    # 将模板对象列表转换为 CharacterListView 响应模型列表，只返回前端需要的信息
    return [
        CharacterListView(
            id=t.id,                     # 模板唯一 ID
            gender=t.gender,             # 角色性别
            personality=t.personality,   # 角色性格
            name=t.name,                 # 角色名称
            description=t.description,   # 角色描述
            traits=t.traits,             # 性格特征列表
        )
        for t in templates              # 遍历所有匹配的角色模板
    ]


@router.post("/choose")
async def choose_character(
    req: ChooseRequest,                                    # 请求体：性别 + 性格
    user_id: int = Depends(require_user_id),               # 从 JWT 令牌中解析当前用户 ID
    db: Session = Depends(get_db),                         # 获取数据库会话
):
    """用户选择/切换角色，若已存在该性格的角色则激活它，否则新建"""
    # 校验性别参数是否合法，只允许 female 或 male 两种取值
    if req.gender not in ("female", "male"):
        raise HTTPException(status_code=400, detail="性别只能为 female 或 male")

    # Validate the personality exists
    templates = list_templates(req.gender)                   # 获取该性别下的所有可用模板
    valid_personalities = [t.personality for t in templates] # 提取所有合法的性格名称
    if req.personality not in valid_personalities:           # 如果请求的性格不在合法列表中
        raise HTTPException(status_code=400, detail=f"该性别下无此性格变体，可选：{valid_personalities}")

    # 将该用户的所有角色标记为非活跃，保证同一时间只有一个角色处于活跃状态
    db.query(UserCharacter).filter(UserCharacter.user_id == user_id).update({"is_active": False})

    # 查询用户是否已经创建过这个性别+性格的角色组合
    char = db.query(UserCharacter).filter(
        UserCharacter.user_id == user_id,      # 当前登录用户
        UserCharacter.gender == req.gender,    # 匹配请求的性别
        UserCharacter.personality == req.personality  # 匹配请求的性格
    ).first()                                  # 取第一个匹配结果（用户名+性别+性格唯一）

    if char:
        # 如果已存在该角色，只需将其重新激活（之前已经被全部设为 False，这里单独设为 True）
        char.is_active = True
        # 提交事务，将激活状态写入数据库
        db.commit()
        # 刷新对象，从数据库获取更新后的数据
        db.refresh(char)
        # 返回切换成功的消息，告知前端是"切换已有伴侣"而非"新建"
        return {"message": "已切换到现有伴侣", "character": char}

    # 如果用户还没有这个性格的角色，则创建一条全新的 UserCharacter 记录
    new_char = UserCharacter(
        user_id=user_id,              # 关联的当前用户 ID
        gender=req.gender,            # 选择的性别
        personality=req.personality,  # 选择的性格
        is_active=True                # 新创建的角色默认为活跃状态
    )
    # 将新角色对象添加到数据库会话中（暂存到内存，尚未写入数据库）
    db.add(new_char)
    # 提交事务，将新角色记录真正写入数据库的 user_characters 表
    db.commit()
    # 刷新对象，从数据库获取最新的数据（如自动生成的 id、默认值 created_at/updated_at）
    db.refresh(new_char)
    # 返回新建成功的消息
    return {"message": "成功建立新关系", "character": new_char}


@router.get("/my", response_model=Optional[CharacterInfo])
async def get_my_character(
    user_id: int = Depends(require_user_id),  # 从 JWT 令牌中解析当前用户 ID
    db: Session = Depends(get_db),            # 获取数据库会话
):
    """获取当前用户正在使用的（活跃的）角色信息"""
    # 查询当前用户 is_active 为 True 的角色记录
    char = db.query(UserCharacter).filter(
        UserCharacter.user_id == user_id,    # 当前登录用户
        UserCharacter.is_active == True      # 只查活跃角色（用户同时只能有一个活跃角色）
    ).first()                                # 取第一个结果（理论上只有一个活跃角色）
    if char is None:
        # 如果用户还没有选择任何角色，返回 null，前端会根据 null 跳转到角色选择页
        return None
    # 将数据库模型转换为 CharacterInfo 响应模型，只暴露需要的字段
    return CharacterInfo(
        gender=char.gender,                       # 角色性别
        personality=char.personality,             # 角色性格
        custom_name=char.custom_name,             # 用户自定义名称（可能为 None）
        relationship_stage=char.relationship_stage, # 关系阶段（0-5）
        intimacy_score=char.intimacy_score,        # 亲密度分数（0.0-1.0）
    )
