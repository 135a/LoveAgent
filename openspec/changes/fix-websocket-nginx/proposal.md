## Why

由于 Nginx 配置中 `/api` 路径缺少 WebSocket 升级协议头，导致前端无法与后端建立实时通信连接。这直接导致聊天界面的输入框因检测不到连接而处于禁用状态。

## What Changes

- 修改 `frontend/nginx.conf`，为 `/api` 路径增加 `Upgrade` 和 `Connection` 协议头支持。
- 确保所有通过 `/api` 路径的 WebSocket 请求都能正确转发到后端。

## Capabilities

### New Capabilities
- 无

### Modified Capabilities
- `chat-interaction`: 增强连接稳定性，支持生产/Docker 环境下的 WebSocket 转发。

## Impact

- `frontend/nginx.conf`: Nginx 代理配置变更。
