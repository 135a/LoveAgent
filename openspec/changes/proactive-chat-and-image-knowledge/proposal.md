## Why

1. **对话单调**：当前 AI 仅被动回答问题，缺乏真实伴侣的主动性和互动感。
2. **多媒体知识缺失**：知识库中的图片（聊天记录截图）无法被纯文本模型识别，导致 AI 丢失了关键背景。
3. **UI 部署同步问题**：之前的退出登录和切换按钮由于 Docker 镜像未重建，在前端未生效。

## What Changes

- **增强主动性**：更新系统提示词模板，要求 AI 根据语境主动开启话题、分享感受或提问。
- **图像知识提取**：通过 OCR 或人工转录将 `interests.md` 中的图片内容转为文本，并注入知识库。
- **UI 彻底生效**：强制重建前端镜像以更新 UI 界面。
- **优化对话流**：微调 LangGraph 逻辑，使回复更具连贯性。

## Capabilities

### New Capabilities
- `conversational-proactivity`: AI 具备主动发起话题和深化交流的能力。
- `multimodal-knowledge-ingestion`: 能够将图片信息转化为文本知识进行检索。

### Modified Capabilities
- `web-frontend`: 确保新增的控制按钮（登出、切换）可见并可用。

## Impact

- `backend/app/characters/templates/*.json`: 提示词模板更新。
- `knowledge/character/female/interests.md`: 内容丰富化。
- `docker-compose.yml`: 部署配置微调。
- `frontend/src/views/Chat.vue`: 确保 UI 渲染逻辑无误。
