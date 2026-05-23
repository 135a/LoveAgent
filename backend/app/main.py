from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routes import auth, characters, relationship, knowledge
from app.routes.chat import router as chat_router
from app.knowledge.ingestion import load_all_knowledge

import app.models  # noqa: F401 - ensure models registered


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

    # Load knowledge base
    print("Loading knowledge base...")
    try:
        await load_all_knowledge()
    except Exception as e:
        print(f"⚠ Knowledge base load skipped: {e}")

    yield
    # Shutdown
    engine.dispose()


app = FastAPI(
    title="LoveAgent API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "LoveAgent is running"}

# Register routers
app.include_router(auth.router)
app.include_router(characters.router)
app.include_router(relationship.router)
app.include_router(knowledge.router)
app.include_router(chat_router)
