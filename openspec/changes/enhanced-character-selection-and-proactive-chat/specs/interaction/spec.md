## ADDED Requirements

### Requirement: 异步主动消息
系统 SHALL 在用户处于 WebSocket 连接中但长时间不发言时，主动发起消息。

#### Scenario: 用户沉默超时
- **WHEN** 用户已发送消息且 AI 已回复，之后用户超过 30 秒未继续输入
- **THEN** 系统自动触发 AI 生成一段基于当前语境的主动消息（如关心或新话题）

## MODIFIED Requirements

### Requirement: 角色切换
系统 SHALL 允许已拥有角色的用户重新进入角色选择页面进行新角色创建。

#### Scenario: 手动切换入口
- **WHEN** 用户从聊天页点击“切换恋人”
- **THEN** 跳转到选角页，页面不再自动重定向回聊天页，用户可以重新选择性别和性格
