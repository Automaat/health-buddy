from datetime import date, datetime

from pydantic import BaseModel, Field


class VaccinationBase(BaseModel):
    vaccine_name: str = Field(..., max_length=200)
    date_administered: date
    next_due_date: date | None = None
    location: str | None = Field(None, max_length=200)
    lot_number: str | None = Field(None, max_length=100)
    notes: str | None = None
    owner: str = Field(..., max_length=100)


class VaccinationCreate(VaccinationBase):
    pass


class VaccinationUpdate(BaseModel):
    vaccine_name: str | None = Field(None, max_length=200)
    date_administered: date | None = None
    next_due_date: date | None = None
    location: str | None = Field(None, max_length=200)
    lot_number: str | None = Field(None, max_length=100)
    notes: str | None = None
    owner: str | None = Field(None, max_length=100)


class VaccinationResponse(VaccinationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
