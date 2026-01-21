"""Apple Health data parser for XML exports and Health Auto Export JSON."""

import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any

from app.schemas.health_metric import HealthMetricCreate

AGGREGATE_METRICS = {"heart_rate", "steps", "hrv", "respiratory_rate", "walking_heart_rate"}
SUM_METRICS = {"steps"}

APPLE_HEALTH_TYPE_MAP: dict[str, tuple[str, str]] = {
    "HKQuantityTypeIdentifierHeartRate": ("heart_rate", "bpm"),
    "HKQuantityTypeIdentifierBodyMass": ("weight", "kg"),
    "HKQuantityTypeIdentifierBloodPressureSystolic": ("blood_pressure_systolic", "mmHg"),
    "HKQuantityTypeIdentifierBloodPressureDiastolic": ("blood_pressure_diastolic", "mmHg"),
    "HKQuantityTypeIdentifierBloodGlucose": ("glucose", "mg/dL"),
    "HKQuantityTypeIdentifierOxygenSaturation": ("spo2", "%"),
    "HKQuantityTypeIdentifierBodyTemperature": ("temperature", "°C"),
    "HKQuantityTypeIdentifierStepCount": ("steps", "steps"),
    "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": ("hrv", "ms"),
    "HKQuantityTypeIdentifierHeight": ("height", "cm"),
    "HKQuantityTypeIdentifierBodyFatPercentage": ("body_fat_percentage", "%"),
    "HKQuantityTypeIdentifierRespiratoryRate": ("respiratory_rate", "breaths/min"),
    "HKQuantityTypeIdentifierRestingHeartRate": ("resting_heart_rate", "bpm"),
    "HKQuantityTypeIdentifierVO2Max": ("vo2_max", "mL/kg/min"),
    "HKQuantityTypeIdentifierWalkingHeartRateAverage": ("walking_heart_rate", "bpm"),
}

HEALTH_AUTO_EXPORT_TYPE_MAP: dict[str, tuple[str, str]] = {
    "heart_rate": ("heart_rate", "bpm"),
    "weight_body_mass": ("weight", "kg"),
    "blood_pressure_systolic": ("blood_pressure_systolic", "mmHg"),
    "blood_pressure_diastolic": ("blood_pressure_diastolic", "mmHg"),
    "blood_glucose": ("glucose", "mg/dL"),
    "oxygen_saturation": ("spo2", "%"),
    "body_temperature": ("temperature", "°C"),
    "step_count": ("steps", "steps"),
    "heart_rate_variability": ("hrv", "ms"),
    "height": ("height", "cm"),
    "body_fat_percentage": ("body_fat_percentage", "%"),
    "respiratory_rate": ("respiratory_rate", "breaths/min"),
    "resting_heart_rate": ("resting_heart_rate", "bpm"),
    "vo2_max": ("vo2_max", "mL/kg/min"),
    "walking_heart_rate_average": ("walking_heart_rate", "bpm"),
    "sleep_analysis": ("sleep_hours", "hours"),
}


