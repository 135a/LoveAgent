from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routes import auth, characters, relationship, knowledge
from app.routes.chat import router as chat_router
from app.knowledge.ingestion import load_all_knowledge

import app.models  # noqa: F401 - ensure models registered


# FastAPI应用的生命周期管理装饰器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

    # Load knowledge base
    print("Loading knowledge base...")
    try:
        await load_all_knowledge()
    except Exception as e:
        print(f"⚠ Knowledge base load skipped: {e}")

    yield
    # Shutdown
    engine.dispose()


app = FastAPI(
    title="LoveAgent API",
    version="0.1.0",
    lifespan=lifespan,
)

# 添加CORS中间件，用于处理跨域资源共享问题
app.add_middleware(
    CORSMiddleware,  # 使用FastAPI的CORS中间件类
    allow_origins=["*"],  # 允许所有来源的跨域请求
    allow_credentials=True,  # 允许携带凭证信息
    allow_methods=["*"],  # 允许所有的HTTP方法
    allow_headers=["*"],  # 允许所有的请求头
)


# 健康检查接口，用于服务状态监控
@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "LoveAgent is running"}

# ===== 注册路由模块 =====
# 将各功能模块的路由注册到 FastAPI 应用中，这样对应的 API 端点才能被访问
# 每个 .router 是 FastAPI 的 APIRouter 实例，包含了该模块下所有路由的定义

# 认证路由：用户注册、登录、获取当前用户信息等
# 注册的端点：POST /api/auth/register, POST /api/auth/login, GET /api/auth/me
app.include_router(auth.router)

# 角色路由：获取角色列表、选择角色、切换角色等
# 注册的端点：GET /api/characters, POST /api/characters/select, GET /api/characters/current
app.include_router(characters.router)

# 关系路由：好感度、亲密度、里程碑等角色关系状态
# 注册的端点：GET /api/relationship/status, GET /api/relationship/milestones
app.include_router(relationship.router)

# 知识路由：用户上传、管理自定义知识，以及检索相关知识
# 注册的端点：POST /api/knowledge/upload, GET /api/knowledge/list, POST /api/knowledge/search
app.include_router(knowledge.router)

# 聊天路由：WebSocket 实时聊天通信
# 注册的端点：WebSocket /api/chat/ws/{conversation_id}
# 注意：这是从 chat.py 导入的 chat_router，与其他路由分开导入是为了避免命名冲突
app.include_router(chat_router)
