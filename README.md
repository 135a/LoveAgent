# LoveAgent - AI 虚拟伴侣

基于 LangChain 的 AI 虚拟伴侣应用。选择性别和性格，开始一段慢热的关系养成之旅。

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
# 确保 MySQL 和 ChromaDB 已启动
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
├── docker-compose.yml       # Docker 编排
├── backend/                  # Python FastAPI 后端
│   └── app/
│       ├── graph/           # LangGraph 对话编排
│       ├── characters/      # 角色系统
│       ├── memory/          # 记忆系统 (ChromaDB)
│       ├── knowledge/       # 知识库引擎
│       └── routes/          # API 路由
├── frontend/                # Vue 3 前端
├── knowledge/               # 知识库目录
│   ├── user/               # AI了解用户的知识
│   └── character/          # AI角色自身的知识
└── data/                    # 持久化数据
```

## 技术栈

- **前端**: Vue 3 + Pinia + Element Plus
- **后端**: Python FastAPI + LangChain + LangGraph
- **LLM**: DeepSeek API
- **数据库**: MySQL 8.0 + ChromaDB
- **部署**: Docker Compose
