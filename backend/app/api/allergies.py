from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import AllergyCreate, AllergyResponse, AllergyUpdate
from app.services.crud import allergy

router = APIRouter(prefix="/allergies", tags=["allergies"])


@router.post("/", response_model=AllergyResponse)
def create_allergy(allrg: AllergyCreate, db: Session = Depends(get_db)):
    return allergy.create(db=db, obj_in=allrg)


@router.get("/{allergy_id}", response_model=AllergyResponse)
def get_allergy(allergy_id: int, db: Session = Depends(get_db)):
    db_allrg = allergy.get(db=db, id=allergy_id)
    if not db_allrg:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return db_allrg


@router.get("/", response_model=list[AllergyResponse])
def list_allergies(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return allergy.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{allergy_id}", response_model=AllergyResponse)
def update_allergy(
    allergy_id: int, allrg_update: AllergyUpdate, db: Session = Depends(get_db)
):
    db_allrg = allergy.get(db=db, id=allergy_id)
    if not db_allrg:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return allergy.update(db=db, db_obj=db_allrg, obj_in=allrg_update)


@router.delete("/{allergy_id}", response_model=AllergyResponse)
def delete_allergy(allergy_id: int, db: Session = Depends(get_db)):
    db_allrg = allergy.delete(db=db, id=allergy_id)
    if not db_allrg:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return db_allrg
