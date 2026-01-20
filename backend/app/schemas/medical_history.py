from datetime import date, datetime

from pydantic import BaseModel, Field


class MedicalHistoryBase(BaseModel):
    event_type: str = Field(..., max_length=100)
    description: str
    event_date: date | None = None
    provider: str | None = Field(None, max_length=200)
    owner: str = Field(..., max_length=100)
    notes: str | None = None


class MedicalHistoryCreate(MedicalHistoryBase):
    pass


class MedicalHistoryUpdate(BaseModel):
    event_type: str | None = Field(None, max_length=100)
    description: str | None = None
    event_date: date | None = None
    provider: str | None = Field(None, max_length=200)
    owner: str | None = Field(None, max_length=100)
    notes: str | None = None


class MedicalHistoryResponse(MedicalHistoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
