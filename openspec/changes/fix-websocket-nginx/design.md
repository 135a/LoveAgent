## Context

前端通过 `ws://host/api/chat` 发起连接。Nginx 当前的 `/api` 配置仅支持 HTTP。当 WebSocket 握手请求（带有 `Upgrade: websocket`）到达 Nginx 时，Nginx 如果不显式设置转发这些头信息，后端将无法识别这是一个升级请求，从而导致连接失败。

## Goals / Non-Goals

**Goals:**
- 在 `nginx.conf` 的 `/api` 块中添加 WebSocket 支持。
- 确保握手成功，使前端能够接收到 `connected` 消息。

**Non-Goals:**
- 不修改前后端代码逻辑。

## Decisions

| Decision | Choice | Rationale | Alternatives |
|----------|--------|-----------|--------------|
| 配置位置 | 修改 `/api` block | 前端目前硬编码使用 `/api/chat`。修改 `/api` 块可以兼容 HTTP 和 WS。 | 将前端路径改为 `/ws/chat` (需要改代码) |
| 协议头设置 | `Upgrade $http_upgrade` | 允许 Nginx 转发客户端发起的协议升级请求。 | 无 |

## Risks / Trade-offs

- **[Risk]** 某些 Nginx 版本对混用 HTTP 和 WS 的 location 支持不佳 → **Mitigation**: 使用标准的 `proxy_set_header Upgrade` 方案，这是 Nginx 官方推荐的通用做法。
