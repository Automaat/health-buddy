from datetime import date, datetime

from pydantic import BaseModel, Field


class LabResultValueBase(BaseModel):
    test_name: str = Field(..., max_length=200)
    value: float
    unit: str = Field(..., max_length=50)
    reference_range: str | None = Field(None, max_length=100)
    is_abnormal: bool = False


class LabResultValueCreate(LabResultValueBase):
    pass


class LabResultValueResponse(LabResultValueBase):
    id: int
    lab_result_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LabResultBase(BaseModel):
    test_date: date
    lab_name: str | None = Field(None, max_length=200)
    ordering_doctor: str | None = Field(None, max_length=200)
    owner: str = Field(..., max_length=100)
    notes: str | None = None


class LabResultCreate(LabResultBase):
    values: list[LabResultValueCreate] = []


class LabResultUpdate(BaseModel):
    test_date: date | None = None
    lab_name: str | None = Field(None, max_length=200)
    ordering_doctor: str | None = Field(None, max_length=200)
    owner: str | None = Field(None, max_length=100)
    notes: str | None = None


class LabResultResponse(LabResultBase):
    id: int
    created_at: datetime
    updated_at: datetime
    values: list[LabResultValueResponse] = []

    class Config:
        from_attributes = True
