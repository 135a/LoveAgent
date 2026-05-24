## 1. 前端选角重定向修复

- [x] 1.1 修改 `frontend/src/views/Chat.vue`：更新 `goSwitch` 函数，使用 `router.push('/characters?action=switch')`。
- [x] 1.2 修改 `frontend/src/views/CharacterSelect.vue`：从 `vue-router` 引入 `useRoute`，在 `onMounted` 逻辑中加入 `route.query.action === 'switch'` 的豁免判断。

## 2. 后端主动聊天逻辑实现

- [x] 2.1 修改 `backend/app/routes/chat.py`：重构 `while` 循环，使用 `asyncio.create_task` 和 `asyncio.wait` 实现带超时的异步消息接收。
- [x] 2.2 在超时分支中，判定是否需要触发主动聊天（检查最后一条消息角色），并向 Graph 注入 `[SYSTEM_PROACTIVE_TRIGGER]`。
- [x] 2.3 修改 `backend/app/graph/nodes.py`：在 `prompt_assembly` 或 `llm_call` 节点拦截特殊输入，替换为系统引导词，并确保此输入不被持久化到数据库。

## 3. 部署与验证

- [x] 3.1 运行 `docker-compose up -d --build` 应用变更。
- [x] 3.2 验证点击“切换恋人”后可以进入选择页并成功创建新性格恋人。
- [x] 3.3 验证在聊天窗口静止一段时间后，AI 是否会自动发来新话题。
