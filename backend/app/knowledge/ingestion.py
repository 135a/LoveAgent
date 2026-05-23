import os
from pathlib import Path

# In container: /app/app/knowledge/ingestion.py -> /app/knowledge
KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "knowledge"


def load_text_files(directory: Path) -> list[tuple[str, str]]:
    """Load all .txt and .md files from a directory, return list of (filename, content)."""
    chunks = []
    if not directory.exists():
        return chunks
    for f in directory.iterdir():
        if f.suffix in (".txt", ".md") and f.is_file():
            content = f.read_text(encoding="utf-8").strip()
            if content:
                # Split into paragraphs as chunks
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                for para in paragraphs:
                    if len(para) > 20:  # skip very short fragments
                        chunks.append((f.name, para))
    return chunks


def get_user_knowledge_files() -> list[tuple[str, str]]:
    return load_text_files(KNOWLEDGE_DIR / "user")


def get_character_knowledge_files(gender: str) -> list[tuple[str, str]]:
    return load_text_files(KNOWLEDGE_DIR / "character" / gender)


async def load_all_knowledge():
    """Load all knowledge files into vector store."""
    from app.memory.vector_store import (
        get_global_collection, get_or_create_collection,
    )

    # Load character knowledge into global collection
    char_coll = get_global_collection("global_character")
    existing_ids = set(char_coll.get()["ids"])

    for gender in ("female", "male"):
        for fname, content in get_character_knowledge_files(gender):
            chunk_id = f"char_{gender}_{fname}"
            if chunk_id not in existing_ids:
                char_coll.add(
                    documents=[content],
                    metadatas=[{"source": fname, "gender": gender, "type": "character"}],
                    ids=[chunk_id],
                )
                print(f"  ✓ Loaded character knowledge: {fname}")

    # Note: user knowledge is loaded per-user on first interaction
    print("✓ Knowledge base loaded successfully")
