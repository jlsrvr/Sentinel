import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.case import Case
from app.core.database import get_db
from app.schemas.case import CaseListResponse, CaseDetailResponse

router = APIRouter(prefix="/cases", tags=["cases"])

@router.get("/", response_model=list[CaseListResponse])
async def list_cases(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    query = select(Case).offset(skip).limit(limit)
    cases = db.execute(query).scalars().all()
    return cases

@router.get("/{case_id}", response_model=CaseDetailResponse)
async def case_details(case_id: uuid.UUID, db: Session = Depends(get_db)):
    query = select(Case).where(Case.id == case_id)
    case = db.execute(query).scalars().first()
    if case:
        return case
    raise HTTPException(status_code=404, detail="Item not found")