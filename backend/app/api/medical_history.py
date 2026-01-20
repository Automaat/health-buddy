from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import MedicalHistoryCreate, MedicalHistoryResponse, MedicalHistoryUpdate
from app.services.crud import medical_history

router = APIRouter(prefix="/medical-history", tags=["medical-history"])


@router.post("/", response_model=MedicalHistoryResponse)
def create_medical_history(hist: MedicalHistoryCreate, db: Session = Depends(get_db)):
    return medical_history.create(db=db, obj_in=hist)


@router.get("/{history_id}", response_model=MedicalHistoryResponse)
def get_medical_history(history_id: int, db: Session = Depends(get_db)):
    db_hist = medical_history.get(db=db, id=history_id)
    if not db_hist:
        raise HTTPException(status_code=404, detail="Medical history not found")
    return db_hist


@router.get("/", response_model=list[MedicalHistoryResponse])
def list_medical_history(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return medical_history.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{history_id}", response_model=MedicalHistoryResponse)
def update_medical_history(
    history_id: int, hist_update: MedicalHistoryUpdate, db: Session = Depends(get_db)
):
    db_hist = medical_history.get(db=db, id=history_id)
    if not db_hist:
        raise HTTPException(status_code=404, detail="Medical history not found")
    return medical_history.update(db=db, db_obj=db_hist, obj_in=hist_update)


@router.delete("/{history_id}", response_model=MedicalHistoryResponse)
def delete_medical_history(history_id: int, db: Session = Depends(get_db)):
    db_hist = medical_history.delete(db=db, id=history_id)
    if not db_hist:
        raise HTTPException(status_code=404, detail="Medical history not found")
    return db_hist
