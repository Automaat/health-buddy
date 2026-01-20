from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MedicalHistory(Base):
    __tablename__ = "medical_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # surgery, hospitalization, family_history
    description: Mapped[str] = mapped_column(Text, nullable=False)
    event_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    provider: Mapped[str | None] = mapped_column(String(200), nullable=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
