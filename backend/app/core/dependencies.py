import uuid
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.case import Case
from app.core.database import get_db
from sqlalchemy import select

def get_current_user_id() -> uuid.UUID:
    # TODO: replace with real JWT auth
    return uuid.UUID('deaf35cb-f139-4e70-9bd6-4515f68c89a7')

def get_case_or_404(case_id: uuid.UUID, db: Session = Depends(get_db)) -> Case:
    case = db.execute(select(Case).where(Case.id == case_id)).scalars().first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case