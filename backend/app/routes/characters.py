from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.jwt import require_user_id
from app.models import UserCharacter
from app.characters.engine import list_templates, get_template

router = APIRouter(prefix="/api/characters", tags=["characters"])


class CharacterListView(BaseModel):
    id: str
    gender: str
    personality: str
    name: str
    description: str
    traits: list[str]


class ChooseRequest(BaseModel):
    gender: str
    personality: str


class CharacterInfo(BaseModel):
    gender: str
    personality: str
    custom_name: Optional[str]
    relationship_stage: int
    intimacy_score: float


@router.get("/")
async def get_characters(gender: Optional[str] = None):
    templates = list_templates(gender)
    return [
        CharacterListView(
            id=t.id,
            gender=t.gender,
            personality=t.personality,
            name=t.name,
            description=t.description,
            traits=t.traits,
        )
        for t in templates
    ]


@router.post("/choose")
async def choose_character(
    req: ChooseRequest,
    user_id: int = Depends(require_user_id),
    db: Session = Depends(get_db),
):
    if req.gender not in ("female", "male"):
        raise HTTPException(status_code=400, detail="性别只能为 female 或 male")

    # Validate the personality exists
    templates = list_templates(req.gender)
    valid_personalities = [t.personality for t in templates]
    if req.personality not in valid_personalities:
        raise HTTPException(status_code=400, detail=f"该性别下无此性格变体，可选：{valid_personalities}")

    # Check if user already has a character
    existing = db.query(UserCharacter).filter(UserCharacter.user_id == user_id).first()
    if existing:
        existing.gender = req.gender
        existing.personality = req.personality
        existing.custom_name = None
        existing.relationship_stage = 0
        existing.intimacy_score = 0.0
        db.commit()
        db.refresh(existing)
        return {"message": "角色已更换", "character": existing}

    new_char = UserCharacter(
        user_id=user_id,
        gender=req.gender,
        personality=req.personality,
    )
    db.add(new_char)
    db.commit()
    db.refresh(new_char)
    return {"message": "角色创建成功", "character": new_char}


@router.get("/my", response_model=Optional[CharacterInfo])
async def get_my_character(
    user_id: int = Depends(require_user_id),
    db: Session = Depends(get_db),
):
    char = db.query(UserCharacter).filter(UserCharacter.user_id == user_id).first()
    if char is None:
        return None
    return CharacterInfo(
        gender=char.gender,
        personality=char.personality,
        custom_name=char.custom_name,
        relationship_stage=char.relationship_stage,
        intimacy_score=char.intimacy_score,
    )
