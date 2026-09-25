from datetime import datetime, timezone


DEFAULT_TEMPERATURE_RANGE = (2.0, 8.0)
DEFAULT_HUMIDITY_RANGE = (45.0, 65.0)


def evaluate_reading(
    reading: dict,
    temperature_range: tuple[float, float] = DEFAULT_TEMPERATURE_RANGE,
    humidity_range: tuple[float, float] = DEFAULT_HUMIDITY_RANGE
) -> dict:
    """Evaluate a storage reading and generate an alert when abnormal."""

    temperature = reading["temperature"]
    humidity = reading["humidity"]
    storage_status = reading["storage_unit_status"]

    alerts = []

    if not temperature_range[0] <= temperature <= temperature_range[1]:
        alerts.append("Temperature outside expected range")

    if not humidity_range[0] <= humidity <= humidity_range[1]:
        alerts.append("Humidity outside expected range")

    if storage_status.upper() != "NORMAL":
        alerts.append("Storage unit reported an abnormal status")

    severity = "HIGH" if len(alerts) >= 2 else "MEDIUM" if alerts else "LOW"

    return {
        "alert_id": f"ALT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "facility_id": reading["facility_id"],
        "storage_unit_id": reading["storage_unit_id"],
        "triggered": bool(alerts),
        "severity": severity,
        "alerts": alerts
    }


if __name__ == "__main__":
    sample_reading = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "facility_id": "FACILITY-001",
        "storage_unit_id": "UNIT-001",
        "temperature": 11.2,
        "humidity": 75.0,
        "storage_unit_status": "ABNORMAL"
    }

    print(evaluate_reading(sample_reading))
