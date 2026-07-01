from pydantic import BaseModel, ConfigDict
from app.models.enums import Action, ConfidenceLevel

class DecisionCreateRequest(BaseModel):
    action: Action
    rationale: str
    policy_reference: str | None
    confidence: ConfidenceLevel
    time_on_case_secs: int