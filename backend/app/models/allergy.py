from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Allergy(Base):
    __tablename__ = "allergies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    allergen: Mapped[str] = mapped_column(String(200), nullable=False)
    reaction_type: Mapped[str | None] = mapped_column(String(200), nullable=True)
    severity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    identified_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
