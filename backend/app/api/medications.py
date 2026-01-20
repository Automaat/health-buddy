from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import MedicationCreate, MedicationResponse, MedicationUpdate
from app.services.crud import medication

router = APIRouter(prefix="/medications", tags=["medications"])


@router.post("/", response_model=MedicationResponse)
def create_medication(med: MedicationCreate, db: Session = Depends(get_db)):
    return medication.create(db=db, obj_in=med)


@router.get("/{medication_id}", response_model=MedicationResponse)
def get_medication(medication_id: int, db: Session = Depends(get_db)):
    db_med = medication.get(db=db, id=medication_id)
    if not db_med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return db_med


@router.get("/", response_model=list[MedicationResponse])
def list_medications(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return medication.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{medication_id}", response_model=MedicationResponse)
def update_medication(
    medication_id: int, med_update: MedicationUpdate, db: Session = Depends(get_db)
):
    db_med = medication.get(db=db, id=medication_id)
    if not db_med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication.update(db=db, db_obj=db_med, obj_in=med_update)


@router.delete("/{medication_id}", response_model=MedicationResponse)
def delete_medication(medication_id: int, db: Session = Depends(get_db)):
    db_med = medication.delete(db=db, id=medication_id)
    if not db_med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return db_med
