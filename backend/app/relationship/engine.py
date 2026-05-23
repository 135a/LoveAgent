STAGE_CONFIG = [
    {"level": 0, "name": "陌生人", "threshold": 0.0,
     "description": "初次见面，礼貌而疏离，话不多，保持距离感。"},
    {"level": 1, "name": "相识", "threshold": 0.10,
     "description": "开始熟悉，会主动找话题，偶尔分享日常。"},
    {"level": 2, "name": "朋友", "threshold": 0.30,
     "description": "语气变得轻松自然，会开小玩笑，开始关心对方。"},
    {"level": 3, "name": "暧昧", "threshold": 0.50,
     "description": "关系微妙起来，会暗示好感，分享更私密的想法。"},
    {"level": 4, "name": "恋爱中", "threshold": 0.70,
     "description": "正式确立关系，亲密称呼，主动表达想念和关心。"},
    {"level": 5, "name": "亲密关系", "threshold": 0.90,
     "description": "深度信任和默契，几乎无话不谈，感情非常稳定。"},
]


def get_stage_info(stage: int) -> dict:

    """
    根据关卡数获取对应的关卡配置信息

    参数:
        stage: int - 关卡编号

    返回:
        dict - 关卡配置信息字典

    注意:
        如果输入的stage小于0，则自动设置为0
        如果输入的stage大于最大关卡数，则自动设置为最大关卡数
    """
    if stage < 0:  # 如果stage小于0，则将其设置为0，防止越界
        stage = 0
    if stage >= len(STAGE_CONFIG):  # 如果stage大于等于关卡配置列表长度，则将其设置为最大有效索引
        stage = len(STAGE_CONFIG) - 1
    return STAGE_CONFIG[stage]  # 返回对应关卡的配置信息


def calculate_intimacy_change(emotion: str, user_message: str) -> float:
    """Calculate intimacy change based on emotion and message content."""
    # Positive interactions
    positive_keywords = ["谢谢", "喜欢", "开心", "想你", "真好", "在一起",
                         "感动", "幸福", "快乐", "美好", "赞", "棒", "好呀"]
    deep_keywords = ["人生", "梦想", "难过", "孤独", "害怕", "过去",
                     "家庭", "秘密", "感受", "心里", "为什么"]

    msg_lower = user_message.lower()
    change = 0.0

    # Emotion-based adjustment
    if emotion in ("开心", "兴奋", "感动"):
        change += 0.02
    elif emotion in ("低落", "难过", "伤心"):
        change += 0.01  # sharing vulnerability builds intimacy
    elif emotion in ("生气", "愤怒"):
        change -= 0.03

    # Content-based adjustment
    has_positive = any(kw in msg_lower for kw in positive_keywords)
    has_deep = any(kw in msg_lower for kw in deep_keywords)

    if has_positive:
        change += 0.02
    if has_deep:
        change += 0.04
    if len(user_message) > 100:
        change += 0.01  # longer messages indicate engagement

    # Clamp
    return max(-0.10, min(0.08, change))


def apply_daily_decay(last_active_days: float, current_score: float) -> float:
    """Apply daily intimacy decay."""
    decay = last_active_days * 0.001
    return max(0.0, current_score - decay)


def get_stage_for_intimacy(score: float) -> int:
    """Determine stage based on intimacy score."""
    for stage in reversed(STAGE_CONFIG):
        if score >= stage["threshold"]:
            return stage["level"]
    return 0
