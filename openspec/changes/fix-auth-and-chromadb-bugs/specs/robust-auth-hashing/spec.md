## ADDED Requirements

### Requirement: 安全且兼容的密码哈希
系统 SHALL 直接使用 `bcrypt` 库进行密码哈希和校验，不依赖中间层框架（如 passlib），以避免库版本冲突。

#### Scenario: 注册哈希
- **WHEN** 用户提交注册请求
- **THEN** 系统使用 `bcrypt.hashpw` 生成哈希值并存储

#### Scenario: 登录校验
- **WHEN** 用户提交登录请求
- **THEN** 系统从数据库读取哈希值，并使用 `bcrypt.checkpw` 进行匹配校验

### Requirement: 解决 72 字节长度限制
系统 SHALL 在使用 `bcrypt` 哈希之前，先对原始密码进行 SHA-256 预哈希。

#### Scenario: 长密码注册
- **WHEN** 用户注册时输入超过 72 字节的超长密码
- **THEN** 系统先将其转为 SHA-256 hex 字符串（64 字节），再喂给 `bcrypt` 处理，确保注册成功且不丢失熵。

#### Scenario: 短密码注册
- **WHEN** 用户注册时输入普通短密码
- **THEN** 同样经过 SHA-256 处理后哈希，流程保持一致。
