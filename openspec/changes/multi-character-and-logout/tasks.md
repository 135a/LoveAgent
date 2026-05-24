## 1. 数据库模型重构

- [x] 1.1 修改 `backend/app/models/__init__.py`：移除 `UserCharacter.user_id` 的 `unique=True`，添加 `is_active` 布尔字段。
- [x] 1.2 在 `Conversation` 模型中添加 `character_id` 外键。
- [x] 1.3 更新 `User` 模型中的 `character` 关系，改为 1:N 关系（`characters`）。

## 2. 后端逻辑适配

- [x] 2.1 修改 `backend/app/routes/characters.py`：重构 `choose_character` 逻辑，支持状态切换和新实例创建。
- [x] 2.2 修改 `backend/app/routes/characters.py`：更新 `get_my_character` 只返回 `is_active=True` 的记录。
- [x] 2.3 修改 `backend/app/memory/vector_store.py`：更新 `_user_collection_name`，接受 `personality` 参数实现分区。
- [x] 2.4 修改 `backend/app/routes/chat.py`：在加载历史记录和创建新会话时，强制使用当前活跃角色的 ID。
- [x] 2.5 更新 `backend/app/knowledge/retriever.py`：适配新的向量集合命名规则。

## 3. 前端 UI 增强

- [x] 3.1 修改 `frontend/src/views/Chat.vue`：在界面顶部或适当位置添加“切换恋人”和“退出登录”按钮。
- [x] 3.2 在 `Chat.vue` 中实现登出逻辑（清除 Token，跳转登录页）。
- [x] 3.3 在 `Chat.vue` 中实现切换逻辑（跳转角色页）。

## 4. 验证与重置

- [x] 4.1 执行环境彻底重置（`docker-compose down -v`）以应用新模型。
- [ ] 4.2 手动测试：创建两个不同性格伴侣，验证记忆是否隔离。
