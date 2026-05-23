from app.services.deepseek import chat_completion


async def generate_summary(messages: list[dict]) -> str:
    """Generate a summary of a conversation."""
    if not messages:
        return ""
    text = "\n".join(f"{m['role']}: {m['content']}" for m in messages[-20:])
    summary = await chat_completion(
        system_prompt="你是一个对话摘要助手。请用一两句话概括以下对话的主要内容。",
        messages=[{"role": "user", "content": f"请概括这段对话：\n\n{text}"}],
    )
    return summary


class SlidingWindowMemory:
    """Maintains a sliding window of recent conversation turns."""

    def __init__(self, max_rounds: int = 30):
        self.max_rounds = max_rounds

    def append(self, messages: list, role: str, content: str) -> list:
        """Add a message, trim if over limit."""
        messages.append({"role": role, "content": content})
        # Keep only the last max_rounds pairs (user + ai = 2 per round)
        max_items = self.max_rounds * 2
        if len(messages) > max_items:
            messages = messages[-max_items:]
        return messages
