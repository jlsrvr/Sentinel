import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.case import Case
from app.core.database import get_db
from app.schemas.case import CaseListResponse, CaseDetailResponse
from app.models.enums import CaseStatus
from app.services.case import can_transition, transition, assign, start_review
from app.core.dependencies import get_current_user_id, get_case_or_404
from app.core.exceptions import InvalidTransitionError

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

def _find_case(case_id: uuid.UUID, db: Session = Depends(get_db)):
    case_query = select(Case).where(Case.id == case_id)
    case = db.execute(case_query).scalars().first()
    if case is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return case

@router.post("/{case_id}/assign", status_code=201)
def assign_case(
    case: Case = Depends(get_case_or_404),
    db: Session = Depends(get_db),
    reviewer_id: uuid.UUID = Depends(get_current_user_id)
):
    try:
        assign(case, reviewer_id)
    except (InvalidTransitionError, ValueError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    db.commit()

@router.post("/{case_id}/start_review", status_code=201)
def start_case_review(
    case: Case = Depends(get_case_or_404),
    db: Session = Depends(get_db)
):
    try:
        start_review(case)
    except (InvalidTransitionError, ValueError) as e:
        raise HTTPException(status_code=409, detail=str(e))
    db.commit()