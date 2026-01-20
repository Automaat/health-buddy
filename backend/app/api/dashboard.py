from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import HealthGoal, HealthMetric, LabResult, Medication, Supplement

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard_data(owner: str, db: Session = Depends(get_db)):
    now = datetime.utcnow()

    latest_metrics = (
        db.query(HealthMetric)
        .filter(HealthMetric.owner == owner)
        .order_by(HealthMetric.measured_at.desc())
        .limit(10)
        .all()
    )

    active_medications = (
        db.query(Medication)
        .filter(Medication.owner == owner, Medication.is_active)
        .all()
    )

    active_supplements = (
        db.query(Supplement)
        .filter(Supplement.owner == owner, Supplement.is_active)
        .all()
    )

    recent_lab_results = (
        db.query(LabResult)
        .filter(LabResult.owner == owner)
        .order_by(LabResult.test_date.desc())
        .limit(3)
        .all()
    )

    active_goals = (
        db.query(HealthGoal)
        .filter(HealthGoal.owner == owner, ~HealthGoal.is_completed)
        .all()
    )

    return {
        "latest_metrics": latest_metrics,
        "active_medications": active_medications,
        "active_supplements": active_supplements,
        "recent_lab_results": recent_lab_results,
        "active_goals": active_goals,
    }
