import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base
from app.models.enums import enum_column, ContentType, Severity, CaseStatus

class Case(Base):
    __tablename__ = 'cases'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    external_id: Mapped[str] = mapped_column()
    content_type: Mapped[ContentType] = enum_column(ContentType)
    content_ref: Mapped[str] = mapped_column()
    content_snapshot: Mapped[str | None] = mapped_column()
    severity: Mapped[Severity] = enum_column(Severity)
    status: Mapped[CaseStatus] = enum_column(CaseStatus)
    queue_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("queues.id"))
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    assigned_at: Mapped[datetime.datetime | None] = mapped_column()
    sla_deadline: Mapped[datetime.datetime | None] = mapped_column()
    source: Mapped[str | None] = mapped_column()
    case_metadata: Mapped[list] = mapped_column(JSONB)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    resolved_at: Mapped[datetime.datetime | None] = mapped_column()

