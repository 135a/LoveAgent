from fastapi import APIRouter, Depends
from app.middleware.jwt import require_user_id
from app.knowledge.ingestion import load_all_knowledge

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.post("/reload")
async def reload_knowledge(user_id: int = Depends(require_user_id)):
    """Manually trigger knowledge base reload."""
    await load_all_knowledge()
    return {"message": "知识库已重新加载"}
