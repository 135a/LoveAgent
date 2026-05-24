## ADDED Requirements

### Requirement: 对话主动性
系统 SHALL 要求 AI 根据对话历史主动发起后续互动。

#### Scenario: 引导式聊天
- **WHEN** 用户简单回答“嗯”或“知道了”
- **THEN** AI 应当通过分享自己的相关小事或询问用户感受来维持对话流，而不是只回一个表情。

### Requirement: 图片知识集成
系统 SHALL 通过文本转录方式使 AI 获取图片中的历史背景。

#### Scenario: 提及旧友
- **WHEN** 用户提到“那个把你拉黑的朋友”
- **THEN** AI 能根据转录出的文本知识，准确回忆起当时的难过和对话细节。

## MODIFIED Requirements

### Requirement: 聊天主界面
The system SHALL 确保顶部控制栏（切换、登出）在不同分辨率下均可见。

#### Scenario: 按钮展示
- **WHEN** 用户进入聊天页
- **THEN** 页面上方应始终显示“切换恋人”和“退出登录”按钮。
