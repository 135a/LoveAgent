from app.memory.vector_store import (
    search_memories,
    search_character_knowledge,
    search_user_knowledge,
)


async def retrieve_context(
    user_id: int,
    query: str,
    top_k: int = 3,
) -> dict[str, str]:
    """Retrieve relevant context from all knowledge sources."""
    memories = search_memories(user_id, query, top_k)
    char_knowledge = search_character_knowledge(query, top_k)
    user_knowledge = search_user_knowledge(user_id, query, top_k)

    return {
        "memories": "\n".join(f"- {m}" for m in memories) if memories else "",
        "character_knowledge": "\n".join(f"- {k}" for k in char_knowledge) if char_knowledge else "",
        "user_knowledge": "\n".join(f"- {k}" for k in user_knowledge) if user_knowledge else "",
    }
