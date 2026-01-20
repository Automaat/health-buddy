from datetime import date, datetime

from pydantic import BaseModel, Field


class MedicalConditionBase(BaseModel):
    name: str = Field(..., max_length=200)
    condition_type: str | None = Field(None, max_length=100)
    diagnosis_date: date | None = None
    diagnosed_by: str | None = Field(None, max_length=200)
    status: str = Field("active", max_length=50)
    owner: str = Field(..., max_length=100)
    severity: str | None = Field(None, max_length=50)
    notes: str | None = None
    is_active: bool = True


class MedicalConditionCreate(MedicalConditionBase):
    pass


class MedicalConditionUpdate(BaseModel):
    name: str | None = Field(None, max_length=200)
    condition_type: str | None = Field(None, max_length=100)
    diagnosis_date: date | None = None
    diagnosed_by: str | None = Field(None, max_length=200)
    status: str | None = Field(None, max_length=50)
    owner: str | None = Field(None, max_length=100)
    severity: str | None = Field(None, max_length=50)
    notes: str | None = None
    is_active: bool | None = None


class MedicalConditionResponse(MedicalConditionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
