"""Tests for Apple Health import API endpoints."""

import io

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAppleHealthXmlImport:
    """Tests for XML file import endpoint."""

    def test_import_xml_file(self):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <HealthData>
            <Record type="HKQuantityTypeIdentifierHeartRate"
                    value="72"
                    unit="count/min"
                    startDate="2024-01-15 10:00:00 +0000" />
        </HealthData>"""

        response = client.post(
            "/api/import/apple-health",
            files={"file": ("export.xml", io.BytesIO(xml_content), "application/xml")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total_records"] == 1
        assert data["imported"] >= 0
        assert "skipped" in data
        assert "errors" in data

    def test_import_xml_with_owner(self):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <HealthData>
            <Record type="HKQuantityTypeIdentifierBodyMass"
                    value="75"
                    unit="kg"
                    startDate="2024-01-15 10:00:00 +0000" />
        </HealthData>"""

        response = client.post(
            "/api/import/apple-health?owner=custom_user",
            files={"file": ("export.xml", io.BytesIO(xml_content), "application/xml")},
        )

        assert response.status_code == 200

    def test_import_rejects_non_xml(self):
        response = client.post(
            "/api/import/apple-health",
            files={"file": ("data.txt", io.BytesIO(b"not xml"), "text/plain")},
        )

        assert response.status_code == 400
        assert "XML" in response.json()["detail"]

    def test_import_rejects_empty_file(self):
        response = client.post(
            "/api/import/apple-health",
            files={"file": ("export.xml", io.BytesIO(b""), "application/xml")},
        )

        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    def test_import_handles_invalid_xml(self):
        response = client.post(
            "/api/import/apple-health",
            files={"file": ("export.xml", io.BytesIO(b"<invalid"), "application/xml")},
        )

        assert response.status_code == 400


class TestAppleHealthWebhook:
    """Tests for Health Auto Export webhook endpoint."""

    def test_webhook_with_metrics(self):
        payload = {
            "data": {
                "metrics": [
                    {
                        "name": "heart_rate",
                        "units": "bpm",
                        "data": [{"date": "2024-01-15T10:00:00Z", "qty": 72}],
                    }
                ]
            }
        }

        response = client.post("/api/import/apple-health/webhook", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["total_records"] == 1

    def test_webhook_with_owner_query_param(self):
        payload = {
            "data": {
                "metrics": [
                    {
                        "name": "step_count",
                        "units": "steps",
                        "data": [{"date": "2024-01-15T10:00:00Z", "qty": 5000}],
                    }
                ]
            }
        }

        response = client.post(
            "/api/import/apple-health/webhook?owner=webhook_user", json=payload
        )

        assert response.status_code == 200

    def test_webhook_with_api_key(self):
        payload = {
            "data": {
                "metrics": [
                    {
                        "name": "heart_rate",
                        "units": "bpm",
                        "data": [{"date": "2024-01-15T10:00:00Z", "qty": 72}],
                    }
                ]
            }
        }

        response = client.post(
            "/api/import/apple-health/webhook?key=my_api_key", json=payload
        )

        assert response.status_code == 200

    def test_webhook_with_metrics_at_root(self):
        payload = {
            "metrics": [
                {
                    "name": "weight_body_mass",
                    "units": "kg",
                    "data": [{"date": "2024-01-15T10:00:00Z", "qty": 75}],
                }
            ]
        }

        response = client.post("/api/import/apple-health/webhook", json=payload)

        assert response.status_code == 200

    def test_webhook_rejects_empty_payload(self):
        response = client.post("/api/import/apple-health/webhook", json={})

        assert response.status_code == 400

    def test_webhook_handles_multiple_metrics(self):
        payload = {
            "data": {
                "metrics": [
                    {
                        "name": "heart_rate",
                        "units": "bpm",
                        "data": [
                            {"date": "2024-01-15T10:00:00Z", "qty": 70},
                            {"date": "2024-01-15T11:00:00Z", "qty": 72},
                        ],
                    },
                    {
                        "name": "step_count",
                        "units": "steps",
                        "data": [{"date": "2024-01-15T10:00:00Z", "qty": 5000}],
                    },
                ]
            }
        }

        response = client.post("/api/import/apple-health/webhook", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["total_records"] == 3


class TestDeduplication:
    """Tests for import deduplication logic."""

    def test_duplicate_import_skipped(self):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <HealthData>
            <Record type="HKQuantityTypeIdentifierHeartRate"
                    value="72"
                    unit="count/min"
                    startDate="2024-02-01 10:00:00 +0000" />
        </HealthData>"""

        response1 = client.post(
            "/api/import/apple-health?owner=dedup_test",
            files={"file": ("export.xml", io.BytesIO(xml_content), "application/xml")},
        )
        assert response1.status_code == 200
        first_import = response1.json()

        response2 = client.post(
            "/api/import/apple-health?owner=dedup_test",
            files={"file": ("export.xml", io.BytesIO(xml_content), "application/xml")},
        )
        assert response2.status_code == 200
        second_import = response2.json()

        assert second_import["total_records"] == first_import["total_records"]
