## ADDED Requirements

### Requirement: Docker Compose 编排
The system SHALL 通过 Docker Compose 一键启动 MySQL、ChromaDB、后端、前端四个服务。

#### Scenario: 一键启动
- **WHEN** 用户执行 `docker compose up -d`
- **THEN** 四个容器依次启动，就绪后通过 `localhost:8080` 访问前端

### Requirement: MySQL 8.0
The system SHALL 使用 MySQL 8.0 存储结构化数据。

#### Scenario: 自动初始化
- **WHEN** 后端首次启动
- **THEN** 自动连接 MySQL 并创建所有表结构

#### Scenario: 数据持久化
- **WHEN** 容器重启
- **THEN** MySQL 数据从 Docker volume 恢复，不丢失

### Requirement: ChromaDB 向量存储
The system SHALL 使用 ChromaDB 作为向量存储引擎。

#### Scenario: 自动创建 Collection
- **WHEN** 新用户首次对话
- **THEN** 自动创建该用户的 ChromaDB Collection（`user_{id}_memory`）

### Requirement: 环境变量配置
The system SHALL 通过 `.env` 文件管理配置。

#### Scenario: 配置加载
- **WHEN** 后端启动
- **THEN** 从 `.env` 读取 `DEEPSEEK_API_KEY`、`MYSQL_PASSWORD`、`JWT_SECRET` 等配置

### Requirement: 一键启动流程
The system SHALL 提供清晰的启动指引。

#### Scenario: 新用户部署
- **WHEN** 用户首次部署
- **THEN** 只需执行 `cp .env.example .env` 填入 API Key → `docker compose up -d` → 访问浏览器
