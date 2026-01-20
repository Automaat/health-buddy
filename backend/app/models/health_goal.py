from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class HealthGoal(Base):
    __tablename__ = "health_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    goal_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_unit: Mapped[str] = mapped_column(String(50), nullable=False)
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    current_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    start_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
