from datetime import datetime

from pydantic import BaseModel, Field


class AppConfigBase(BaseModel):
    key: str = Field(..., max_length=100)
    value: str


class AppConfigCreate(AppConfigBase):
    pass


class AppConfigUpdate(BaseModel):
    value: str


class AppConfigResponse(AppConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
