from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import VaccinationCreate, VaccinationResponse, VaccinationUpdate
from app.services.crud import vaccination

router = APIRouter(prefix="/vaccinations", tags=["vaccinations"])


@router.post("/", response_model=VaccinationResponse)
def create_vaccination(vacc: VaccinationCreate, db: Session = Depends(get_db)):
    return vaccination.create(db=db, obj_in=vacc)


@router.get("/{vaccination_id}", response_model=VaccinationResponse)
def get_vaccination(vaccination_id: int, db: Session = Depends(get_db)):
    db_vacc = vaccination.get(db=db, id=vaccination_id)
    if not db_vacc:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    return db_vacc


@router.get("/", response_model=list[VaccinationResponse])
def list_vaccinations(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return vaccination.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{vaccination_id}", response_model=VaccinationResponse)
def update_vaccination(
    vaccination_id: int, vacc_update: VaccinationUpdate, db: Session = Depends(get_db)
):
    db_vacc = vaccination.get(db=db, id=vaccination_id)
    if not db_vacc:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    return vaccination.update(db=db, db_obj=db_vacc, obj_in=vacc_update)


@router.delete("/{vaccination_id}", response_model=VaccinationResponse)
def delete_vaccination(vaccination_id: int, db: Session = Depends(get_db)):
    db_vacc = vaccination.delete(db=db, id=vaccination_id)
    if not db_vacc:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    return db_vacc
