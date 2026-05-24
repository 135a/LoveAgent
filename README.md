# LoveAgent - AI 虚拟伴侣

基于 LangChain + LangGraph 的 AI 虚拟伴侣应用。选择性别和性格，开始一段慢热的关系养成之旅。

## 快速启动

### 前置要求

- Docker & Docker Compose
- DeepSeek API Key

### 一键启动

```bash
# 1. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY

# 2. 启动所有服务
docker compose up -d

# 3. 访问前端
open http://localhost:8080
```

### 手动启动（开发模式）

**后端：**

```bash
cd backend
pip install .
# 确保 MySQL(3306) 和 ChromaDB(8000) 已启动
uvicorn app.main:app --reload --port 8000
```

**前端：**

```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
LoveAgent/
├── docker-compose.yml       # Docker 编排（MySQL + ChromaDB + 后端 + 前端）
├── backend/                  # Python FastAPI 后端
│   └── app/
│       ├── main.py          # 应用入口
│       ├── config.py        # 配置管理
│       ├── database.py      # 数据库连接
│       ├── init_app.py      # 初始化逻辑
│       ├── graph/           # LangGraph 对话编排
│       │   ├── graph.py     # 对话图定义
│       │   ├── nodes.py     # 图节点
│       │   └── state.py     # 对话状态
│       ├── characters/      # 角色系统
│       │   ├── base.py      # 角色基类
│       │   └── engine.py    # 角色引擎
│       ├── memory/          # 记忆系统
│       │   ├── vector_store.py  # 向量存储 (ChromaDB)
│       │   └── summarizer.py    # 记忆摘要
│       ├── knowledge/       # 知识库引擎
│       │   ├── ingestion.py # 知识导入
│       │   └── retriever.py # 知识检索
│       ├── relationship/    # 关系系统
│       │   └── engine.py    # 关系进展引擎
│       ├── routes/          # API 路由
│       │   ├── auth.py      # 认证
│       │   ├── chat.py      # 聊天
│       │   ├── characters.py # 角色
│       │   ├── knowledge.py # 知识库
│       │   └── relationship.py # 关系
│       ├── middleware/       # 中间件
│       │   └── jwt.py       # JWT 鉴权
│       ├── services/        # 外部服务
│       │   └── deepseek.py  # DeepSeek API 调用
│       └── models/          # 数据模型
├── frontend/                # Vue 3 前端
│   └── src/
│       ├── views/           # 页面
│       │   ├── Login.vue    # 登录/注册
│       │   ├── CharacterSelect.vue  # 角色选择
│       │   ├── Chat.vue     # 聊天界面
│       │   └── Settings.vue # 设置
│       ├── stores/          # Pinia 状态管理
│       ├── router/          # 路由配置
│       ├── composables/     # 组合式函数 (WebSocket)
│       └── utils/           # 工具 (Axios 封装)
├── knowledge/               # 知识库目录
│   ├── user/                # AI 了解用户的知识
│   └── character/           # AI 角色自身的知识
└── data/                    # 持久化数据
```

## 功能特性

- **角色系统** — 选择角色性别与性格，获得独特的陪伴体验
- **LangGraph 对话编排** — 基于状态图的对话流程，支持多轮上下文
- **关系养成** — 关系阶段动态演进，从陌生到亲密逐步解锁
- **记忆系统** — ChromaDB 向量存储，AI 能记住你们的过往对话
- **知识库** — 支持角色知识注入，让 AI 更懂你和它自己
- **WebSocket 实时通信** — 流式消息推送，对话体验更流畅
- **JWT 认证** — 用户系统支持多账号隔离

## 技术栈

- **前端**: Vue 3 + Pinia + Element Plus + WebSocket
- **后端**: Python FastAPI + LangChain + LangGraph
- **LLM**: DeepSeek API
- **数据库**: MySQL 8.0 + ChromaDB（向量数据库）
- **部署**: Docker Compose
