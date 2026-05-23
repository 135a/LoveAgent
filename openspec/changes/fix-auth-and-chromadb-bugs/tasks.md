## 1. 依赖清理与更新

- [x] 1.1 修改 `backend/pyproject.toml`，移除 `passlib` 及其 bcrypt 额外项，添加 `bcrypt` 依赖。
- [x] 1.2 在后端容器或开发环境更新依赖。

## 2. 密码哈希重构

- [x] 2.1 修改 `backend/app/middleware/jwt.py`，移除 `passlib` 相关代码。
- [x] 2.2 在 `jwt.py` 中实现基于 SHA-256 + `bcrypt` 的 `hash_password` 函数。
- [x] 2.3 在 `jwt.py` 中实现对应的 `verify_password` 校验函数。

## 3. 向量存储鲁棒性修复

- [x] 3.1 修改 `backend/app/memory/vector_store.py`，引入 `chromadb.errors` 中的异常定义。
- [x] 3.2 更新 `get_or_create_collection` 和 `get_global_collection` 函数，捕获正确的集合缺失异常。

## 4. 验证与测试

- [x] 4.1 编写测试脚本验证长密码（>72 字节）的哈希与登录逻辑。
- [x] 4.2 验证应用启动时自动创建 `global_character` 集合的功能。
- [x] 4.3 手动测试注册和登录全流程，确保修复有效。
