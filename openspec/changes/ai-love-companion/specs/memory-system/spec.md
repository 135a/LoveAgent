## ADDED Requirements

### Requirement: 三层记忆架构
The system SHALL 实现三层记忆：工作记忆（当前对话 N 轮）、摘要记忆（对话摘要）、向量记忆（语义检索）。

#### Scenario: 三层协同
- **WHEN** 用户发送消息
- **THEN** 系统从三层记忆中检索相关内容，合并注入 Prompt

### Requirement: 工作记忆按用户隔离
The system SHALL 为每个用户维护独立的工作记忆窗口。

#### Scenario: 多用户不混淆
- **WHEN** 用户 A 和用户 B 同时在线聊天
- **THEN** A 的工作记忆只包含 A 的对话，B 的工作记忆只包含 B 的对话

### Requirement: 摘要记忆
The system SHALL 在对话结束时自动生成摘要，按用户和会话存储。

#### Scenario: 生成摘要
- **WHEN** 用户关闭对话或会话超时
- **THEN** 系统生成该次对话的摘要，存入 MySQL（关联 user_id 和 conversation_id）

#### Scenario: 加载历史摘要
- **WHEN** 用户开始新对话
- **THEN** 系统加载该用户之前的对话摘要作为上下文（仅该用户的摘要）

### Requirement: 向量记忆按用户隔离
The system SHALL 将每个用户的向量记忆存入独立的 ChromaDB Collection（命名规则：`user_{id}_memory`）。

#### Scenario: 存储记忆
- **WHEN** 用户分享个人信息（如"我喜欢吃火锅"）
- **THEN** 系统提取关键信息，向量化存入该用户的 ChromaDB Collection

#### Scenario: 检索不跨用户
- **WHEN** 用户 A 查询记忆
- **THEN** 只从 `user_A_memory` Collection 检索，不会搜到用户 B 的记忆

#### Scenario: 跨会话回忆
- **WHEN** 用户在新对话中说"你还记得我喜欢吃什么吗？"
- **THEN** 系统从该用户的向量记忆检索到"火锅"，回复"当然记得，你最喜欢吃火锅了～"

### Requirement: 记忆情感权重
The system SHALL 为记忆标记情感权重，高权重记忆检索优先级更高。

#### Scenario: 重要记忆优先
- **WHEN** 用户曾深度分享过某件事
- **THEN** 该记忆的向量在检索时获得更高排序
