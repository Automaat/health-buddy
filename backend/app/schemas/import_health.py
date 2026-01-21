"""Schemas for Apple Health import endpoints."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ImportResult(BaseModel):
    """Result of a health data import operation."""

    total_records: int
    imported: int
    skipped: int
    errors: int


class ImportStatus(BaseModel):
    """Status of last import operation."""

    last_import_at: datetime | None = None
    last_import_source: str | None = None
    last_import_count: int | None = None


class HealthAutoExportPayload(BaseModel):
    """Health Auto Export JSON payload structure."""

    data: dict[str, Any] | None = None
    metrics: list[dict[str, Any]] | None = None
