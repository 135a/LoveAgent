## ADDED Requirements

### Requirement: 对话轮次处理
The system SHALL 通过 LangGraph pipeline 处理用户消息：输入门控 → 记忆检索 → Prompt 组装 → LLM 调用 → 后处理 → 响应。

#### Scenario: 正常对话流程
- **WHEN** 用户发送一条消息
- **THEN** 系统依次执行意图分析、记忆检索、Prompt 构建、DeepSeek 调用、后处理，最终返回回复

#### Scenario: 空消息处理
- **WHEN** 用户发送空消息或纯空白消息
- **THEN** 系统返回提示"说点什么吧～"

### Requirement: WebSocket 实时通信
The system SHALL 通过 WebSocket 实现实时消息传输，支持流式打字机效果。

#### Scenario: 建立连接
- **WHEN** 用户进入聊天界面
- **THEN** 前端建立 WebSocket 连接（带 JWT token 认证）

#### Scenario: 流式回复
- **WHEN** 用户发送消息后
- **THEN** AI 回复以流式方式逐字返回，前端展示打字机效果

### Requirement: 情感意图检测
The system SHALL 在 Input Gate 节点检测用户消息的情感倾向和意图。

#### Scenario: 正面情感
- **WHEN** 用户发送"今天好开心！"
- **THEN** 系统标记情感为"开心"，亲密度微调 +0.01

#### Scenario: 负面情感
- **WHEN** 用户发送"今天心情很差"
- **THEN** 系统标记情感为"低落"，角色回复增加安慰语气

### Requirement: 对话控制
The system SHALL 支持重置对话历史但保留关系状态。

#### Scenario: 重置对话
- **WHEN** 用户执行重置操作
- **THEN** 系统清空当前对话历史，但关系阶段和亲密度保持不变
