from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.jwt import require_user_id
from app.models import UserCharacter, Milestone
from app.relationship.engine import get_stage_info

router = APIRouter(prefix="/api/relationship", tags=["relationship"])


class RelationshipResponse(BaseModel):
    stage: int
    stage_name: str
    intimacy_score: float
    milestones: list[dict]


@router.get("/")
async def get_relationship(
    user_id: int = Depends(require_user_id),
    db: Session = Depends(get_db),
):
    char = db.query(UserCharacter).filter(UserCharacter.user_id == user_id).first()
    if char is None:
        raise HTTPException(status_code=404, detail="尚未创建角色")

    stage_info = get_stage_info(char.relationship_stage)
    milestones = db.query(Milestone).filter(
        Milestone.user_id == user_id
    ).order_by(Milestone.created_at.desc()).limit(20).all()

    return RelationshipResponse(
        stage=char.relationship_stage,
        stage_name=stage_info["name"],
        intimacy_score=char.intimacy_score,
        milestones=[
            {"event_type": m.event_type, "description": m.description,
             "intimacy_change": m.intimacy_change, "created_at": str(m.created_at)}
            for m in milestones
        ],
    )
