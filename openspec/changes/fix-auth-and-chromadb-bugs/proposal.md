## Why

当前系统的注册功能因 `passlib` 与新版 `bcrypt` 不兼容而崩溃（500 错误），且 `bcrypt` 存在 72 字节密码长度限制。同时，ChromaDB 在集合不存在时抛出的异常未被正确捕获，导致知识库初始化失败。

## What Changes

- 移除老旧的 `passlib` 依赖，改用原生的 `bcrypt` 库进行密码哈希。
- 引入 SHA-256 预哈希机制，解决 `bcrypt` 的 72 字节输入限制，确保支持任意长度密码。
- 修复 `vector_store.py` 中的 ChromaDB 异常捕获逻辑，确保集合不存在时能正确创建。
- 更新 `pyproject.toml` 以匹配新的依赖关系。

## Capabilities

### New Capabilities
- `robust-auth-hashing`: 现代、稳定的密码哈希方案，支持长密码且无库版本兼容性问题。

### Modified Capabilities
- `knowledge-base`: 提高知识库初始化和集合管理的可靠性。

## Impact

- `backend/app/middleware/jwt.py`: 更改哈希和校验逻辑。
- `backend/app/routes/auth.py`: 配合哈希逻辑调整。
- `backend/app/memory/vector_store.py`: 修正异常捕获。
- `backend/pyproject.toml`: 依赖项变更。
