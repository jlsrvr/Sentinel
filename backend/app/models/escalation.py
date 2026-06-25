import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey, CheckConstraint
from app.core.database import Base
from app.models.enums import enum_column, EscalationType

class Escalation(Base):
    __tablename__ = 'escalations'
    __table_args__ = (
        CheckConstraint(
            "to_queue_id IS NOT NULL OR to_reviewer_id IS NOT NULL",
            name="ck_escalation_target"
        ),
    )
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cases.id"))
    initiated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    escalation_type: Mapped[EscalationType] = enum_column(EscalationType)
    reason: Mapped[str] = mapped_column()
    to_queue_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("queues.id"))
    to_reviewer_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
