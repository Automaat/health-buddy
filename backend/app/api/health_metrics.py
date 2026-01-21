from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import HealthMetricCreate, HealthMetricResponse, HealthMetricUpdate
from app.services.crud import health_metric

router = APIRouter(prefix="/health-metrics", tags=["health-metrics"])


@router.post("", response_model=HealthMetricResponse)
def create_health_metric(metric: HealthMetricCreate, db: Session = Depends(get_db)):
    return health_metric.create(db=db, obj_in=metric)


@router.get("/{metric_id}", response_model=HealthMetricResponse)
def get_health_metric(metric_id: int, db: Session = Depends(get_db)):
    db_metric = health_metric.get(db=db, id=metric_id)
    if not db_metric:
        raise HTTPException(status_code=404, detail="Health metric not found")
    return db_metric


@router.get("", response_model=list[HealthMetricResponse])
def list_health_metrics(
    skip: int = 0,
    limit: int = 100,
    owner: str | None = None,
    metric_type: str | None = None,
    db: Session = Depends(get_db),
):
    return health_metric.get_multi(
        db=db, skip=skip, limit=limit, owner=owner, metric_type=metric_type
    )


@router.patch("/{metric_id}", response_model=HealthMetricResponse)
def update_health_metric(
    metric_id: int, metric_update: HealthMetricUpdate, db: Session = Depends(get_db)
):
    db_metric = health_metric.get(db=db, id=metric_id)
    if not db_metric:
        raise HTTPException(status_code=404, detail="Health metric not found")
    return health_metric.update(db=db, db_obj=db_metric, obj_in=metric_update)


@router.delete("/{metric_id}", response_model=HealthMetricResponse)
def delete_health_metric(metric_id: int, db: Session = Depends(get_db)):
    db_metric = health_metric.delete(db=db, id=metric_id)
    if not db_metric:
        raise HTTPException(status_code=404, detail="Health metric not found")
    return db_metric
