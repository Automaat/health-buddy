from datetime import date, datetime

from pydantic import BaseModel, Field


class AllergyBase(BaseModel):
    allergen: str = Field(..., max_length=200)
    reaction_type: str | None = Field(None, max_length=200)
    severity: str | None = Field(None, max_length=50)
    identified_date: date | None = None
    notes: str | None = None
    owner: str = Field(..., max_length=100)
    is_active: bool = True


class AllergyCreate(AllergyBase):
    pass


class AllergyUpdate(BaseModel):
    allergen: str | None = Field(None, max_length=200)
    reaction_type: str | None = Field(None, max_length=200)
    severity: str | None = Field(None, max_length=50)
    identified_date: date | None = None
    notes: str | None = None
    owner: str | None = Field(None, max_length=100)
    is_active: bool | None = None


class AllergyResponse(AllergyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
