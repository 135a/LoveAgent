## 1. Nginx 配置修复

- [x] 1.1 修改 `frontend/nginx.conf`，在 `location /api` 块中添加 WebSocket 升级头信息。

## 2. 部署与验证

- [x] 2.1 重启前端 Nginx 容器以加载新配置。
- [x] 2.2 验证聊天界面输入框已解锁，且消息收发正常。
