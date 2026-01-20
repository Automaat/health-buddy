from app.models import (
    AppConfig,
    HealthGoal,
    HealthMetric,
    MedicalHistory,
    Medication,
    Supplement,
    Vaccination,
)
from app.schemas import (
    AppConfigCreate,
    AppConfigUpdate,
    HealthGoalCreate,
    HealthGoalUpdate,
    HealthMetricCreate,
    HealthMetricUpdate,
    MedicalHistoryCreate,
    MedicalHistoryUpdate,
    MedicationCreate,
    MedicationUpdate,
    SupplementCreate,
    SupplementUpdate,
    VaccinationCreate,
    VaccinationUpdate,
)
from app.services.base import CRUDBase
from app.services.lab_result_service import lab_result_service as lab_result

health_metric = CRUDBase[HealthMetric, HealthMetricCreate, HealthMetricUpdate](HealthMetric)
medication = CRUDBase[Medication, MedicationCreate, MedicationUpdate](Medication)
supplement = CRUDBase[Supplement, SupplementCreate, SupplementUpdate](Supplement)
health_goal = CRUDBase[HealthGoal, HealthGoalCreate, HealthGoalUpdate](HealthGoal)
vaccination = CRUDBase[Vaccination, VaccinationCreate, VaccinationUpdate](Vaccination)
medical_history = CRUDBase[MedicalHistory, MedicalHistoryCreate, MedicalHistoryUpdate](
    MedicalHistory
)
app_config = CRUDBase[AppConfig, AppConfigCreate, AppConfigUpdate](AppConfig)

__all__ = [
    "app_config",
    "health_goal",
    "health_metric",
    "lab_result",
    "medical_history",
    "medication",
    "supplement",
    "vaccination",
]
