from pydantic import BaseModel


class CharacterTemplate(BaseModel):
    """角色预设模板的数据模型，对应 templates/ 下的每个 JSON 文件"""

    id: str  # 模板唯一标识，如 "female_quiet"
    gender: str  # 性别：female（女生）/ male（男生）
    personality: str  # 性格变体：文静、治愈、傲娇、阳光、风趣、暖男
    name: str  # 角色默认名字，如 "小雅"
    description: str  # 简短描述，展示在角色选择卡片上
    traits: list[str]  # 性格特质列表，如 ["安静", "细腻", "慢热"]
    speaking_style: str  # 说话风格描述，用于辅助生成对话
    system_prompt_template: str  # System Prompt 模板，用 {} 做占位符
