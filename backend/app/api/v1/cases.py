from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.case import Case
from app.core.database import get_db
from app.schemas.case import CaseListResponse

router = APIRouter(prefix="/cases", tags=["cases"])

@router.get("/", response_model=list[CaseListResponse])
async def list_cases(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    query = select(Case).offset(skip).limit(limit)
    cases = db.execute(query).scalars().all()
    return cases