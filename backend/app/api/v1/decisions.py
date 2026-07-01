import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.case import Case
from app.models.decision import Decision
from app.models.enums import CaseStatus
from app.core.database import get_db
from app.schemas.decision import DecisionCreateRequest
from app.core.dependencies import get_current_user_id

router = APIRouter(prefix="/cases/{case_id}/decisions", tags=["decisions"])

@router.post("/", status_code=201)
async def create_decision(
    case_id: uuid.UUID,
    body: DecisionCreateRequest,
    db: Session = Depends(get_db),
    reviewer_id: uuid.UUID = Depends(get_current_user_id)
):
    case_query = select(Case).where(Case.id == case_id)
    case = db.execute(case_query).scalars().first()
    reviewer_query = select(User).where(User.id == reviewer_id)
    reviewer = db.execute(reviewer_query).scalars().first()
    if case is None or reviewer is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if case.status != CaseStatus.IN_REVIEW:
        raise HTTPException(status_code=409, detail="Case cannot receive decision")
    decision = Decision(
        case_id=case.id,
        reviewer_id=reviewer_id,
        action=body.action,
        rationale=body.rationale,
        policy_reference=body.policy_reference,
        confidence=body.confidence,
        time_on_case_secs=body.time_on_case_secs,
    )
    db.add(decision)
    db.flush()