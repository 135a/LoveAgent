## Why

1. **选角交互受限**：目前用户点击“切换恋人”会被强制重定向回当前聊天，无法重新选择性别和性格，这限制了多恋人并存的自由度。
2. **对话互动性不足**：AI 目前完全处于“应答”模式，在用户沉默时无法主动发起话题，缺乏真实的情感交互。

## What Changes

- **增强选角页灵活性**：通过路由参数区分“首次进入”和“手动切换”，允许用户在已有角色时依然可以进入选择界面。
- **引入异步主动聊天机制**：WebSocket 循环新增超时监听，当用户长时间不发言时，触发 AI 的主动关怀或话题延续逻辑。
- **动态 Prompt 注入**：针对系统自动触发的对话，向 LLM 注入专门的引导语。

## Capabilities

### New Capabilities
- `async-proactive-chat`: AI 具备基于时间的独立发起对话能力。

### Modified Capabilities
- `web-frontend`: 修正角色选择页面的拦截和跳转逻辑。
- `chat-interaction`: 改造长连接循环，支持并发任务监听。

## Impact

- `frontend/src/views/CharacterSelect.vue`: 调整 `onMounted` 拦截逻辑。
- `frontend/src/views/Chat.vue`: 修改跳转路由。
- `backend/app/routes/chat.py`: 重构 WebSocket 主循环，引入 `asyncio.wait`。
- `backend/app/graph/nodes.py`: 适配系统主动触发信号。
