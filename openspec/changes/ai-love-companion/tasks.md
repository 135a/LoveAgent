## 1. 基础设施搭建

- [x] 1.1 创建项目目录结构（backend/、frontend/、knowledge/）
- [x] 1.2 编写 docker-compose.yml（MySQL + ChromaDB + Backend + Frontend）
- [x] 1.3 编写 backend/Dockerfile
- [x] 1.4 编写 frontend/Dockerfile + nginx.conf
- [x] 1.5 编写 .env.example 和 .env
- [x] 1.6 编写 README.md（启动指引）

## 2. 后端基础框架

- [x] 2.1 初始化 Python 项目（pyproject.toml，依赖：fastapi, langchain, langgraph, chromadb, mysql-connector, openai, python-jose, passlib, uvicorn）
- [x] 2.2 编写 app/config.py（环境变量加载）
- [x] 2.3 编写 app/main.py（FastAPI 入口，CORS 配置）
- [x] 2.4 编写 app/database.py（MySQL 连接 + SQLAlchemy 初始化）
- [x] 2.5 编写 app/models/ 目录下所有 ORM 模型（users, user_characters, conversations, messages, milestones）

## 3. 用户认证系统

- [x] 3.1 编写 app/routes/auth.py（注册 POST /api/auth/register）
- [x] 3.2 编写 app/routes/auth.py（登录 POST /api/auth/login，返回 JWT）
- [x] 3.3 编写 app/middleware/jwt.py（JWT 中间件，从请求头解析 token）
- [x] 3.4 编写依赖注入函数 get_current_user_id（供受保护路由使用）

## 4. 角色系统

- [x] 4.1 编写角色预设模板 JSON（female: 文静/治愈/傲娇，male: 阳光/风趣/暖男）
- [x] 4.2 编写 app/characters/base.py（角色数据模型 + Prompt 模板）
- [x] 4.3 编写 app/characters/engine.py（根据性别+性格生成 System Prompt）
- [x] 4.4 编写 app/routes/characters.py（获取角色列表、选择角色创建实例）

## 5. LangGraph 对话编排

- [x] 5.1 编写 app/graph/state.py（定义 LangGraph State：messages, user_id, character_id, relationship_stage, intimacy_score 等）
- [x] 5.2 编写 app/graph/nodes.py（input_gate, memory_retrieval, prompt_assembly, llm_call, post_processing 各节点）
- [x] 5.3 编写 app/graph/graph.py（构建 LangGraph 状态图，连接各节点）
- [x] 5.4 编写 app/services/deepseek.py（DeepSeek API 封装，OpenAI 兼容格式）

## 6. 记忆系统

- [x] 6.1 编写 app/memory/vector_store.py（ChromaDB 封装，按 user_id 隔离 Collection）
- [x] 6.2 编写 app/memory/summarizer.py（对话摘要生成与压缩）
- [x] 6.3 实现工作记忆滑动窗口（保留最近 30 轮对话）

## 7. 关系进化系统

- [x] 7.1 定义 6 阶段关系配置（亲密度阈值、各阶段 Prompt 风格）
- [x] 7.2 实现亲密度计算引擎（加分/扣分/衰减逻辑）
- [x] 7.3 实现阶段转换逻辑（达到阈值自动升级，更新角色 Prompt）
- [x] 7.4 编写 app/routes/relationship.py（查询关系状态 API）

## 8. 知识库系统

- [x] 8.1 编写 app/knowledge/ingestion.py（文件解析 + 文本分块）
- [x] 8.2 编写 app/knowledge/retriever.py（向量检索封装，按用户/角色分类）
- [x] 8.3 实现启动时自动加载 knowledge/ 目录
- [x] 8.4 编写 app/routes/knowledge.py（知识库重载 API）
- [x] 8.5 创建示例知识文件（knowledge/character/female/、knowledge/character/male/、knowledge/user/）

## 9. 聊天 WebSocket

- [x] 9.1 编写 app/routes/chat.py（WebSocket 端点，JWT 认证）
- [x] 9.2 集成 LangGraph 图（接收消息 → 执行图 → 流式返回）
- [x] 9.3 实现消息持久化（存入 MySQL messages 表）

## 10. Vue 3 前端

- [x] 10.1 初始化 Vue 3 + Vite + Pinia + Element Plus 项目
- [x] 10.2 配置 vue-router（登录页、角色选择页、聊天页、设置页）
- [x] 10.3 实现登录/注册页面组件
- [x] 10.4 实现角色选择页面（性别卡片 + 性格变体卡片）
- [x] 10.5 实现聊天主界面（消息列表 + 输入框 + 打字机效果）
- [x] 10.6 实现关系状态展示组件（阶段标签 + 亲密度进度条）
- [x] 10.7 实现设置页面（修改称呼、重置对话、登出）
- [x] 10.8 实现 WebSocket 客户端 composable（useWebSocket.js）
- [x] 10.9 配置 axios 拦截器（自动携带 JWT token）

## 11. 集成与测试

- [x] 11.1 编写后端启动初始化脚本（建表 + 加载知识库 + 创建默认角色）
- [x] 11.2 测试完整流程：注册 → 登录 → 选角色 → 聊天 → 关系进化
- [x] 11.3 测试多用户隔离（注册两个用户，验证记忆不串）
- [x] 11.4 测试 Docker Compose 一键启动