class AppleHealthParser:
    """Parser for Apple Health data from various sources."""

    def parse_xml(
        self, content: bytes, owner: str, aggregate_days: int = 30
    ) -> list[HealthMetricCreate]:
        """Parse Apple Health export XML file with aggregation for old data.

        Args:
            content: XML file content
            owner: Owner identifier
            aggregate_days: Data older than this many days gets aggregated to daily values.
                           Set to 0 to disable aggregation.
        """
        metrics: list[HealthMetricCreate] = []
        to_aggregate: dict[str, dict[str, list[float]]] = defaultdict(
            lambda: defaultdict(list)
        )
        cutoff = datetime.now(UTC) - timedelta(days=aggregate_days) if aggregate_days > 0 else None

        root = ET.fromstring(content)

        for record in root.iter("Record"):
            metric = self._parse_xml_record(record, owner)
            if not metric:
                continue

            if (
                cutoff
                and metric.metric_type in AGGREGATE_METRICS
                and metric.measured_at.replace(tzinfo=UTC) < cutoff
            ):
                day_key = metric.measured_at.strftime("%Y-%m-%d")
                to_aggregate[metric.metric_type][day_key].append(metric.value)
            else:
                metrics.append(metric)

        for metric_type, daily_values in to_aggregate.items():
            mapping = next(
                (v for k, v in APPLE_HEALTH_TYPE_MAP.items() if v[0] == metric_type), None
            )
            if not mapping:
                continue
            _, unit = mapping

            for day_str, values in daily_values.items():
                if metric_type in SUM_METRICS:
                    agg_value = round(sum(values), 2)
                else:
                    agg_value = round(sum(values) / len(values), 2)

                measured_at = datetime.strptime(day_str, "%Y-%m-%d").replace(
                    hour=12, tzinfo=UTC
                )
                metrics.append(
                    HealthMetricCreate(
                        metric_type=metric_type,
                        value=agg_value,
                        unit=unit,
                        measured_at=measured_at,
                        owner=owner,
                        source="apple_health_import",
                    )
                )

        return metrics

    def _parse_xml_record(
        self, record: ET.Element, owner: str
    ) -> HealthMetricCreate | None:
        """Parse a single Record element from Apple Health XML."""
        record_type = record.get("type", "")
        mapping = APPLE_HEALTH_TYPE_MAP.get(record_type)

        if not mapping:
            return None

        metric_type, default_unit = mapping

        try:
            value = float(record.get("value", "0"))
        except ValueError:
            return None

        unit = record.get("unit", default_unit)
        value, unit = self._convert_unit(value, unit, default_unit)

        start_date_str = record.get("startDate", "")
        if not start_date_str:
            return None

        measured_at = self._parse_apple_date(start_date_str)
        if not measured_at:
            return None

        return HealthMetricCreate(
            metric_type=metric_type,
            value=value,
            unit=unit,
            measured_at=measured_at,
            owner=owner,
            source="apple_health_import",
        )

    def parse_auto_export_json(
        self, data: dict[str, Any], owner: str
    ) -> list[HealthMetricCreate]:
        """Parse Health Auto Export JSON payload."""
        metrics: list[HealthMetricCreate] = []

        data_section = data.get("data", data)
        if isinstance(data_section, dict):
            metrics_data = data_section.get("metrics", [])
        else:
            metrics_data = []

        for metric_data in metrics_data:
            parsed = self._parse_auto_export_metric(metric_data, owner)
            metrics.extend(parsed)

        return metrics

    def _parse_auto_export_metric(
        self, metric_data: dict[str, Any], owner: str
    ) -> list[HealthMetricCreate]:
        """Parse a single metric from Health Auto Export JSON."""
        results: list[HealthMetricCreate] = []

        name = metric_data.get("name", "")
        mapping = HEALTH_AUTO_EXPORT_TYPE_MAP.get(name.lower().replace(" ", "_"))

        if not mapping:
            return results

        metric_type, default_unit = mapping
        unit = metric_data.get("units", default_unit)

        for data_point in metric_data.get("data", []):
            value = data_point.get("qty")
            if value is None:
                value = data_point.get("value")
            if value is None:
                continue

            try:
                value = float(value)
            except (ValueError, TypeError):
                continue

            date_str = data_point.get("date", "")
            if not date_str:
                continue

            measured_at = self._parse_iso_date(date_str)
            if not measured_at:
                continue

            value, unit = self._convert_unit(value, unit, default_unit)

            results.append(
                HealthMetricCreate(
                    metric_type=metric_type,
                    value=value,
                    unit=unit,
                    measured_at=measured_at,
                    owner=owner,
                    source="apple_health_webhook",
                )
            )

        return results

    def _parse_apple_date(self, date_str: str) -> datetime | None:
        """Parse Apple Health XML date format."""
        formats = [
            "%Y-%m-%d %H:%M:%S %z",
            "%Y-%m-%d %H:%M:%S",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

    def _parse_iso_date(self, date_str: str) -> datetime | None:
        """Parse ISO format date string."""
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            return None

    def _convert_unit(
        self, value: float, source_unit: str, target_unit: str
    ) -> tuple[float, str]:
        """Convert value to target unit if needed."""
        source_lower = source_unit.lower()
        target_lower = target_unit.lower()

        if source_lower == target_lower:
            return value, target_unit

        if source_lower == "lb" and target_lower == "kg":
            return round(value * 0.453592, 2), target_unit
        if source_lower == "kg" and target_lower == "lb":
            return round(value / 0.453592, 2), target_unit
        if source_lower == "in" and target_lower == "cm":
            return round(value * 2.54, 2), target_unit
        if source_lower == "cm" and target_lower == "in":
            return round(value / 2.54, 2), target_unit
        if source_lower == "f" and target_lower == "°c":
            return round((value - 32) * 5 / 9, 2), target_unit
        if source_lower == "°c" and target_lower == "f":
            return round(value * 9 / 5 + 32, 2), target_unit

        return value, source_unit


apple_health_parser = AppleHealthParser()
