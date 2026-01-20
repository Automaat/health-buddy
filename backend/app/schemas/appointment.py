from datetime import datetime

from pydantic import BaseModel, Field


class AppointmentBase(BaseModel):
    doctor_name: str = Field(..., max_length=200)
    specialty: str | None = Field(None, max_length=100)
    appointment_date: datetime
    purpose: str | None = None
    location: str | None = Field(None, max_length=200)
    notes: str | None = None
    follow_up_required: bool = False
    owner: str = Field(..., max_length=100)
    is_completed: bool = False


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    doctor_name: str | None = Field(None, max_length=200)
    specialty: str | None = Field(None, max_length=100)
    appointment_date: datetime | None = None
    purpose: str | None = None
    location: str | None = Field(None, max_length=200)
    notes: str | None = None
    follow_up_required: bool | None = None
    owner: str | None = Field(None, max_length=100)
    is_completed: bool | None = None


class AppointmentResponse(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
