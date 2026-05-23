## MODIFIED Requirements

### Requirement: 聊天主界面
The system SHALL 提供聊天主界面，包含消息列表、输入框。应保持界面简洁，不强制显示关系状态。

#### Scenario: 发送消息
- **WHEN** 用户在输入框输入消息并发送
- **THEN** 消息显示在列表中，AI 回复展示在界面上

#### Scenario: 纯净对话模式
- **WHEN** 用户在聊天界面
- **THEN** 界面顶端不应展示关系阶段标签（如"相识"）和亲密度进度条，以提供更沉浸的对话体验

## REMOVED Requirements

### Requirement: 关系状态展示
**Reason**: 用户认为该界面元素多余且干扰体验，更倾向于极简的对话 UI。
**Migration**: 所有的关系进化逻辑保留在后端，但前端不再通过进度条形式强制展示。
