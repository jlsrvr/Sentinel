import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base
from app.models.enums import enum_column, Role

class User(Base):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    full_name: Mapped[str] = mapped_column()
    role: Mapped[Role] = enum_column(Role)
    skills: Mapped[list] = mapped_column(JSONB)
    is_active: Mapped[bool] = mapped_column(default=True)
    exposure_limit_hours_per_week: Mapped[int] = mapped_column(default=20)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
