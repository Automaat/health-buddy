from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_health_metric():
    response = client.post(
        "/api/health-metrics",
        json={
            "metric_type": "blood_pressure_systolic",
            "value": 120.0,
            "unit": "mmHg",
            "measured_at": "2024-01-15T10:00:00Z",
            "owner": "test_user",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["metric_type"] == "blood_pressure_systolic"
    assert data["value"] == 120.0
    assert data["unit"] == "mmHg"
    assert data["owner"] == "test_user"
    assert "id" in data


def test_get_health_metric():
    # Create a metric first
    create_response = client.post(
        "/api/health-metrics",
        json={
            "metric_type": "heart_rate",
            "value": 72.0,
            "unit": "bpm",
            "measured_at": "2024-01-15T10:00:00Z",
            "owner": "test_user",
        },
    )
    metric_id = create_response.json()["id"]

    # Get the metric
    response = client.get(f"/api/health-metrics/{metric_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == metric_id
    assert data["metric_type"] == "heart_rate"
    assert data["value"] == 72.0


def test_get_health_metric_not_found():
    response = client.get("/api/health-metrics/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Health metric not found"


def test_list_health_metrics():
    # Create multiple metrics
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
    client.post(
        "/api/health-metrics",
        json={
            "metric_type": "weight",
            "value": 80.0,
            "unit": "kg",
            "measured_at": "2024-01-16T10:00:00Z",
            "owner": "user2",
        },
    )

    # List all metrics
    response = client.get("/api/health-metrics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_list_health_metrics_with_owner_filter():
    # Create metrics for different owners
    client.post(
        "/api/health-metrics",
        json={
            "metric_type": "glucose",
            "value": 95.0,
            "unit": "mg/dL",
            "measured_at": "2024-01-15T10:00:00Z",
            "owner": "alice",
        },
    )
    client.post(
        "/api/health-metrics",
        json={
            "metric_type": "glucose",
            "value": 100.0,
            "unit": "mg/dL",
            "measured_at": "2024-01-16T10:00:00Z",
            "owner": "bob",
        },
    )

    # Filter by owner
    response = client.get("/api/health-metrics?owner=alice")
    assert response.status_code == 200
    data = response.json()
    assert all(metric["owner"] == "alice" for metric in data)


def test_update_health_metric():
    # Create a metric
    create_response = client.post(
        "/api/health-metrics",
        json={
            "metric_type": "temperature",
            "value": 36.5,
            "unit": "°C",
            "measured_at": "2024-01-15T10:00:00Z",
            "owner": "test_user",
        },
    )
    metric_id = create_response.json()["id"]

    # Update the metric
    response = client.patch(
        f"/api/health-metrics/{metric_id}",
        json={"value": 37.0, "notes": "Updated measurement"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == 37.0
    assert data["notes"] == "Updated measurement"


def test_update_health_metric_not_found():
    response = client.patch("/api/health-metrics/99999", json={"value": 100.0})
    assert response.status_code == 404
    assert response.json()["detail"] == "Health metric not found"


def test_delete_health_metric():
    # Create a metric
    create_response = client.post(
        "/api/health-metrics",
        json={
            "metric_type": "spo2",
            "value": 98.0,
            "unit": "%",
            "measured_at": "2024-01-15T10:00:00Z",
            "owner": "test_user",
        },
    )
    metric_id = create_response.json()["id"]

    # Delete the metric
    response = client.delete(f"/api/health-metrics/{metric_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == metric_id

    # Verify it's deleted
    get_response = client.get(f"/api/health-metrics/{metric_id}")
    assert get_response.status_code == 404


def test_delete_health_metric_not_found():
    response = client.delete("/api/health-metrics/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Health metric not found"
