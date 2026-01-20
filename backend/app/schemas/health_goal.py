from datetime import date, datetime

from pydantic import BaseModel, Field


class HealthGoalBase(BaseModel):
    name: str = Field(..., max_length=200)
    goal_type: str = Field(..., max_length=100)
    target_value: float
    target_unit: str = Field(..., max_length=50)
    target_date: date | None = None
    current_value: float | None = None
    start_value: float | None = None
    owner: str = Field(..., max_length=100)
    is_completed: bool = False


class HealthGoalCreate(HealthGoalBase):
    pass


class HealthGoalUpdate(BaseModel):
    name: str | None = Field(None, max_length=200)
    goal_type: str | None = Field(None, max_length=100)
    target_value: float | None = None
    target_unit: str | None = Field(None, max_length=50)
    target_date: date | None = None
    current_value: float | None = None
    start_value: float | None = None
    owner: str | None = Field(None, max_length=100)
    is_completed: bool | None = None


class HealthGoalResponse(HealthGoalBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
