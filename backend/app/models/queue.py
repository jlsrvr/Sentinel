import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base

class Queue(Base):
    __tablename__ = 'queues'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column()
    required_skills: Mapped[list] = mapped_column(JSONB)
    severity_levels: Mapped[list] = mapped_column(JSONB)
    sla_hours: Mapped[int | None] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
