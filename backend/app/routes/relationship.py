# 导入 FastAPI 路由工具：APIRouter 创建路由分组，Depends 实现依赖注入，HTTPException 抛出 HTTP 错误
from fastapi import APIRouter, Depends, HTTPException
# 导入 Pydantic 的数据模型基类，用于声明响应数据结构
from pydantic import BaseModel
# 导入 SQLAlchemy 的会话类型，用于数据库操作的类型注解
from sqlalchemy.orm import Session

# 导入数据库会话依赖，FastAPI 通过 Depends(get_db) 自动注入数据库会话
from app.database import get_db
# 导入 JWT 中间件中的用户 ID 获取函数，从令牌中解析出当前登录用户的 ID
from app.middleware.jwt import require_user_id
# 导入 ORM 模型：UserCharacter 用户角色表，Milestone 关系里程碑表
from app.models import UserCharacter, Milestone
# 导入关系引擎，get_stage_info 根据关系阶段数字返回对应的阶段名称和描述
from app.relationship.engine import get_stage_info

# 创建关系路由分组，所有端点自动添加 /api/relationship 前缀，API 文档中归类到 "relationship" 标签下
router = APIRouter(prefix="/api/relationship", tags=["relationship"])


class RelationshipResponse(BaseModel):
    """关系状态响应模型，包含当前关系阶段信息和里程碑记录"""
    stage: int                     # 关系阶段数字：0-5，数字越高关系越亲密
    stage_name: str                # 关系阶段中文名称，如"陌生人"、"朋友"、"恋人"等
    intimacy_score: float           # 当前亲密度分数：0.0-1.0
    milestones: list[dict]         # 最近的里程碑事件列表（按时间倒序，最多20条）


@router.get("/")
async def get_relationship(
    user_id: int = Depends(require_user_id),   # 从 JWT 令牌中解析当前用户 ID
    db: Session = Depends(get_db),             # 获取数据库会话
):
    """获取当前用户与其角色的关系状态，包括关系阶段、亲密度和里程碑记录"""
    # 查询当前用户的角色记录（关联用户与角色关系的核心数据表）
    char = db.query(UserCharacter).filter(UserCharacter.user_id == user_id).first()
    # 如果用户还没有创建过角色，返回 404 错误，提示前端引导用户去选择角色
    if char is None:
        raise HTTPException(status_code=404, detail="尚未创建角色")

    # 根据关系阶段数字获取阶段详情（名称、描述、阈值等）
    stage_info = get_stage_info(char.relationship_stage)
    # 查询该用户的所有里程碑事件，按创建时间倒序排列，最多取最近 20 条
    milestones = db.query(Milestone).filter(
        Milestone.user_id == user_id             # 只查当前用户的里程碑
    ).order_by(Milestone.created_at.desc()).limit(20).all()  # 倒序 + 限制数量

    # 组装并返回关系状态响应
    return RelationshipResponse(
        stage=char.relationship_stage,           # 当前阶段数字
        stage_name=stage_info["name"],           # 当前阶段中文名称（从引擎查询）
        intimacy_score=char.intimacy_score,      # 当前亲密度分数
        # 将里程碑 ORM 对象列表转换为字典列表，暴露给前端
        milestones=[
            {
                "event_type": m.event_type,        # 里程碑事件类型（如"首次对话"、"表白"）
                "description": m.description,      # 事件描述文本
                "intimacy_change": m.intimacy_change, # 亲密度变化值（正数增加，负数减少）
                "created_at": str(m.created_at)    # 事件发生时间，转为字符串便于 JSON 序列化
            }
            for m in milestones                   # 遍历所有查询到的里程碑记录
        ],
    )
