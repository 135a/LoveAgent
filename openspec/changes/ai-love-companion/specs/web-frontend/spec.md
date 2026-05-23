## ADDED Requirements

### Requirement: 登录/注册页面
The system SHALL 提供登录和注册页面作为应用的入口。

#### Scenario: 首次访问
- **WHEN** 用户首次访问应用
- **THEN** 展示登录页面，提供"注册"入口链接

#### Scenario: 注册流程
- **WHEN** 用户点击注册，填写用户名和密码
- **THEN** 注册成功后自动登录并跳转到角色选择页

#### Scenario: 自动登录
- **WHEN** 用户已有 JWT token 且未过期
- **THEN** 自动跳过登录页，直接进入角色选择或聊天页

### Requirement: 角色选择界面
The system SHALL 提供角色选择界面，包含性别选择和性格变体选择。

#### Scenario: 选择性别
- **WHEN** 用户进入角色选择页
- **THEN** 展示两个性别卡片（女生/男生），用户点击选择

#### Scenario: 选择性格变体
- **WHEN** 用户选择性别后
- **THEN** 展示该性别对应的 3 个性格变体卡片供选择

#### Scenario: 已有角色实例
- **WHEN** 用户已有角色实例
- **THEN** 直接进入聊天界面，跳过角色选择

### Requirement: 聊天主界面
The system SHALL 提供聊天主界面，包含消息列表、输入框、关系状态。

#### Scenario: 发送消息
- **WHEN** 用户在输入框输入消息并发送
- **THEN** 消息显示在列表中，AI 回复以打字机效果逐字展示

#### Scenario: 关系状态展示
- **WHEN** 用户在聊天界面
- **THEN** 显示当前关系阶段标签（如"相识"）和亲密度进度条

#### Scenario: 记忆提示
- **WHEN** AI 回复中引用记忆
- **THEN** 前端展示"回忆中…"提示

### Requirement: 设置页面
The system SHALL 提供设置页面修改角色称呼等。

#### Scenario: 修改称呼
- **WHEN** 用户在设置中修改对 AI 的称呼
- **THEN** 调用 API 保存，后续对话使用新称呼

### Requirement: 用户登出
The system SHALL 提供登出功能。

#### Scenario: 登出
- **WHEN** 用户点击登出
- **THEN** 清除本地 JWT token，跳转到登录页
