from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import MedicalConditionCreate, MedicalConditionResponse, MedicalConditionUpdate
from app.services.crud import medical_condition

router = APIRouter(prefix="/conditions", tags=["conditions"])


@router.post("/", response_model=MedicalConditionResponse)
def create_condition(cond: MedicalConditionCreate, db: Session = Depends(get_db)):
    return medical_condition.create(db=db, obj_in=cond)


@router.get("/{condition_id}", response_model=MedicalConditionResponse)
def get_condition(condition_id: int, db: Session = Depends(get_db)):
    db_cond = medical_condition.get(db=db, id=condition_id)
    if not db_cond:
        raise HTTPException(status_code=404, detail="Condition not found")
    return db_cond


@router.get("/", response_model=list[MedicalConditionResponse])
def list_conditions(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return medical_condition.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{condition_id}", response_model=MedicalConditionResponse)
def update_condition(
    condition_id: int, cond_update: MedicalConditionUpdate, db: Session = Depends(get_db)
):
    db_cond = medical_condition.get(db=db, id=condition_id)
    if not db_cond:
        raise HTTPException(status_code=404, detail="Condition not found")
    return medical_condition.update(db=db, db_obj=db_cond, obj_in=cond_update)


@router.delete("/{condition_id}", response_model=MedicalConditionResponse)
def delete_condition(condition_id: int, db: Session = Depends(get_db)):
    db_cond = medical_condition.delete(db=db, id=condition_id)
    if not db_cond:
        raise HTTPException(status_code=404, detail="Condition not found")
    return db_cond
