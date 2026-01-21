from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

SourceType = Literal["manual", "apple_health_import", "apple_health_webhook"]


class HealthMetricBase(BaseModel):
    metric_type: str = Field(..., max_length=100)
    value: float
    unit: str = Field(..., max_length=50)
    measured_at: datetime
    owner: str = Field(..., max_length=100)
    notes: str | None = None
    is_active: bool = True


class HealthMetricCreate(HealthMetricBase):
    source: SourceType = "manual"


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
    source: SourceType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
