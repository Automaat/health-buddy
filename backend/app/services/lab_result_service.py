from sqlalchemy.orm import Session

from app.models import LabResult, LabResultValue
from app.schemas import LabResultCreate, LabResultUpdate
from app.services.base import CRUDBase


class LabResultService(CRUDBase[LabResult, LabResultCreate, LabResultUpdate]):
    def create(self, db: Session, obj_in: LabResultCreate) -> LabResult:
        obj_data = obj_in.model_dump(exclude={"values"})
        db_obj = LabResult(**obj_data)
        db.add(db_obj)
        db.flush()

        for value_in in obj_in.values:
            value_data = value_in.model_dump()
            db_value = LabResultValue(**value_data, lab_result_id=db_obj.id)
            db.add(db_value)

        db.commit()
        db.refresh(db_obj)
        return db_obj


lab_result_service = LabResultService(LabResult)
