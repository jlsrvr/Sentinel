import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from app.core.database import Base
from app.models.enums import Severity, severity_enum

class ContentExposure(Base):
    __tablename__ = 'content_exposures'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    reviewer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cases.id"))
    severity_at_review: Mapped[Severity] = mapped_column(severity_enum)
    started_at: Mapped[datetime.datetime] = mapped_column()
    ended_at: Mapped[datetime.datetime | None] = mapped_column()
    duration_secs: Mapped[int | None] = mapped_column()
    week_start: Mapped[datetime.date] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())