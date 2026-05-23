## 1. 基础连接修复

- [x] 1.1 修改 `frontend/vite.config.js`，在 `/api` 代理中添加 `ws: true`。
- [x] 1.2 重启前端开发服务器以生效配置。

## 2. 界面精简

- [x] 2.1 修改 `frontend/src/views/Chat.vue`，删除顶部的 `.header` 节点及其内容。
- [x] 2.2 清理 `Chat.vue` 中不再需要的 `currentStage`、`intimacyPercent`、`intimacyColor` 等计算属性。
- [x] 2.3 调整 CSS，确保移除头部后聊天区域高度布局正确（如调整 `.messages` 的高度或布局方式）。

## 3. 验证

- [x] 3.1 验证进入聊天页面后，WebSocket 连接成功建立，输入框变为可用状态。
- [x] 3.2 验证顶部进度条和关系标签已消失。
- [x] 3.3 进行一轮对话，确保消息收发正常。
