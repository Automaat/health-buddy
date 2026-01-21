"""Tests for Apple Health parser service."""

import pytest

from app.services.apple_health_parser import AppleHealthParser


@pytest.fixture
def parser():
    return AppleHealthParser()


class TestParseXml:
    """Tests for XML parsing."""

    def test_parse_heart_rate_record(self, parser: AppleHealthParser):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <HealthData>
            <Record type="HKQuantityTypeIdentifierHeartRate"
                    value="72"
                    unit="count/min"
                    startDate="2024-01-15 10:00:00 +0000" />
        </HealthData>"""

        metrics = parser.parse_xml(xml_content, "test_user")

        assert len(metrics) == 1
        assert metrics[0].metric_type == "heart_rate"
        assert metrics[0].value == 72.0
        assert metrics[0].owner == "test_user"
        assert metrics[0].source == "apple_health_import"

    def test_parse_weight_record(self, parser: AppleHealthParser):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <HealthData>
            <Record type="HKQuantityTypeIdentifierBodyMass"
                    value="75.5"
                    unit="kg"
                    startDate="2024-01-15 10:00:00 +0000" />
        </HealthData>"""

        metrics = parser.parse_xml(xml_content, "test_user")

        assert len(metrics) == 1
        assert metrics[0].metric_type == "weight"
        assert metrics[0].value == 75.5
        assert metrics[0].unit == "kg"

    def test_parse_blood_pressure_records(self, parser: AppleHealthParser):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <HealthData>
            <Record type="HKQuantityTypeIdentifierBloodPressureSystolic"
                    value="120"
                    unit="mmHg"
                    startDate="2024-01-15 10:00:00 +0000" />
            <Record type="HKQuantityTypeIdentifierBloodPressureDiastolic"
                    value="80"
                    unit="mmHg"
                    startDate="2024-01-15 10:00:00 +0000" />
        </HealthData>"""

        metrics = parser.parse_xml(xml_content, "test_user")

        assert len(metrics) == 2
        systolic = next(m for m in metrics if m.metric_type == "blood_pressure_systolic")
        diastolic = next(m for m in metrics if m.metric_type == "blood_pressure_diastolic")

        assert systolic.value == 120.0
        assert diastolic.value == 80.0

    def test_parse_skips_unknown_types(self, parser: AppleHealthParser):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <HealthData>
            <Record type="HKQuantityTypeIdentifierUnknownType"
                    value="100"
                    unit="units"
                    startDate="2024-01-15 10:00:00 +0000" />
        </HealthData>"""

        metrics = parser.parse_xml(xml_content, "test_user")
        assert len(metrics) == 0

    def test_parse_multiple_records(self, parser: AppleHealthParser):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <HealthData>
            <Record type="HKQuantityTypeIdentifierHeartRate"
                    value="70"
                    unit="count/min"
                    startDate="2024-01-15 10:00:00 +0000" />
            <Record type="HKQuantityTypeIdentifierHeartRate"
                    value="72"
                    unit="count/min"
                    startDate="2024-01-15 11:00:00 +0000" />
            <Record type="HKQuantityTypeIdentifierStepCount"
                    value="5000"
                    unit="count"
                    startDate="2024-01-15 12:00:00 +0000" />
        </HealthData>"""

        metrics = parser.parse_xml(xml_content, "test_user")

        assert len(metrics) == 3
        heart_rate_metrics = [m for m in metrics if m.metric_type == "heart_rate"]
        step_metrics = [m for m in metrics if m.metric_type == "steps"]

        assert len(heart_rate_metrics) == 2
        assert len(step_metrics) == 1

    def test_parse_handles_invalid_value(self, parser: AppleHealthParser):
        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
        <HealthData>
            <Record type="HKQuantityTypeIdentifierHeartRate"
                    value="invalid"
                    unit="count/min"
                    startDate="2024-01-15 10:00:00 +0000" />
        </HealthData>"""

        metrics = parser.parse_xml(xml_content, "test_user")
        assert len(metrics) == 0


class TestParseAutoExportJson:
    """Tests for Health Auto Export JSON parsing."""

    def test_parse_heart_rate_metric(self, parser: AppleHealthParser):
        data = {
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

        metrics = parser.parse_auto_export_json(data, "test_user")

        assert len(metrics) == 1
        assert metrics[0].metric_type == "heart_rate"
        assert metrics[0].value == 72.0
        assert metrics[0].source == "apple_health_webhook"

    def test_parse_weight_metric(self, parser: AppleHealthParser):
        data = {
            "data": {
                "metrics": [
                    {
                        "name": "weight_body_mass",
                        "units": "kg",
                        "data": [{"date": "2024-01-15T10:00:00Z", "qty": 75.5}],
                    }
                ]
            }
        }

        metrics = parser.parse_auto_export_json(data, "test_user")

        assert len(metrics) == 1
        assert metrics[0].metric_type == "weight"
        assert metrics[0].value == 75.5

    def test_parse_multiple_data_points(self, parser: AppleHealthParser):
        data = {
            "data": {
                "metrics": [
                    {
                        "name": "step_count",
                        "units": "steps",
                        "data": [
                            {"date": "2024-01-15T10:00:00Z", "qty": 5000},
                            {"date": "2024-01-16T10:00:00Z", "qty": 6000},
                            {"date": "2024-01-17T10:00:00Z", "qty": 7000},
                        ],
                    }
                ]
            }
        }

        metrics = parser.parse_auto_export_json(data, "test_user")

        assert len(metrics) == 3
        assert all(m.metric_type == "steps" for m in metrics)
        assert [m.value for m in metrics] == [5000.0, 6000.0, 7000.0]

    def test_parse_skips_unknown_metric_names(self, parser: AppleHealthParser):
        data = {
            "data": {
                "metrics": [
                    {
                        "name": "unknown_metric",
                        "units": "units",
                        "data": [{"date": "2024-01-15T10:00:00Z", "qty": 100}],
                    }
                ]
            }
        }

        metrics = parser.parse_auto_export_json(data, "test_user")
        assert len(metrics) == 0

    def test_parse_handles_value_field(self, parser: AppleHealthParser):
        data = {
            "data": {
                "metrics": [
                    {
                        "name": "heart_rate",
                        "units": "bpm",
                        "data": [{"date": "2024-01-15T10:00:00Z", "value": 72}],
                    }
                ]
            }
        }

        metrics = parser.parse_auto_export_json(data, "test_user")

        assert len(metrics) == 1
        assert metrics[0].value == 72.0


class TestUnitConversion:
    """Tests for unit conversion."""

    def test_convert_lb_to_kg(self, parser: AppleHealthParser):
        value, unit = parser._convert_unit(150.0, "lb", "kg")
        assert round(value, 2) == 68.04
        assert unit == "kg"

    def test_convert_in_to_cm(self, parser: AppleHealthParser):
        value, unit = parser._convert_unit(70.0, "in", "cm")
        assert round(value, 2) == 177.8
        assert unit == "cm"

    def test_convert_f_to_c(self, parser: AppleHealthParser):
        value, unit = parser._convert_unit(98.6, "F", "°C")
        assert round(value, 2) == 37.0
        assert unit == "°C"

    def test_same_unit_no_conversion(self, parser: AppleHealthParser):
        value, unit = parser._convert_unit(100.0, "kg", "kg")
        assert value == 100.0
        assert unit == "kg"

    def test_unknown_units_returns_original(self, parser: AppleHealthParser):
        value, unit = parser._convert_unit(100.0, "unknown1", "unknown2")
        assert value == 100.0
        assert unit == "unknown1"
