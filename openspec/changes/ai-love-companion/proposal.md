## Why

构建一个基于 LangChain 的 AI 虚拟伴侣应用，提供沉浸式的角色扮演和关系养成体验。用户可以选择 AI 伴侣的性别（男/女），在不同性格变体中做选择，随和、慢热地发展一段虚拟关系。通过知识库系统（用户知识 + 角色设定知识）增强 AI 的个性化和真实感。

## What Changes

- 新建一个完整的全栈项目，包含 Vue 3 前端 + FastAPI 后端 + LangGraph AI 编排
- 搭建 MySQL + ChromaDB 双存储架构（结构化数据 + 向量检索）
- 实现两个核心 AI 角色：女生（慢热害羞型）和男生（活泼幽默型），各带 3 个性格变体
- 实现 6 阶段关系进化系统（陌生人→相识→朋友→暧昧→恋爱中→亲密关系），带亲密度数值驱动
- 实现本地知识库系统：`knowledge/user/`（用户知识）和 `knowledge/character/`（角色设定知识），启动时自动加载到 ChromaDB
- **实现用户注册/登录系统，每个用户拥有独立的恋人实例**（关系阶段、亲密度、记忆、对话历史完全隔离）
- Docker Compose 一键启动所有服务

## Capabilities

### New Capabilities
- `user-auth`: 用户注册/登录系统，JWT 鉴权，每个用户拥有独立的恋人实例
- `chat-interaction`: 基于 LangGraph 的 AI 对话编排，包含情感检测、记忆检索、Prompt 构建、后处理
- `character-system`: 角色定义与管理系统，支持性别选择 + 性格变体 + 人格设定
- `relationship-evolution`: 6 阶段关系进化引擎，亲密度计算，阶段转换逻辑
- `memory-system`: 分层记忆系统（短期对话 + 向量检索 + 摘要记忆），**按用户隔离**
- `knowledge-base`: 本地知识库加载与检索（用户知识 + 角色知识）
- `web-frontend`: Vue 3 前端聊天界面，角色选择，关系状态展示，登录/注册页面
- `infrastructure`: Docker Compose 容器化部署（MySQL + ChromaDB + Backend + Frontend）

### Modified Capabilities
- 无（全新项目）

## Impact

- 新建 `LoveAgent/` 项目目录，包含完整的全栈代码
- Python 后端依赖：langchain, langgraph, fastapi, chromadb, mysql-connector, openai(兼容 deepseek), python-jose(JWT), passlib(密码哈希)
- 前端依赖：Vue 3, Pinia, Naive UI/Element Plus, WebSocket 客户端, vue-router
- 基础设施：Docker Compose 编排 4 个容器
- 知识库：`knowledge/` 目录下放置用户和角色知识文件
- **每个用户独立隔离**：ChromaDB 中按 user_id 隔离向量数据，MySQL 中按 user_id 隔离对话/关系数据
