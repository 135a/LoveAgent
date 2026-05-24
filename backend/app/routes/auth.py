# 导入 FastAPI 路由工具：APIRouter 创建路由分组，Depends 实现依赖注入，HTTPException 抛出 HTTP 错误，status 提供 HTTP 状态码常量
from fastapi import APIRouter, Depends, HTTPException, status
# 导入 Pydantic 的数据模型基类，用于声明请求和响应的数据结构
from pydantic import BaseModel
# 导入 SQLAlchemy 的会话类型，用于数据库操作的类型注解
from sqlalchemy.orm import Session

# 导入数据库会话依赖，FastAPI 会通过 Depends(get_db) 自动注入数据库会话
from app.database import get_db
# 导入用户 ORM 模型，对应数据库中的 users 表
from app.models import User
# 导入 JWT 工具函数：hash_password 加密密码，verify_password 验证密码，create_access_token 生成 JWT 令牌
from app.middleware.jwt import hash_password, verify_password, create_access_token

# 创建认证路由分组，所有端点自动添加 /api/auth 前缀，在 API 文档中归类到 "auth" 标签下
router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):

    """
    用户注册请求模型类
    用于接收和处理用户注册时的请求数据
    """
    username: str  # 用户名，字符串类型
    password: str  # 密码，字符串类型


class LoginRequest(BaseModel):
    """用户登录请求模型，包含用户名和密码"""
    username: str  # 登录用户名
    password: str  # 登录密码


class AuthResponse(BaseModel):
    """认证成功后的统一响应模型，包含令牌和用户基本信息"""
    token: str    # JWT 访问令牌，后续请求需在 Header 中携带此令牌
    user_id: int  # 用户唯一标识 ID
    username: str  # 用户名


@router.post("/register")
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # 校验密码长度，如果少于 6 位则返回 400 错误并提示具体原因
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="密码至少需要 6 位")
    # 查询数据库中是否已存在相同用户名的记录，first() 返回第一个匹配结果或 None
    existing = db.query(User).filter(User.username == req.username).first()
    # 如果用户名已存在，返回 409 冲突错误，阻止重复注册
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户名已被注册")

    # 创建新的 User 模型实例，密码经过哈希加密后存储，绝不存储明文密码
    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
    )
    # 将新用户对象添加到数据库会话中（暂存到内存，尚未写入数据库）
    db.add(user)
    # 提交事务，将新增用户真正写入数据库
    db.commit()
    # 刷新 user 对象，从数据库中获取最新的数据（如自增的 id、默认的 created_at）
    db.refresh(user)

    # 为用户生成 JWT 令牌，令牌中编码了用户 ID，后续请求凭此令牌鉴权
    token = create_access_token(user.id)
    # 返回统一的认证响应，包含令牌和用户基本信息
    return AuthResponse(token=token, user_id=user.id, username=user.username)


@router.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    # 根据用户名查询用户，first() 返回匹配的第一个用户或 None
    user = db.query(User).filter(User.username == req.username).first()
    # 验证用户是否存在，以及密码是否匹配（将明文密码与数据库中的哈希值比对）
    if not user or not verify_password(req.password, user.password_hash):
        # 用户名不存在或密码错误都返回 401 未授权，不透露具体是哪个错了（防止枚举攻击）
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    # 登录成功后为用户生成 JWT 令牌
    token = create_access_token(user.id)
    # 返回统一的认证响应
    return AuthResponse(token=token, user_id=user.id, username=user.username)
