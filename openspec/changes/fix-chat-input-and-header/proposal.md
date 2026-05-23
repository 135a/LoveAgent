## Why

用户在聊天界面无法输入文字，且认为顶部的关系进度条（亲密度、关系阶段）是多余的。解决无法输入的问题是保证应用可用的首要任务，同时精简 UI 以符合用户审美和需求。

## What Changes

- **修复输入框禁用问题**：解决 WebSocket 连接失败导致的输入框被禁用的 Bug。
- **精简聊天界面 UI**：从 `Chat.vue` 中移除顶部的关系阶段（相识等）和亲密度进度条。
- **调整 WebSocket 代理配置**：确保 Vite 开发服务器能正确代理 `/api/chat` 的 WebSocket 连接。

## Capabilities

### New Capabilities
- 无

### Modified Capabilities
- `chat-interaction`: 修复连接稳定性。
- `web-frontend`: 调整聊天界面布局，移除进度条显示。

## Impact

- `frontend/vite.config.js`: 更新代理配置以支持 WebSocket。
- `frontend/src/views/Chat.vue`: 移除顶部的关系信息头部组件。
- `frontend/src/composables/useWebSocket.js`: 优化连接逻辑（如有必要）。
