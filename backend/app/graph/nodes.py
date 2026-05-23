from app.characters.engine import get_template, build_system_prompt
from app.relationship.engine import get_stage_info, calculate_intimacy_change, get_stage_for_intimacy
from app.knowledge.retriever import retrieve_context
from app.memory.vector_store import add_memory
from app.graph.state import RelationshipState


async def input_gate(state: RelationshipState) -> dict:
    """Analyze user input for emotion and intent."""
    user_msg = state.get("current_input", "")
    emotion = "中性"

    # Simple emotion detection
    positive_words = ["开心", "高兴", "快乐", "幸福", "喜欢", "爱", "好开心",
                      "哈哈", "嘻嘻", "太好了", "感动", "谢谢"]
    negative_words = ["难过", "伤心", "哭", "烦", "累", "讨厌", "生气",
                      "痛苦", "失望", "焦虑", "压力", "不开心"]
    angry_words = ["滚", "烦死了", "气死", "愤怒", "受不了"]

    for w in angry_words:
        if w in user_msg:
            emotion = "生气"
            break
    else:
        for w in negative_words:
            if w in user_msg:
                emotion = "低落"
                break
        else:
            for w in positive_words:
                if w in user_msg:
                    emotion = "开心"
                    break

    # Calculate intimacy change
    intimacy_change = calculate_intimacy_change(emotion, user_msg)
    new_score = max(0.0, min(1.0, state.get("intimacy_score", 0.0) + intimacy_change))
    new_stage = get_stage_for_intimacy(new_score)
    stage_info = get_stage_info(new_stage)

    return {
        "user_emotion": emotion,
        "intimacy_score": new_score,
        "relationship_stage": new_stage,
        "stage_name": stage_info["name"],
        "stage_description": stage_info["description"],
    }


async def memory_retrieval(state: RelationshipState) -> dict:
    """Retrieve relevant memories and knowledge."""
    query = state.get("current_input", "")
    user_id = state.get("user_id", 0)

    context = await retrieve_context(user_id, query)
    return {
        "retrieved_memories": context["memories"],
        "user_knowledge": context["user_knowledge"],
        "character_knowledge": context["character_knowledge"],
    }


async def prompt_assembly(state: RelationshipState) -> dict:
    """Build the system prompt with character, stage, and context."""
    personality = state.get("personality", "文静")
    
    # DEBUG: print raw personality to see what's happening
    print(f"[DEBUG] Raw personality in prompt_assembly: {personality}")
    
    # Defensive mapping for common encoding issues
    templates_mapping = {
        # female
        "文静": "female_quiet",
        "治愈": "female_healing",
        "傲娇": "female_tsundere",
        # male
        "阳光": "male_sunny",
        "风趣": "male_funny",
        "暖男": "male_warm",
    }
    
    # Handle known garbled versions or default
    template_id = templates_mapping.get(personality)
    if not template_id:
        # If personality contains specific garbled patterns or is missing, default to female_quiet
        print(f"[DEBUG] Personality '{personality}' not found in mapping, defaulting to female_quiet")
        template_id = "female_quiet"
        
    template = get_template(template_id)

    if template is None:
        print(f"[ERROR] Template {template_id} NOT FOUND in JSON files!")
        return {"system_prompt": "You are a gentle and quiet female AI companion named 灵儿."}

    prompt = build_system_prompt(
        template=template,
        stage_name=state.get("stage_name") or "相识",
        stage_description=state.get("stage_description", ""),
        custom_name=state.get("custom_name"),
        memories=state.get("retrieved_memories", ""),
        user_knowledge=state.get("user_knowledge", ""),
        character_knowledge=state.get("character_knowledge", ""),
    )

    return {"system_prompt": prompt}


async def llm_call(state: RelationshipState) -> dict:
    """Call the LLM to generate a response."""
    from app.services.deepseek import chat_completion

    system_prompt = state.get("system_prompt", "")
    messages = state.get("messages", [])

    print(f"\n[DEBUG] System Prompt:\n{system_prompt}\n")
    print(f"[DEBUG] Personality from state: {state.get('personality')}")

    # Convert messages to API format
    api_messages = []
    for msg in messages[-10:]:  # Last 10 turns
        # Messages from sliding window are dictionaries
        if isinstance(msg, dict) and "role" in msg and "content" in msg:
            api_messages.append({"role": msg["role"], "content": msg["content"]})

    # Add current input if not already in history (though it usually is)
    current_input = state.get("current_input", "")
    if not api_messages or api_messages[-1]["content"] != current_input:
        api_messages.append({"role": "user", "content": current_input})

    response = await chat_completion(system_prompt, api_messages)
    return {"response": response}


async def post_processing(state: RelationshipState) -> dict:
    """Save memories and update state after LLM response."""
    user_id = state.get("user_id", 0)
    user_msg = state.get("current_input", "")
    ai_response = state.get("response", "")

    # Store important user information as memory
    important_topics = ["喜欢", "最爱", "讨厌", "害怕", "梦想", "生日", "名字"]
    if any(kw in user_msg for kw in important_topics):
        add_memory(user_id, user_msg, {"type": "user_info", "emotion": state.get("user_emotion", "")})

    # Store AI response as memory for future reference
    if ai_response and len(ai_response) > 20:
        add_memory(user_id, f"AI: {ai_response[:200]}", {"type": "conversation", "role": "ai"})

    return {}
