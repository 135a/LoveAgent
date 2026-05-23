## 1. 增加调试日志

- [ ] 1.1 在 `backend/app/graph/nodes.py` 的 `llm_call` 函数中打印 `system_prompt`。
- [ ] 1.2 在 `backend/app/services/deepseek.py` 的 `chat_completion` 函数中打印发送给 API 的 `messages`。

## 2. 数据库检查

- [ ] 2.1 查询 `user_characters` 表，检查 `personality` 字段的具体值。

## 3. 问题分析与修复

- [ ] 3.1 观察日志，确认 Prompt 是否包含角色设定。
- [ ] 3.2 确认 DeepSeek API 是否正确接收并返回了角色化的回复。
- [ ] 3.3 修复发现的逻辑问题。
