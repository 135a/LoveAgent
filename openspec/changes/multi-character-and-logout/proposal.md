## Why

目前一个用户只能绑定一个 AI 恋人，且所有性格共用一套记忆，这不符合“不同恋人不同体验”的需求。同时，界面缺少“退出登录”和“切换角色”的便捷入口，导致用户体验受阻。

## What Changes

- **支持多恋人共存**：修改数据库，允许一个用户拥有多个性格角色的独立实例，互不覆盖。
- **记忆物理隔离**：在向量数据库（ChromaDB）中按“用户+性格”进行分区存储，确保不同角色的对话记忆完全独立。
- **新增交互控件**：在聊天界面增加退出登录和返回选角页面的功能。
- **活跃状态管理**：后端自动追踪用户当前正在与哪位恋人聊天。

## Capabilities

### New Capabilities
- `multi-lover-support`: 支持多角色实例管理及活跃切换。
- `isolated-personality-memory`: 实现性格级别的向量记忆隔离。

### Modified Capabilities
- `user-auth`: 增加登出功能支持。
- `chat-interaction`: 对话加载逻辑适配多角色隔离。

## Impact

- `backend/app/models/__init__.py`: 模型结构变更。
- `backend/app/routes/characters.py`: 选角逻辑由“覆盖”改为“切换/新增”。
- `backend/app/memory/vector_store.py`: 集合命名逻辑调整。
- `frontend/src/views/Chat.vue`: 界面布局及导航逻辑更新。
