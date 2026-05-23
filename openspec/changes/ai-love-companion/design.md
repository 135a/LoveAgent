## Context

构建一个基于 LangChain 的 AI 虚拟伴侣应用。用户注册/登录后选择 AI 伴侣性别（女生/男生）和性格变体，通过自然对话发展关系。女生角色慢热害羞，男生角色活泼幽默。采用 DeepSeek API 作为 LLM 后端，LangGraph 编排对话流程。

核心约束：**每个用户拥有独立的恋人实例**——关系阶段、亲密度、对话历史、向量记忆完全按用户隔离。不能出现多个用户共享同一个 AI 伴侣记忆的情况。

## Goals / Non-Goals

**Goals:**
- 用户注册/登录系统，JWT 鉴权
- 每个用户拥有独立的关系阶段、亲密度、记忆、对话历史
- LangGraph 对话编排，支持意图识别、记忆检索、Prompt 构建、后处理
- 6 阶段关系进化系统，亲密度数值驱动
- 分层记忆系统（工作记忆 + 摘要记忆 + 向量记忆）
- 本地知识库自动加载（角色知识全局可用，用户知识按用户隔离）
- Vue 3 前端提供登录/注册、角色选择、聊天、关系状态展示
- Docker Compose 一键启动 MySQL + ChromaDB + Backend + Frontend

**Non-Goals:**
- OAuth/第三方登录（仅用户名+密码注册）
- 管理员后台
- 移动端 App
- 语音/视频交互
- 前端上传知识库文件

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| 鉴权方式 | JWT（access token） | 无状态，适合前后端分离 |
| 密码存储 | passlib + bcrypt | 行业标准密码哈希 |
| 数据隔离策略 | 所有表/集合带 user_id 字段 | 简单可靠，查询时强制过滤 |
| ChromaDB 隔离 | Collection 名带 user_id 后缀 | 天然隔离，互不干扰 |
| LLM | DeepSeek API (deepseek-chat) | 性价比高，OpenAI 兼容格式 |
| AI 框架 | LangChain + LangGraph | 有状态图能力，适合关系状态机 |
| 向量存储 | ChromaDB | 轻量 Docker 化，按 user_id 分 Collection |
| 结构化 DB | MySQL 8.0 | 用户需求指定 |
| 前端框架 | Vue 3 + Pinia + Element Plus | 成熟稳定，组件丰富 |
| 通信方式 | WebSocket | 流式消息实时性 |

## 核心架构：多用户隔离

```
用户A                    用户B                    用户C
  │                       │                       │
  ├─ JWT: token_A         ├─ JWT: token_B         ├─ JWT: token_C
  │                       │                       │
  ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────┐
│                  FastAPI (JWT 中间件)                  │
│  从 token 解析 user_id → 注入到每个请求上下文          │
└────────┬────────────┬────────────┬──────────────────┘
         │            │            │
         ▼            ▼            ▼
  ┌────────────┐ ┌────────────┐ ┌────────────┐
  │ LangGraph A │ │ LangGraph B │ │ LangGraph C │ ← 每个用户独立的图实例
  │             │ │             │ │             │
  │ State_A     │ │ State_B     │ │ State_C     │ ← 状态完全独立
  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
         │               │               │
         ▼               ▼               ▼
  ┌─────────────────────────────────────────────┐
  │                 存储层 (按user_id隔离)         │
  │                                              │
  │  MySQL:                                       │
  │    users 表 (全局)                             │
  │    user_characters 表 (WHERE user_id = ?)    │
  │    conversations 表 (WHERE user_id = ?)      │
  │    messages 表 (WHERE user_id = ?)            │
  │                                              │
  │  ChromaDB:                                    │
  │    collection: user_{id}_memory  (向量记忆)    │
  │    collection: user_{id}_knowledge (用户知识)  │
  │    collection: global_character  (角色知识)    │
  └─────────────────────────────────────────────┘
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| DeepSeek API 不可用 | LLM 调用层抽象，可切换其他 OpenAI 兼容 API |
| ChromaDB 数据丢失 | ChromaDB 挂载 Docker volume，MySQL 存消息记录可重建 |
| 长对话上下文超限 | LangGraph 中实现对话摘要压缩，滑动窗口控制 |
| JWT token 泄露 | 设置较短过期时间（24h），后续可加 refresh token |
| 多用户并发下 ChromaDB 性能 | 单机场景用户量有限，ChromaDB 足以应对 |

## MySQL 核心表设计

```sql
-- 用户表
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 用户-角色实例表 (每个用户一条记录)
CREATE TABLE user_characters (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  gender ENUM('female', 'male') NOT NULL,
  personality VARCHAR(20) NOT NULL,      -- 文静/治愈/傲娇/阳光/风趣/暖男
  custom_name VARCHAR(50),               -- 用户给 AI 起的称呼
  relationship_stage INT DEFAULT 0,      -- 0-5
  intimacy_score FLOAT DEFAULT 0.0,      -- 0.0-1.0
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 对话表
CREATE TABLE conversations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  summary TEXT,
  message_count INT DEFAULT 0,
  started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  ended_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 消息表
CREATE TABLE messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  conversation_id INT NOT NULL,
  user_id INT NOT NULL,
  role ENUM('user', 'ai') NOT NULL,
  content TEXT NOT NULL,
  emotion_tag VARCHAR(20),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 关系里程碑
CREATE TABLE milestones (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  event_type VARCHAR(50) NOT NULL,
  description TEXT,
  intimacy_change FLOAT DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## API 路由设计

```
POST /api/auth/register    ─ 注册
POST /api/auth/login       ─ 登录，返回 JWT
GET  /api/characters       ─ 获取角色列表（按性别过滤）
POST /api/characters/choose ─ 选择性别+性格，创建角色实例
GET  /api/relationship     ─ 查询当前关系状态
WS   /api/chat             ─ WebSocket 聊天（需 JWT 认证）
POST /api/knowledge/reload ─ 重载知识库
```
