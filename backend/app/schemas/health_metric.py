from datetime import datetime

from pydantic import BaseModel, Field


class HealthMetricBase(BaseModel):
    metric_type: str = Field(..., max_length=100)
    value: float
    unit: str = Field(..., max_length=50)
    measured_at: datetime
    owner: str = Field(..., max_length=100)
    notes: str | None = None
    is_active: bool = True


class HealthMetricCreate(HealthMetricBase):
    pass


class HealthMetricUpdate(BaseModel):
    metric_type: str | None = Field(None, max_length=100)
    value: float | None = None
    unit: str | None = Field(None, max_length=50)
    measured_at: datetime | None = None
    owner: str | None = Field(None, max_length=100)
    notes: str | None = None
    is_active: bool | None = None


class HealthMetricResponse(HealthMetricBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
