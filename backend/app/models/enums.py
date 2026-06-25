import enum
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import mapped_column

def enum_column(enum_class, **kwargs):
    return mapped_column(
        SAEnum(enum_class, values_callable=lambda x: [e.value for e in x]),
        **kwargs
    )

class Role(str, enum.Enum):
    ANALYST = "analyst"
    SENIOR_REVIEWER = "senior_reviewer"
    POLICY = "policy"
    ADMIN = "admin"

class ContentType(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    ACCOUNT = "account"

class Severity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CaseStatus(str, enum.Enum):
    UNASSIGNED = "unassigned"
    ASSIGNED = "assigned"
    IN_REVIEW = "in_review"
    ESCALATED = "escalated"
    RESOLVED = "resolved"

class Action(str, enum.Enum):
    APPROVE = "approve"
    REMOVE = "remove"
    WARN = "warn"
    RESTRICT = "restrict"
    ESCALATE = "escalate"
    REQUEST_INFO = "request_info"

class ConfidenceLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class EscalationType(str, enum.Enum):
    SENIOR_REVIEW = "senior_review"
    POLICY_REVIEW = "policy_review"
    LEGAL = "legal"
    QUALITY_CHECK = "quality_check"
