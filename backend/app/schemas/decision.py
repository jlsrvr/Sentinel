import uuid
import datetime
from pydantic import BaseModel, ConfigDict
from app.models.enums import Action, ConfidenceLevel

class DecisionCreateRequest(BaseModel):
    action: Action
    rationale: str
    policy_reference: str | None
    confidence: ConfidenceLevel
    time_on_case_secs: int

class DecisionListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    case_id: uuid.UUID
    reviewer_id: uuid.UUID
    action: Action
    rationale: str
    policy_reference: str | None
    confidence: ConfidenceLevel
    time_on_case_secs: int
    created_at: datetime.datetime