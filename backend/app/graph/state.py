from typing import TypedDict, Annotated, Optional, Sequence
from langgraph.graph.message import add_messages


class RelationshipState(TypedDict):
    """State for the LangGraph relationship conversation flow."""

    # Identity
    user_id: int
    character_id: str  # template id
    personality: str

    # Current conversation
    messages: Annotated[list, add_messages]
    current_input: str

    # Relationship tracking
    relationship_stage: int  # 0-5
    intimacy_score: float  # 0.0-1.0
    stage_name: str
    stage_description: str

    # Customization
    custom_name: Optional[str]

    # Memory & knowledge
    retrieved_memories: str
    user_knowledge: str
    character_knowledge: str

    # Emotion detection
    user_emotion: str  # detected emotion from input

    # Output
    system_prompt: str
    response: str
