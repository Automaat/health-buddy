# Health Buddy

Health tracking application - Phase 1 (Backend)

## Stack

- **Backend**: FastAPI + Python 3.12 + SQLAlchemy 2.x + Pydantic + PostgreSQL + Alembic
- **Styling**: Nord theme
- **DevOps**: Docker Compose + uv

## Features

- Health metrics tracking (vitals, biometrics)
- Medication and supplement management
- Lab results tracking
- Medical conditions and symptoms
- Appointments scheduling
- Health goals tracking
- Allergies management
- Vaccination records
- Medical history

## Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.12+
- uv (Python package manager)

### Development

1. Start PostgreSQL:
```bash
docker-compose up postgres -d
```

2. Install dependencies:
```bash
cd backend
uv pip install -r pyproject.toml
```

3. Run migrations:
```bash
cd backend
alembic upgrade head
```

4. Start backend:
```bash
cd backend
uvicorn app.main:app --reload
```

API will be available at http://localhost:8000
API docs at http://localhost:8000/docs

### Docker

Run everything with Docker Compose:
```bash
docker-compose up
```

## API Endpoints

- `/api/health-metrics` - Health metrics CRUD
- `/api/medications` - Medications CRUD
- `/api/supplements` - Supplements CRUD
- `/api/lab-results` - Lab results CRUD
- `/api/conditions` - Medical conditions CRUD
- `/api/symptoms` - Symptoms CRUD
- `/api/appointments` - Appointments CRUD
- `/api/goals` - Health goals CRUD
- `/api/allergies` - Allergies CRUD
- `/api/vaccinations` - Vaccinations CRUD
- `/api/medical-history` - Medical history CRUD
- `/api/config` - App configuration CRUD
- `/api/dashboard` - Dashboard aggregated data

## Database Schema

13 main entities:
- HealthMetric
- Medication
- Supplement
- LabResult + LabResultValue
- MedicalCondition
- Symptom
- Appointment
- HealthGoal
- Allergy
- Vaccination
- MedicalHistory
- AppConfig

All entities support multi-user with `owner` field.

## License

MIT
