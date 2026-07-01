import uuid
import datetime
from pydantic import BaseModel, ConfigDict
from app.models.enums import ContentType, Severity, CaseStatus

class CaseListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : uuid.UUID
    external_id : str
    severity : Severity
    status : CaseStatus
    content_type : ContentType
    source : str
    queue_id : uuid.UUID
    assigned_to : uuid.UUID | None
    sla_deadline : datetime.datetime | None

class CaseDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    external_id: str
    content_type: ContentType
    content_ref: str
    content_snapshot: str | None
    severity: Severity
    status: CaseStatus
    queue_id: uuid.UUID
    assigned_to: uuid.UUID | None
    assigned_at: datetime.datetime | None
    sla_deadline: datetime.datetime | None
    source: str
    case_metadata: list
    created_at: datetime.datetime
    updated_at: datetime.datetime
    resolved_at: datetime.datetime | None