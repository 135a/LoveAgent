## Why

AI 助手在对话中未能遵循预设角色（img_2.png 显示其回答为 DeepSeek 默认助手），说明 System Prompt 注入或模型调用逻辑存在问题。我们需要通过增加日志记录来定位 Prompt 在哪个环节丢失或被忽略。

## What Changes

- **增加详细日志**：在 `backend/app/graph/nodes.py` 中打印生成的 `system_prompt`。
- **打印模型请求载荷**：在 `backend/app/services/deepseek.py` 中记录发送给 API 的完整消息列表。
- **检查数据库数据**：确认 `user_characters` 表中的性格字段与代码映射逻辑一致。
- **修复潜在漏洞**：根据日志发现的问题，修复 Prompt 组装或传递中的 Bug。

## Capabilities

### New Capabilities
- 无

### Modified Capabilities
- `chat-interaction`: 提高对话系统的可观测性，修复角色设定失效的问题。

## Impact

- `backend/app/graph/nodes.py`: 增加打印语句。
- `backend/app/services/deepseek.py`: 增加打印语句。
