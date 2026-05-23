## ADDED Requirements

### Requirement: 6 阶段关系体系
The system SHALL 实现 6 阶段关系进化：陌生人(0) → 相识(1) → 朋友(2) → 暧昧(3) → 恋爱中(4) → 亲密关系(5)。

#### Scenario: 初始状态
- **WHEN** 用户首次创建角色实例
- **THEN** 关系阶段为"陌生人"，亲密度为 0.0

#### Scenario: 阶段递进
- **WHEN** 亲密度达到阶段转换阈值（0.10/0.30/0.50/0.70/0.90）
- **THEN** 关系阶段自动升级，角色 Prompt 切换为对应风格

### Requirement: 亲密度计算
The system SHALL 根据用户互动动态计算亲密度（0.0 ~ 1.0）。

#### Scenario: 积极互动加分
- **WHEN** 用户主动关心、分享、积极回应
- **THEN** 亲密度 +0.01~0.05

#### Scenario: 深度交流加分
- **WHEN** 用户进行情感或人生等深度话题交流
- **THEN** 亲密度 +0.03~0.08

#### Scenario: 负面互动扣分
- **WHEN** 用户负面情绪攻击或恶意输入
- **THEN** 亲密度 -0.02~0.10

#### Scenario: 日常衰减
- **WHEN** 用户超过 24 小时未对话
- **THEN** 亲密度每日衰减 0.001

### Requirement: 阶段影响对话风格
The system SHALL 根据关系阶段调整 AI 的说话语气和内容。

#### Scenario: 陌生人回复
- **WHEN** 关系阶段为"陌生人"
- **THEN** AI 回复简短客气，不主动提问

#### Scenario: 恋爱中回复
- **WHEN** 关系阶段为"恋爱中"
- **THEN** AI 回复亲密，使用昵称，主动表达关心

### Requirement: 关系状态持久化
The system SHALL 将关系阶段和亲密度持久化到 MySQL。

#### Scenario: 重启恢复
- **WHEN** 系统重启后
- **THEN** 用户的关系阶段和亲密度从 MySQL 恢复
