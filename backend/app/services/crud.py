from app.models import (
    Allergy,
    AppConfig,
    Appointment,
    HealthGoal,
    HealthMetric,
    MedicalCondition,
    MedicalHistory,
    Medication,
    Supplement,
    Symptom,
    Vaccination,
)
from app.schemas import (
    AllergyCreate,
    AllergyUpdate,
    AppConfigCreate,
    AppConfigUpdate,
    AppointmentCreate,
    AppointmentUpdate,
    HealthGoalCreate,
    HealthGoalUpdate,
    HealthMetricCreate,
    HealthMetricUpdate,
    MedicalConditionCreate,
    MedicalConditionUpdate,
    MedicalHistoryCreate,
    MedicalHistoryUpdate,
    MedicationCreate,
    MedicationUpdate,
    SupplementCreate,
    SupplementUpdate,
    SymptomCreate,
    SymptomUpdate,
    VaccinationCreate,
    VaccinationUpdate,
)
from app.services.base import CRUDBase
from app.services.lab_result_service import lab_result_service as lab_result

health_metric = CRUDBase[HealthMetric, HealthMetricCreate, HealthMetricUpdate](HealthMetric)
medication = CRUDBase[Medication, MedicationCreate, MedicationUpdate](Medication)
supplement = CRUDBase[Supplement, SupplementCreate, SupplementUpdate](Supplement)
medical_condition = CRUDBase[MedicalCondition, MedicalConditionCreate, MedicalConditionUpdate](
    MedicalCondition
)
symptom = CRUDBase[Symptom, SymptomCreate, SymptomUpdate](Symptom)
appointment = CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate](Appointment)
health_goal = CRUDBase[HealthGoal, HealthGoalCreate, HealthGoalUpdate](HealthGoal)
allergy = CRUDBase[Allergy, AllergyCreate, AllergyUpdate](Allergy)
vaccination = CRUDBase[Vaccination, VaccinationCreate, VaccinationUpdate](Vaccination)
medical_history = CRUDBase[MedicalHistory, MedicalHistoryCreate, MedicalHistoryUpdate](
    MedicalHistory
)
app_config = CRUDBase[AppConfig, AppConfigCreate, AppConfigUpdate](AppConfig)

__all__ = [
    "allergy",
    "app_config",
    "appointment",
    "health_goal",
    "health_metric",
    "lab_result",
    "medical_condition",
    "medical_history",
    "medication",
    "supplement",
    "symptom",
    "vaccination",
]
