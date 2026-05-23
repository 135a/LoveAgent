from langgraph.graph import StateGraph, END

from app.graph.state import RelationshipState
from app.graph.nodes import (
    input_gate,
    memory_retrieval,
    prompt_assembly,
    llm_call,
    post_processing,
)


def build_chat_graph() -> StateGraph:
    """Build the LangGraph for the relationship chat flow."""
    workflow = StateGraph(RelationshipState)

    # Add nodes
    workflow.add_node("input_gate", input_gate)
    workflow.add_node("memory_retrieval", memory_retrieval)
    workflow.add_node("prompt_assembly", prompt_assembly)
    workflow.add_node("llm_call", llm_call)
    workflow.add_node("post_processing", post_processing)

    # Set entry point
    workflow.set_entry_point("input_gate")

    # Define edges
    workflow.add_edge("input_gate", "memory_retrieval")
    workflow.add_edge("memory_retrieval", "prompt_assembly")
    workflow.add_edge("prompt_assembly", "llm_call")
    workflow.add_edge("llm_call", "post_processing")
    workflow.add_edge("post_processing", END)

    return workflow.compile()


# Global compiled graph instance
chat_graph = build_chat_graph()
