# Health-Buddy Project Guide

## Overview

Personal health tracking: vitals, medications, lab results, vaccinations, medical history.

**Stack:** Python 3.14/FastAPI/SQLAlchemy 2.0/PostgreSQL 18 + TypeScript/SvelteKit 5/Nord theme
**Multi-user:** `owner` field on all models
**Architecture:** Backend (Generic CRUD, layered), Frontend (runes, ../home-ui components)
**Tools:** mise for dependencies

## Project Structure

```
healt-buddy/
├── backend/app/          # api/ models/ schemas/ services/ core/
├── frontend/src/         # routes/ lib/components/ lib/types/ lib/utils/
├── ../home-ui/           # Shared UI (Button, Input, Modal, Card)
└── .mise.toml            # Python 3.14.2, Node 24
```

**Key modules:**
- Backend: 9 routers, 10 models, Generic CRUD pattern
- Frontend: 5 routes, 13 domain components, home-ui integration

## Development Workflow

**Before coding:** ASK questions → research patterns → plan → implement
**Process:** Explore → Plan → Code → Test → Commit
**Never:** Jump to code, guess patterns, make assumptions

## Python/Backend Conventions

### Code Style
- **Formatter:** ruff (line 100), **Type hints:** required everywhere
- **Imports:** Third-party alphabetical, then local alphabetical

### SQLAlchemy 2.0 Pattern
```python
from sqlalchemy.orm import Mapped, mapped_column

class HealthMetric(Base):
    __tablename__ = "health_metrics"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    metric_type: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    measured_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
```

### Generic CRUD Base
```python
from typing import Generic, TypeVar
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, obj_in: CreateSchemaType, owner: str) -> ModelType:
        db_obj = self.model(**obj_in.model_dump(), owner=owner)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
```

**Extend for complex ops:**
```python
class LabResultService(CRUDBase[LabResult, LabResultCreate, LabResultUpdate]):
    def get_with_values(self, db: Session, id: int) -> LabResult | None:
        return db.query(self.model).options(joinedload(self.model.values)).filter(
            self.model.id == id
        ).first()
```

### API Pattern
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(prefix="/api/health-metrics", tags=["health-metrics"])

@router.post("/", response_model=HealthMetricRead)
def create_metric(
    metric: HealthMetricCreate,
    db: Session = Depends(get_db),
    owner: str = "default_user",  # TODO: auth
) -> HealthMetricRead:
    return health_metric_service.create(db, metric, owner)

