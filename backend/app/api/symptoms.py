from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import SymptomCreate, SymptomResponse, SymptomUpdate
from app.services.crud import symptom

router = APIRouter(prefix="/symptoms", tags=["symptoms"])


@router.post("/", response_model=SymptomResponse)
def create_symptom(symp: SymptomCreate, db: Session = Depends(get_db)):
    return symptom.create(db=db, obj_in=symp)


@router.get("/{symptom_id}", response_model=SymptomResponse)
def get_symptom(symptom_id: int, db: Session = Depends(get_db)):
    db_symp = symptom.get(db=db, id=symptom_id)
    if not db_symp:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return db_symp


@router.get("/", response_model=list[SymptomResponse])
def list_symptoms(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return symptom.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{symptom_id}", response_model=SymptomResponse)
def update_symptom(symptom_id: int, symp_update: SymptomUpdate, db: Session = Depends(get_db)):
    db_symp = symptom.get(db=db, id=symptom_id)
    if not db_symp:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return symptom.update(db=db, db_obj=db_symp, obj_in=symp_update)


@router.delete("/{symptom_id}", response_model=SymptomResponse)
def delete_symptom(symptom_id: int, db: Session = Depends(get_db)):
    db_symp = symptom.delete(db=db, id=symptom_id)
    if not db_symp:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return db_symp
