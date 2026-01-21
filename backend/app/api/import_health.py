"""API endpoints for importing Apple Health data."""

import logging

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import HealthMetric
from app.schemas import HealthAutoExportPayload, HealthMetricCreate, ImportResult
from app.services.apple_health_parser import apple_health_parser
from app.services.crud import health_metric

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/import", tags=["import"])

DEFAULT_OWNER = "default_user"


@router.post("/apple-health", response_model=ImportResult)
async def import_apple_health_xml(
    file: UploadFile = File(...),
    owner: str = Query(DEFAULT_OWNER),
    aggregate_days: int = Query(30, description="Aggregate old data to daily values. 0=disable"),
    db: Session = Depends(get_db),
) -> ImportResult:
    """Import Apple Health export XML file.

    High-frequency metrics (heart_rate, steps, hrv) older than aggregate_days
    are aggregated to daily averages/sums to reduce storage.
    """
    if not file.filename or not file.filename.endswith(".xml"):
        raise HTTPException(status_code=400, detail="File must be an XML file")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")

    try:
        metrics = apple_health_parser.parse_xml(content, owner, aggregate_days)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse XML: {e}") from e

    return _import_metrics(db, metrics, owner)


@router.post("/apple-health/webhook", response_model=ImportResult)
def import_apple_health_webhook(
    payload: HealthAutoExportPayload,
    owner: str = Query(DEFAULT_OWNER),
    db: Session = Depends(get_db),
) -> ImportResult:
    """Webhook endpoint for Health Auto Export app."""
    data: dict = {}
    if payload.data:
        data = {"data": payload.data}
    elif payload.metrics:
        data = {"data": {"metrics": payload.metrics}}
    else:
        raise HTTPException(
            status_code=400,
            detail="No metrics data in payload. Expected 'data' or 'metrics' field.",
        )

    metrics = apple_health_parser.parse_auto_export_json(data, owner)
    return _import_metrics(db, metrics, owner)


def _import_metrics(
    db: Session, metrics: list[HealthMetricCreate], owner: str
) -> ImportResult:
    """Import metrics with deduplication."""
    imported = 0
    skipped = 0
    errors = 0

    for metric in metrics:
        try:
            existing = (
                db.query(HealthMetric)
                .filter(
                    HealthMetric.owner == owner,
                    HealthMetric.metric_type == metric.metric_type,
                    HealthMetric.measured_at == metric.measured_at,
                )
                .first()
            )

            if existing:
                if existing.source == "manual":
                    skipped += 1
                    continue
                existing.value = metric.value
                existing.unit = metric.unit
                existing.source = metric.source
                db.commit()
                imported += 1
            else:
                health_metric.create(db=db, obj_in=metric)
                imported += 1
        except Exception:
            logger.exception("Failed to import metric: %s", metric.metric_type)
            errors += 1
            db.rollback()

    return ImportResult(
        total_records=len(metrics),
        imported=imported,
        skipped=skipped,
        errors=errors,
    )
