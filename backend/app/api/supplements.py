from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import SupplementCreate, SupplementResponse, SupplementUpdate
from app.services.crud import supplement

router = APIRouter(prefix="/supplements", tags=["supplements"])


@router.post("/", response_model=SupplementResponse)
def create_supplement(supp: SupplementCreate, db: Session = Depends(get_db)):
    return supplement.create(db=db, obj_in=supp)


@router.get("/{supplement_id}", response_model=SupplementResponse)
def get_supplement(supplement_id: int, db: Session = Depends(get_db)):
    db_supp = supplement.get(db=db, id=supplement_id)
    if not db_supp:
        raise HTTPException(status_code=404, detail="Supplement not found")
    return db_supp


@router.get("/", response_model=list[SupplementResponse])
def list_supplements(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return supplement.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{supplement_id}", response_model=SupplementResponse)
def update_supplement(
    supplement_id: int, supp_update: SupplementUpdate, db: Session = Depends(get_db)
):
    db_supp = supplement.get(db=db, id=supplement_id)
    if not db_supp:
        raise HTTPException(status_code=404, detail="Supplement not found")
    return supplement.update(db=db, db_obj=db_supp, obj_in=supp_update)


@router.delete("/{supplement_id}", response_model=SupplementResponse)
def delete_supplement(supplement_id: int, db: Session = Depends(get_db)):
    db_supp = supplement.delete(db=db, id=supplement_id)
    if not db_supp:
        raise HTTPException(status_code=404, detail="Supplement not found")
    return db_supp
