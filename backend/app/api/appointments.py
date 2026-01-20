from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.services.crud import appointment

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentResponse)
def create_appointment(appt: AppointmentCreate, db: Session = Depends(get_db)):
    return appointment.create(db=db, obj_in=appt)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appt = appointment.get(db=db, id=appointment_id)
    if not db_appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appt


@router.get("/", response_model=list[AppointmentResponse])
def list_appointments(
    skip: int = 0, limit: int = 100, owner: str | None = None, db: Session = Depends(get_db)
):
    return appointment.get_multi(db=db, skip=skip, limit=limit, owner=owner)


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int, appt_update: AppointmentUpdate, db: Session = Depends(get_db)
):
    db_appt = appointment.get(db=db, id=appointment_id)
    if not db_appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment.update(db=db, db_obj=db_appt, obj_in=appt_update)


@router.delete("/{appointment_id}", response_model=AppointmentResponse)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appt = appointment.delete(db=db, id=appointment_id)
    if not db_appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appt
