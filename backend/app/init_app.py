"""
Application initialization script.
Run on startup to ensure DB tables exist and knowledge base is loaded.
"""
from app.database import engine, Base
from app.knowledge.ingestion import load_all_knowledge


async def init_app():
    """Initialize the application: create tables and load knowledge."""
    print("=== LoveAgent Initialization ===")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables ready")

    # Load knowledge base
    print("Loading knowledge base...")
    try:
        await load_all_knowledge()
    except Exception as e:
        print(f"⚠ Knowledge base load skipped (ChromaDB may not be ready): {e}")

    print("=== Initialization Complete ===")
