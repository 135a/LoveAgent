## ADDED Requirements

### Requirement: 用户注册
The system SHALL 允许新用户通过用户名和密码注册。

#### Scenario: 注册成功
- **WHEN** 用户提交未重复的用户名和有效密码（6 位以上）
- **THEN** 系统创建用户，密码以 bcrypt 哈希存储，返回成功消息

#### Scenario: 用户名已存在
- **WHEN** 用户提交的用户名已存在
- **THEN** 系统返回 409 错误："用户名已被注册"

#### Scenario: 密码强度不足
- **WHEN** 用户提交的密码少于 6 位
- **THEN** 系统返回 400 错误："密码至少需要 6 位"

### Requirement: 用户登录
The system SHALL 允许已注册用户通过用户名和密码登录，返回 JWT token。

#### Scenario: 登录成功
- **WHEN** 用户提交正确的用户名和密码
- **THEN** 系统返回 JWT access token（有效期 24 小时）

#### Scenario: 登录失败
- **WHEN** 用户提交错误的用户名或密码
- **THEN** 系统返回 401 错误："用户名或密码错误"

### Requirement: JWT 鉴权
The system SHALL 在需要身份认证的接口验证 JWT token。

#### Scenario: 带 token 访问
- **WHEN** 用户携带有效 JWT token 访问受保护接口
- **THEN** 系统解析 token 获取 user_id，正常处理请求

#### Scenario: 无 token 访问
- **WHEN** 用户未携带 token 访问受保护接口
- **THEN** 系统返回 401 错误："未授权"

#### Scenario: token 过期
- **WHEN** 用户携带已过期的 token 访问接口
- **THEN** 系统返回 401 错误："token 已过期，请重新登录"
