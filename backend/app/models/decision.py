import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from app.core.database import Base
from app.models.enums import enum_column, Action, ConfidenceLevel

class Decision(Base):
    __tablename__ = 'decisions'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cases.id"))
    reviewer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    action: Mapped[Action] = enum_column(Action)
    rationale: Mapped[str] = mapped_column()
    policy_reference: Mapped[str | None] = mapped_column()
    confidence: Mapped[ConfidenceLevel] = enum_column(ConfidenceLevel)
    time_on_case_secs: Mapped[int] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())