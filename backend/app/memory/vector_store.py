from typing import Optional

import chromadb
from chromadb.config import Settings

from app.config import settings


def _get_client() -> chromadb.Client:
    """
    获取一个ChromaDB客户端实例
    该函数创建并返回一个ChromaDB的HTTP客户端，用于与ChromaDB服务进行交互。
    客户端配置了禁用遥测功能，以保护数据隐私。
    Returns:
        chromadb.Client: ChromaDB的HTTP客户端实例，用于数据库连接和操作
    """
    return chromadb.HttpClient(
        host=settings.chroma_host,    # ChromaDB服务器的主机地址
        port=settings.chroma_port,    # ChromaDB服务器的端口号
        settings=Settings(anonymized_telemetry=False),  # 禁用匿名遥测设置
    )


def _user_collection_name(user_id: int, personality: str = "default", suffix: str = "memory") -> str:
    # ASCII-safe collection name
    p_map = {
        "文静": "quiet", "治愈": "healing", "傲娇": "tsundere",
        "阳光": "sunny", "风趣": "funny", "暖男": "warm"
    }
    p_id = p_map.get(personality, "unknown")
    return f"u_{user_id}_{p_id}_{suffix}"


def get_or_create_collection(user_id: int, personality: str = "default", suffix: str = "memory"):
    client = _get_client()
    name = _user_collection_name(user_id, personality, suffix)
    try:
        return client.get_collection(name)
    except Exception:
        return client.create_collection(name)


def get_global_collection(name: str = "global_character"):

    """
    获取或创建一个全局集合

    参数:
        name (str): 集合的名称，默认为"global_character"

    返回:
        Collection: 返回获取或创建的集合对象

    异常处理:
        如果获取集合失败，则尝试创建一个新的集合
    """
    client = _get_client()  # 获取客户端实例
    try:
        return client.get_collection(name)  # 尝试获取指定名称的集合
    except Exception:  # 如果获取集合失败
        return client.create_collection(name)  # 创建一个新的集合


def add_memory(user_id: int, personality: str, text: str, metadata: Optional[dict] = None):
    """Add a memory fragment for a user's specific character."""
    collection = get_or_create_collection(user_id, personality)
    import uuid
    collection.add(
        documents=[text],
        metadatas=[metadata or {}],
        ids=[str(uuid.uuid4())],
    )


def search_memories(user_id: int, personality: str, query: str, top_k: int = 5) -> list[str]:
    """Search memories for a user's specific character."""
    try:
        collection = get_or_create_collection(user_id, personality)
        results = collection.query(query_texts=[query], n_results=top_k)
        if results["documents"] and results["documents"][0]:
            return results["documents"][0]
    except Exception:
        pass
    return []


def search_character_knowledge(personality: str, query: str, top_k: int = 5) -> list[str]:
    """Search character-specific knowledge from global base."""
    try:
        collection = get_global_collection()
        results = collection.query(
            query_texts=[query], 
            n_results=top_k,
            where={"personality": personality}
        )
        if results["documents"] and results["documents"][0]:
            return results["documents"][0]
    except Exception:
        pass
    return []


def search_user_knowledge(user_id: int, personality: str, query: str, top_k: int = 5) -> list[str]:
    """Search user-specific knowledge for a specific character."""
    try:
        collection = get_or_create_collection(user_id, personality, "knowledge")
        results = collection.query(query_texts=[query], n_results=top_k)
        if results["documents"] and results["documents"][0]:
            return results["documents"][0]
    except Exception:
        pass
    return []
