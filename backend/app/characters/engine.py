import json  # JSON 文件读写
import os  # 文件和路径操作
from pathlib import Path  # 跨平台路径处理
from typing import Optional  # 可选类型注解

from app.characters.base import CharacterTemplate  # 角色模板数据模型


# 模板 JSON 文件的存放目录：characters/templates/
TEMPLATES_DIR = Path(__file__).parent / "templates"

# 全局缓存，避免每次调用都重新读取 JSON 文件
_templates: Optional[dict[str, CharacterTemplate]] = None


def _load_all_templates() -> dict[str, CharacterTemplate]:
    """加载所有角色模板 JSON 文件到缓存中"""
    global _templates
    if _templates is not None:  # 缓存命中，直接返回
        return _templates
    _templates = {}  # 初始化缓存
    for f in TEMPLATES_DIR.glob("*.json"):  # 遍历 templates 目录下所有 .json 文件
        with open(f, encoding="utf-8") as fp:
            data = json.load(fp)  # 解析 JSON
        _templates[data["id"]] = CharacterTemplate(**data)  # 转为数据模型，以 id 为 key
    return _templates


def get_template(template_id: str) -> Optional[CharacterTemplate]:
    """按模板 ID 获取单个角色模板，不存在返回 None"""
    return _load_all_templates().get(template_id)


def list_templates(gender: Optional[str] = None) -> list[CharacterTemplate]:
    """列出全部角色模板，可选按性别筛选（female / male）"""
    templates = list(_load_all_templates().values())  # 所有模板
    if gender:
        templates = [t for t in templates if t.gender == gender]  # 按性别过滤
    return templates


def build_system_prompt(
    template: CharacterTemplate,  # 选中的角色模板
    stage_name: str,  # 当前关系阶段名称，如"朋友"、"暧昧"
    stage_description: str,  # 当前关系阶段的风格描述
    custom_name: Optional[str] = None,  # 用户给角色起的自定义称呼，可选
    memories: str = "",  # 检索到的历史记忆文本
    user_knowledge: str = "",  # 用户相关的知识库内容
    character_knowledge: str = "",  # 角色相关的知识库内容（背景故事、兴趣等）
) -> str:
    """根据模板和各维度数据，生成最终发给 LLM 的 System Prompt"""
    name = custom_name or template.name  # 优先使用用户自定义称呼，否则用默认名字
    
    # 格式化知识块，增加明确的边界和身份标识
    formatted_memories = f"### 最近对话记忆 (注意区分 AI 和用户的身份):\n{memories}" if memories else "暂无记忆"
    formatted_user_info = f"### 关于【当前用户】已知的信息 (这是对方的情况，不是你的):\n{user_knowledge}" if user_knowledge else "暂无用户信息"
    formatted_char_info = f"### 关于【你自己({name})】的设定背景 (这是你的真实情况，请务必遵守):\n{character_knowledge}" if character_knowledge else "暂无你的设定"

    return template.system_prompt_template.format(
        name=name,  # 角色名字
        personality=template.personality,  # 性格变体
        core_traits="、".join(template.traits),  # 性格特质，顿号连接，如"安静、细腻、慢热"
        speaking_style=template.speaking_style,  # 说话风格
        stage_name=stage_name,  # 当前关系阶段
        stage_description=stage_description,  # 阶段描述
        memories=formatted_memories,  # 格式化后的历史记忆
        user_knowledge=formatted_user_info,  # 格式化后的用户知识
        character_knowledge=formatted_char_info,  # 格式化后的角色知识
    )
