## Context

当前聊天界面存在功能性 Bug（无法输入文字）和体验性问题（进度条干扰）。经分析，输入受限是由于 WebSocket 连接未成功建立，导致输入框处于禁用状态。同时，用户明确要求移除顶部的关系进度条。

## Goals / Non-Goals

**Goals:**
- 修复 WebSocket 连接，恢复聊天功能。
- 移除前端 `Chat.vue` 中的关系阶段和亲密度进度条 UI。
- 保持后端关系逻辑不变，仅调整前端展示。

**Non-Goals:**
- 不涉及后端 `chat.py` 逻辑修改。
- 不移除数据库中的关系数据。

## Decisions

| Decision | Choice | Rationale | Alternatives |
|----------|--------|-----------|--------------|
| WebSocket 代理 | 在 Vite 中为 `/api` 开启 `ws: true` | 后端 WS 路由在 `/api/chat`。通过在现有 `/api` 代理中开启 `ws` 支持，可以最精简地解决跨域和连接问题。 | 更改后端 WS 路由到 `/ws` (需要改代码，成本更高) |
| UI 移除方式 | 直接从 `Chat.vue` 模板中删除相关 DOM | 用户明确不再需要这些展示。直接删除是最彻底的精简方式。 | 使用 `v-if` 隐藏 (没必要，代码会变冗余) |
| 输入框状态管理 | 保持现有的 `disabled` 逻辑 | 该逻辑本身是正确的（未连接不许输入），修复连接后该状态会自动恢复正常。 | 强制取消 `disabled` (会导致发送失败，用户体验更差) |

## Risks / Trade-offs

- **[Risk]** 移除进度条后用户无法直观看到关系变化 → **Mitigation**: 维持后端逻辑，AI 的对话语气依然会随关系改变。
- **[Risk]** 代理配置冲突 → **Mitigation**: 优先测试 `ws: true` 是否影响正常的 HTTP API。
