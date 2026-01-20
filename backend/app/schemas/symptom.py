from datetime import datetime

from pydantic import BaseModel, Field


class SymptomBase(BaseModel):
    symptom_type: str = Field(..., max_length=200)
    severity: int = Field(..., ge=1, le=10)
    occurred_at: datetime
    duration_minutes: int | None = Field(None, ge=0)
    notes: str | None = None
    owner: str = Field(..., max_length=100)
    related_condition_id: int | None = None


class SymptomCreate(SymptomBase):
    pass


class SymptomUpdate(BaseModel):
    symptom_type: str | None = Field(None, max_length=200)
    severity: int | None = Field(None, ge=1, le=10)
    occurred_at: datetime | None = None
    duration_minutes: int | None = Field(None, ge=0)
    notes: str | None = None
    owner: str | None = Field(None, max_length=100)
    related_condition_id: int | None = None


class SymptomResponse(SymptomBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
