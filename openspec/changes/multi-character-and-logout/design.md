## Context
目前 `UserCharacter` 与 `User` 是 1:1 关系，限制了多角色体验。且向量存储以 `user_id` 为唯一维度，导致记忆混杂。

## Goals
- 实现恋人实例的多样化并存。
- 确保记忆数据的绝对隔离。
- 提供流畅的切换和登出体验。

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| 数据库约束 | 移除 `UserCharacter.user_id` 的 Unique | 一个用户需要能够关联多条性格记录。 |
| 活跃追踪 | 在 `UserCharacter` 增加 `is_active` | 不需要前端传递 ID，后端根据 Token 自动识别当前聊天的对象，简化前端逻辑。 |
| 记忆键名 | `user_{id}_{personality_id}_memory` | 引入性格 ID (如 `female_quiet`) 确保物理层面的隔离。 |
| 对话绑定 | 在 `Conversation` 增加 `character_id` | 确保历史记录加载时不会张冠李戴。 |

## Risks / Trade-offs
- **[Risk]** 旧数据不兼容 -> **Mitigation**: 由于是早期开发阶段，执行 `docker-compose down -v` 重置数据库是最稳妥的。
