## Context
当前的对话模式是严格的 Request-Response，这削弱了 AI 伴侣的真实感。同时，前端对选角页的强制重定向逻辑阻止了用户创建多角色。

## Goals
- 允许通过参数绕过重定向逻辑。
- 实现非阻塞的 WebSocket 并发任务监听。
- 引导 LLM 在无用户输入的情况下生成自然回复。

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| 重定向控制 | `?action=switch` | 简单高效，无需修改复杂的 Vue Router 守卫，直接在组件内部判断。 |
| 并发逻辑 | `asyncio.wait(timeout)` | 在单个协程循环内实现超时监听，代码复杂度低，且能直接访问 WebSocket 对象。 |
| 触发信号 | `[SYSTEM_PROACTIVE_TRIGGER]` | 作为特殊的内部输入，方便在 `prompt_assembly` 节点中拦截并替换为专用的 System 指令。 |

## Risks / Trade-offs
- **[Risk]** 超时时间太短导致 AI 刷屏 -> **Mitigation**: 初步设定为 45 秒，且规定必须在最后一条消息是 AI 发出的情况下才触发系统主动。
