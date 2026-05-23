## Context

当前后端在用户注册和向量数据库初始化方面存在严重 Bug。密码哈希依赖的库过旧导致崩溃，且无法支持长密码。ChromaDB 的集合自动创建逻辑因捕获异常类型错误而失效。

## Goals / Non-Goals

**Goals:**
- 实现兼容最新环境、且无长度限制的密码哈希系统。
- 确保 ChromaDB 集合在不存在时能自动、可靠地创建。
- 清理冗余的密码处理库依赖。

**Non-Goals:**
- 不涉及数据库表结构变更。
- 不修改 JWT 生成和验证流程（仅修改哈希存储和比对）。

## Decisions

| Decision | Choice | Rationale | Alternatives |
|----------|--------|-----------|--------------|
| 哈希库选择 | 原生 `bcrypt` | `passlib` 已停止更新且与新版 `bcrypt` 不兼容。直接使用原生库最稳定。 | 继续修补 `passlib` (极其困难且不稳) |
| 处理长密码限制 | SHA-256 预哈希 | `bcrypt` 限制输入为 72 字节。先计算 SHA-256 hex (64 字符) 可确保输入恒定且不丢熵。 | 截断密码 (安全性差); 改用 Argon2 (依赖更重) |
| ChromaDB 异常捕获 | 捕获 `chromadb.errors.InvalidCollectionException` | ChromaDB 5.x 在 `get_collection` 失败时抛出此特定异常，而非旧版的 `ValueError`。 | 捕获所有异常 (颗粒度太粗) |

## Risks / Trade-offs

- **[Risk]** 预哈希导致旧哈希失效 → **Mitigation**: 当前系统无用户数据，可直接切换。若未来有用户，需实现双重校验逻辑。
- **[Risk]** 环境变量配置错误 → **Mitigation**: 保持现有环境变量名不变，仅修改内部逻辑。
