## MODIFIED Requirements

### Requirement: WebSocket 实时通信
The system SHALL 通过 WebSocket 实现实时消息传输，支持流式打字机效果。必须确保开发环境下 WebSocket 连接能够通过 Vite 代理正确到达后端。

#### Scenario: 建立连接
- **WHEN** 用户进入聊天界面
- **THEN** 前端建立 WebSocket 连接（带 JWT token 认证），且在开发环境下通过 Vite 代理转发
