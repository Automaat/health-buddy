from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import LabResultCreate, LabResultResponse, LabResultUpdate
from app.services.crud import lab_result

router = APIRouter(prefix="/lab-results", tags=["lab-results"])


@router.post("/", response_model=LabResultResponse)
def create_lab_result(result: LabResultCreate, db: Session = Depends(get_db)):
    return lab_result.create(db=db, obj_in=result)


@router.get("/{result_id}", response_model=LabResultResponse)
def get_lab_result(result_id: int, db: Session = Depends(get_db)):
    db_result = lab_result.get(db=db, id=result_id)
    if not db_result:
        raise HTTPException(status_code=404, detail="Lab result not found")
    return db_result


@router.get("/", response_model=list[LabResultResponse])
def list_lab_results(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return lab_result.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{result_id}", response_model=LabResultResponse)
def update_lab_result(
    result_id: int, result_update: LabResultUpdate, db: Session = Depends(get_db)
):
    db_result = lab_result.get(db=db, id=result_id)
    if not db_result:
        raise HTTPException(status_code=404, detail="Lab result not found")
    return lab_result.update(db=db, db_obj=db_result, obj_in=result_update)


@router.delete("/{result_id}", response_model=LabResultResponse)
def delete_lab_result(result_id: int, db: Session = Depends(get_db)):
    db_result = lab_result.delete(db=db, id=result_id)
    if not db_result:
        raise HTTPException(status_code=404, detail="Lab result not found")
    return db_result
