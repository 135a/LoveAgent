## ADDED Requirements

### Requirement: 本地目录知识库
The system SHALL 从 `knowledge/` 目录加载知识文件，目录结构为 `knowledge/user/` 和 `knowledge/character/`。

#### Scenario: 加载用户知识
- **WHEN** 后端启动
- **THEN** 自动扫描 `knowledge/user/` 下所有 `.txt` 和 `.md` 文件，分块向量化后存入 ChromaDB（每个用户独立的 Collection）

#### Scenario: 加载角色知识
- **WHEN** 后端启动
- **THEN** 自动扫描 `knowledge/character/<gender>/` 下所有文件，分块向量化后存入全局 ChromaDB Collection（所有用户共享）

### Requirement: 知识文件格式
The system SHALL 支持 `.txt` 和 `.md` 格式的知识文件。

#### Scenario: txt 加载
- **WHEN** `knowledge/user/about_me.txt` 存在
- **THEN** 系统读取内容并按段落分块

#### Scenario: md 加载
- **WHEN** `knowledge/character/female/backstory.md` 存在
- **THEN** 系统读取内容并按段落分块

### Requirement: 对话中知识检索
The system SHALL 在对话时自动检索相关知识注入 Prompt。

#### Scenario: 用户知识注入
- **WHEN** 用户谈到与知识库相关的内容
- **THEN** 系统从该用户的 ChromaDB Collection 检索相关片段，注入 Prompt

#### Scenario: 角色知识注入
- **WHEN** 用户询问角色背景
- **THEN** 系统从角色知识库检索相关内容，角色能回答自己的"故事"

### Requirement: 知识库重载
The system SHALL 提供 API 接口手动触发知识库重新加载。

#### Scenario: 手动重载
- **WHEN** 用户更新了 knowledge/ 目录中的文件
- **THEN** 调用 API 端点触发重新加载，无需重启服务
