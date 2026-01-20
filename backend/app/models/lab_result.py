from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.lab_result_value import LabResultValue


class LabResult(Base):
    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    lab_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    ordering_doctor: Mapped[str | None] = mapped_column(String(200), nullable=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    values: Mapped[list["LabResultValue"]] = relationship(
        back_populates="lab_result", cascade="all, delete-orphan"
    )
