##  task
- [x] 1.1 手动或借助工具转录 `knowledge/character/female/interests.md` 中的所有图片文字。
- [x] 1.2 将转录后的文字以“历史聊天记录”的形式追加到 `interests.md` 中。
- [x] 1.3 触发后端知识库重载。

## 2. 角色主动性增强

- [x] 2.1 修改 `backend/app/characters/templates/` 目录下的所有 JSON 模板，在 `system_prompt_template` 中加入关于主动性的具体指令。
- [x] 2.2 特别针对“文静”等角色，平衡主动性与性格人设。

## 3. UI 部署与同步

- [x] 3.1 运行 `docker-compose build frontend` 重新构建前端。
- [x] 3.2 运行 `docker-compose up -d frontend` 重启并确认按钮可见。

## 4. 验证

- [ ] 4.1 测试 AI 是否能主动分享感受。
- [ ] 4.2 测试 AI 是否知道图片中的聊天细节。
