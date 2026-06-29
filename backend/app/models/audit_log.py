import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, INET
from app.core.database import Base
from app.models.enums import EntityType

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    entity_type: Mapped[EntityType] = mapped_column()
    entity_id: Mapped[uuid.UUID] = mapped_column()
    action: Mapped[str] = mapped_column()
    actor_id: Mapped[uuid.UUID| None] = mapped_column(ForeignKey("users.id"))
    before_state: Mapped[list | None] = mapped_column(JSONB)
    after_state: Mapped[list| None] = mapped_column(JSONB)
    ip_address: Mapped[str | None] = mapped_column(INET)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())