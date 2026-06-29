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