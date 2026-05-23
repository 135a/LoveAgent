## ADDED Requirements

### Requirement: 对话调试能力
系统 SHALL 记录发送给 LLM 的完整提示词载荷，以便在角色失效时进行排查。

#### Scenario: 日志查看
- **WHEN** 对话发生时
- **THEN** 后端控制台输出当前使用的 System Prompt 和上下文消息
