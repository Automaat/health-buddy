from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_dashboard_data_empty():
    response = client.get("/api/dashboard?owner=test_user")
    assert response.status_code == 200
    data = response.json()
    assert "latest_metrics" in data
    assert "active_medications" in data
    assert "active_supplements" in data
    assert "recent_lab_results" in data
    assert "active_goals" in data
    assert isinstance(data["latest_metrics"], list)
    assert isinstance(data["active_medications"], list)
    assert isinstance(data["active_supplements"], list)
    assert isinstance(data["recent_lab_results"], list)
    assert isinstance(data["active_goals"], list)


def test_get_dashboard_data_with_metrics():
    # Create some health metrics
    client.post(
        "/api/health-metrics",
        json={
            "metric_type": "blood_pressure_systolic",
            "value": 120.0,
            "unit": "mmHg",
            "measured_at": "2024-01-15T10:00:00Z",
            "owner": "dashboard_user",
        },
    )
    client.post(
        "/api/health-metrics",
        json={
            "metric_type": "heart_rate",
            "value": 72.0,
            "unit": "bpm",
            "measured_at": "2024-01-15T11:00:00Z",
            "owner": "dashboard_user",
        },
    )

    # Get dashboard
    response = client.get("/api/dashboard?owner=dashboard_user")
    assert response.status_code == 200
    data = response.json()
    assert len(data["latest_metrics"]) >= 2
    # Verify metrics are for the correct owner
    for metric in data["latest_metrics"]:
        assert metric["owner"] == "dashboard_user"


def test_get_dashboard_data_with_medications():
    # Create an active medication
    client.post(
        "/api/medications",
        json={
            "name": "Aspirin",
            "dosage": "100",
            "unit": "mg",
            "frequency": "Daily",
            "start_date": "2024-01-01",
            "is_active": True,
            "owner": "med_user",
        },
    )

    # Get dashboard
    response = client.get("/api/dashboard?owner=med_user")
    assert response.status_code == 200
    data = response.json()
    assert len(data["active_medications"]) >= 1
    assert data["active_medications"][0]["name"] == "Aspirin"
    assert data["active_medications"][0]["is_active"] is True


def test_get_dashboard_data_filters_by_owner():
    # Create data for user1
    client.post(
        "/api/health-metrics",
        json={
            "metric_type": "weight",
            "value": 75.0,
            "unit": "kg",
            "measured_at": "2024-01-15T10:00:00Z",
            "owner": "user1",
        },
    )

    # Create data for user2
    client.post(
        "/api/health-metrics",
        json={
            "metric_type": "weight",
            "value": 80.0,
            "unit": "kg",
            "measured_at": "2024-01-15T10:00:00Z",
            "owner": "user2",
        },
    )

    # Get dashboard for user1
    response = client.get("/api/dashboard?owner=user1")
    assert response.status_code == 200
    data = response.json()
    # All metrics should belong to user1
    for metric in data["latest_metrics"]:
        assert metric["owner"] == "user1"