@router.get("/{metric_id}", response_model=HealthMetricRead)
def get_metric(metric_id: int, db: Session = Depends(get_db)) -> HealthMetricRead:
    db_obj = health_metric_service.get(db, metric_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return db_obj
```

### Pydantic v2 Schemas
```python
from pydantic import BaseModel, Field

class HealthMetricCreate(BaseModel):
    metric_type: str = Field(..., min_length=1)
    value: float
    unit: str
    measured_at: datetime
    notes: str | None = None

class HealthMetricUpdate(BaseModel):
    value: float | None = None
    notes: str | None = None
    class Config:
        from_attributes = True  # Pydantic v2

class HealthMetricRead(HealthMetricCreate):
    id: int
    owner: str
    created_at: datetime
    class Config:
        from_attributes = True
```

## TypeScript/Frontend Conventions

### Code Style
- **Formatter:** Prettier (tabs, single quotes, 100 chars), **Linter:** oxlint
- **Naming:** camelCase vars, PascalCase types/components, kebab-case files
- **NEVER use `any` type** - explicit types always

### Svelte 5 Runes
```typescript
<script lang="ts">
	interface Props {
		title: string;
		value: number;
		variant?: 'blue' | 'green' | 'yellow' | 'red';
		trend?: 'up' | 'down' | 'stable';
	}

	let { title, value, variant = 'blue', trend = 'stable' }: Props = $props();
	const trendSymbol = $derived(trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→');
</script>
```

### Type Safety
```typescript
// Full interfaces for API responses
export interface HealthMetric {
	id: number;
	owner: string;
	metric_type: string;
	value: number;
	unit: string;
	measured_at: string;
	notes?: string;
	created_at: string;
}
```

### API Client
```typescript
// lib/utils/api.ts
export class APIError extends Error {
	constructor(message: string, public status: number, public data?: unknown) {
		super(message);
	}
}

export async function post<T>(url: string, data: unknown): Promise<T> {
	const response = await fetch(url, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(data)
	});
	if (!response.ok) throw new APIError('Request failed', response.status);
	return response.json();
}
```

### SvelteKit Actions
```typescript
import type { Actions } from './$types';
import { fail } from '@sveltejs/kit';

export const actions: Actions = {
	create: async ({ request }) => {
		const data = await request.formData();
		const value = parseFloat(data.get('value') as string);
		if (isNaN(value)) return fail(400, { error: 'Invalid value' });

		try {
			await post('/api/health-metrics', {
				metric_type: data.get('metric_type'),
				value,
				unit: data.get('unit'),
				measured_at: new Date().toISOString()
			});
			return { success: true };
		} catch (_error) {
			return fail(400, { error: 'Failed to create' });
		}
	}
};
```

### Import Order
```typescript
// 1. SvelteKit, 2. Local components, 3. Utils/types, 4. Third-party
import { page } from '$app/state';
import MetricCard from '$lib/components/MetricCard.svelte';
import { formatDate } from '$lib/utils/formatters';
import type { HealthMetric } from '$lib/types';
```

## Testing

### Backend (pytest)
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_health_metric():
    response = client.post("/api/health-metrics", json={
        "metric_type": "blood_pressure_systolic",
        "value": 120,
        "unit": "mmHg",
        "measured_at": "2024-01-15T10:00:00Z"
    })
    assert response.status_code == 200
    assert response.json()["value"] == 120
```

**Commands:**
```bash
cd backend && pytest --cov=app --cov-report=xml
```

### Frontend (vitest)
```typescript
import { describe, it, expect } from 'vitest';
import { formatDate } from '$lib/utils/formatters';

describe('formatDate', () => {
	it('formats correctly', () => {
		expect(formatDate('2024-01-15')).toBe('Jan 15, 2024');
	});
});
```

**Commands:**
```bash
cd frontend && npm run test:coverage
```

**Coverage:** 80% minimum (CI enforced), write tests with features not after

## Simplicity Principles

### NEVER
❌ Over-engineer, premature abstractions
❌ Create UI components (use ../home-ui)
❌ Placeholders/TODOs
❌ Skip linter errors with disable directives
❌ Use `any` type
❌ Omit type hints
❌ Add unrequested features

### ALWAYS
✅ Use home-ui: Button, Input, Select, Modal, Card, Badge
✅ Follow existing patterns
✅ Three similar lines > abstraction
✅ Complete working code
✅ Fix linter errors properly (research, ask if stuck)

## Code Generation

**Strategy:** Incremental (20-50 lines), one logical unit, complete working code
**NEVER:** >100 lines at once, placeholders (`// ... rest`), modify unrelated code
**ALWAYS:** Follow patterns, write tests, run linter, verify works

## Commands

### Mise
```bash
mise dev              # docker compose up
mise dev:build        # docker compose up --build
mise down             # docker compose down
mise install          # uv sync && npm install
```

### Backend
```bash
cd backend
uv sync                                    # Install deps
alembic upgrade head                       # Migrations
uvicorn app.main:app --reload              # Dev (8000)
pytest --cov=app --cov-report=xml          # Tests
ruff check backend/ && ruff format backend/
```

### Frontend
```bash
cd frontend
npm install && npm run dev                 # Dev (5173)
npm run build && npm run preview           # Build
npm run lint && npm run check              # Lint + types
npm run test:coverage                      # Tests
```

### Docker
```bash
docker-compose up postgres -d              # DB only (5433)
docker-compose up                          # All services
```

## Domain Patterns

### Entities
- **HealthMetric:** Vitals (BP = 2 metrics: systolic + diastolic with same timestamp)
- **Medication/Supplement:** Active tracking, refill warnings
- **LabResult → LabResultValue:** One-to-many (CBC has multiple values)
- **HealthGoal:** Progress tracking
- **Vaccination:** Immunization with next due date
- **MedicalHistory:** Timeline events

**All models:** `owner` field for multi-user

### Removed Features (DO NOT suggest)
- Conditions, Symptoms, Appointments, Allergies (removed PR #14)

### UI Strategy
**Use home-ui:** Button, Input, Select, Textarea, Modal, Card, Badge
**Create only:** MetricCard, MedicationCard, LabResultCard, VaccinationCard, GoalProgressBar

### Nord Colors
```css
--nord10: #5e81ac;  /* Blue - vitals */
--nord14: #a3be8c;  /* Green - success */
--nord13: #ebcb8b;  /* Yellow - warnings */
--nord11: #bf616a;  /* Red - errors */
--nord7: #8fbcbb;   /* Teal - medications */
```

## Git

### Branches
`{type}/{description}` - Examples: `feat/add-chart`, `fix/validation`

### Commits
```bash
git commit -s -S -m "$(cat <<'EOF'
feat: add blood pressure trend chart

- Implement ECharts line chart for BP history
- Add date range filter (7/30/90 days)
- Highlight abnormal readings in red
EOF
)"
```

**ALWAYS:** Sign (`-s -S`), conventional types (feat/fix/chore/test/ci/docs)
**NEVER:** Use `-F` flag, skip signing, work around hooks

## Gotchas

1. **datetime:** Use `datetime.now(UTC)` not `datetime.utcnow()` (deprecated)
2. **home-ui:** Import from ../home-ui, don't recreate Button/Input/Modal
3. **Blood pressure:** TWO metrics (systolic + diastolic), not one
4. **Linter:** Fix properly, never skip with directives
5. **DB ports:** 5433 (host), 5432 (container)
6. **Type hints:** Required everywhere in Python

## Critical Files

**Backend:**
- `/backend/app/main.py` - FastAPI app
- `/backend/app/services/crud.py` - Generic CRUD base
- `/backend/app/core/database.py` - DB session
- `/backend/pyproject.toml` - Deps, ruff config

**Frontend:**
- `/frontend/src/lib/utils/api.ts` - API client
- `/frontend/src/lib/constants.ts` - Metric types, units, lab tests
- `/frontend/src/app.css` - Nord theme
- `/frontend/src/routes/+layout.svelte` - Root layout

**Config:**
- `/.mise.toml` - Python 3.14.2, Node 24
- `/docker-compose.yml` - postgres:5433, backend:8000, frontend:5173
- `/.github/workflows/ci.yml` - CI tests, coverage
