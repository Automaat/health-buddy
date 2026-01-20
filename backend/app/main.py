from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    config,
    dashboard,
    goals,
    health_metrics,
    lab_results,
    medical_history,
    medications,
    supplements,
    vaccinations,
)
from app.core.config import settings

app = FastAPI(
    title="Health Buddy API",
    description="Health tracking application backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix=settings.api_prefix)
app.include_router(health_metrics.router, prefix=settings.api_prefix)
app.include_router(medications.router, prefix=settings.api_prefix)
app.include_router(supplements.router, prefix=settings.api_prefix)
app.include_router(lab_results.router, prefix=settings.api_prefix)
app.include_router(goals.router, prefix=settings.api_prefix)
app.include_router(vaccinations.router, prefix=settings.api_prefix)
app.include_router(medical_history.router, prefix=settings.api_prefix)
app.include_router(config.router, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {"message": "Health Buddy API", "version": "0.1.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
