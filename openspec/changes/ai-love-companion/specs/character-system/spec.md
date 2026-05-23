## ADDED Requirements

### Requirement: 性别选择
The system SHALL 让用户选择 AI 伴侣的性别，可选"女生"或"男生"。

#### Scenario: 选择女生
- **WHEN** 用户选择"女生"
- **THEN** 系统加载女生角色模板（慢热害羞型基础人格）

#### Scenario: 选择男生
- **WHEN** 用户选择"男生"
- **THEN** 系统加载男生角色模板（活泼幽默型基础人格）

### Requirement: 性格变体
The system SHALL 提供性格变体选择，每个性别至少 3 种变体。

#### Scenario: 女生变体
- **WHEN** 用户选择女生后
- **THEN** 展示"文静型"、"治愈型"、"傲娇型"三个变体供选择

#### Scenario: 男生变体
- **WHEN** 用户选择男生后
- **THEN** 展示"阳光型"、"风趣型"、"暖男型"三个变体供选择

### Requirement: 角色一致性
The system SHALL 确保 AI 角色在对话中保持人格一致性，不崩坏人设。

#### Scenario: 长期对话不崩坏
- **WHEN** 用户连续对话 50 轮
- **THEN** 角色始终表现出设定的人格特质和说话风格

### Requirement: 自定义称呼
The system SHALL 允许用户给 AI 伴侣自定义称呼。

#### Scenario: 修改称呼
- **WHEN** 用户在设置中修改称呼
- **THEN** 后续对话中角色使用新称呼

### Requirement: 角色实例隔离
The system SHALL 确保每个用户的角色实例（关系、记忆、对话）完全隔离。

#### Scenario: 多用户数据隔离
- **WHEN** 用户 A 和用户 B 都选择了女生角色
- **THEN** 两人各自拥有独立的角色实例，互不干扰，AI 回复内容基于各自的关系阶段和记忆
