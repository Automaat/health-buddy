from datetime import date, datetime

from pydantic import BaseModel, Field


class MedicationBase(BaseModel):
    name: str = Field(..., max_length=200)
    dosage: str = Field(..., max_length=100)
    unit: str = Field(..., max_length=50)
    frequency: str = Field(..., max_length=100)
    purpose: str | None = None
    start_date: date
    end_date: date | None = None
    prescribing_doctor: str | None = Field(None, max_length=200)
    owner: str = Field(..., max_length=100)
    is_active: bool = True
    refill_reminder_date: date | None = None


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(BaseModel):
    name: str | None = Field(None, max_length=200)
    dosage: str | None = Field(None, max_length=100)
    unit: str | None = Field(None, max_length=50)
    frequency: str | None = Field(None, max_length=100)
    purpose: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    prescribing_doctor: str | None = Field(None, max_length=200)
    owner: str | None = Field(None, max_length=100)
    is_active: bool | None = None
    refill_reminder_date: date | None = None


class MedicationResponse(MedicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
