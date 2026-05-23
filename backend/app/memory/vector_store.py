from typing import Optional

import chromadb
from chromadb.config import Settings

from app.config import settings


def _get_client() -> chromadb.Client:
    return chromadb.HttpClient(
        host=settings.chroma_host,
        port=settings.chroma_port,
        settings=Settings(anonymized_telemetry=False),
    )


def _user_collection_name(user_id: int, suffix: str = "memory") -> str:
    return f"user_{user_id}_{suffix}"


def get_or_create_collection(user_id: int, suffix: str = "memory"):
    client = _get_client()
    name = _user_collection_name(user_id, suffix)
    try:
        return client.get_collection(name)
    except Exception:
        return client.create_collection(name)


def get_global_collection(name: str = "global_character"):
    client = _get_client()
    try:
        return client.get_collection(name)
    except Exception:
        return client.create_collection(name)


def add_memory(user_id: int, text: str, metadata: Optional[dict] = None):
    """Add a memory fragment for a user."""
    collection = get_or_create_collection(user_id)
    import uuid
    collection.add(
        documents=[text],
        metadatas=[metadata or {}],
        ids=[str(uuid.uuid4())],
    )


def search_memories(user_id: int, query: str, top_k: int = 5) -> list[str]:
    """Search memories for a user."""
    try:
        collection = get_or_create_collection(user_id)
        results = collection.query(query_texts=[query], n_results=top_k)
        if results["documents"] and results["documents"][0]:
            return results["documents"][0]
    except Exception:
        pass
    return []


def search_character_knowledge(query: str, top_k: int = 5) -> list[str]:
    """Search global character knowledge base."""
    try:
        collection = get_global_collection()
        results = collection.query(query_texts=[query], n_results=top_k)
        if results["documents"] and results["documents"][0]:
            return results["documents"][0]
    except Exception:
        pass
    return []


def search_user_knowledge(user_id: int, query: str, top_k: int = 5) -> list[str]:
    """Search user-specific knowledge."""
    try:
        collection = get_or_create_collection(user_id, "knowledge")
        results = collection.query(query_texts=[query], n_results=top_k)
        if results["documents"] and results["documents"][0]:
            return results["documents"][0]
    except Exception:
        pass
    return []
