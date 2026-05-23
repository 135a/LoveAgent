## ADDED Requirements

### Requirement: 鲁棒的向量集合管理
系统 SHALL 确保在访问 ChromaDB 集合时，如果集合不存在，应自动创建，且必须能正确处理 ChromaDB 5.x 抛出的异常。

#### Scenario: 首次启动初始化
- **WHEN** ChromaDB 为空且后端尝试加载全局角色知识
- **THEN** 系统捕获集合不存在的异常，自动创建 `global_character` 集合并继续加载

#### Scenario: 新用户首次对话
- **WHEN** 一个新用户首次发送消息，系统尝试访问其私有记忆集合
- **THEN** 系统自动创建 `user_{id}_memory` 集合，确保对话不中断
