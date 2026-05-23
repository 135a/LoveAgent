## MODIFIED Requirements

### Requirement: WebSocket 实时通信
The system SHALL 通过 WebSocket 实现实时消息传输。在 Docker/Nginx 环境下，`/api` 路径必须支持协议升级（Upgrade Header），以确保连接能到达后端。

#### Scenario: Docker 环境下的连接
- **WHEN** 客户端通过 Nginx 代理发起 `ws://host/api/chat` 连接
- **THEN** Nginx 成功转发 Upgrade 头信息，后端返回 `connected` 消息，前端输入框变为可用。
