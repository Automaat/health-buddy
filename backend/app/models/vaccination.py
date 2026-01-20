from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vaccine_name: Mapped[str] = mapped_column(String(200), nullable=False)
    date_administered: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    lot_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
