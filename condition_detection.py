# condition_detection.py
# SCRUM-12: Abnormal Storage Condition Detection

DEFAULT_LIMITS = {
    "temperature": {
        "min": 2.0,
        "max": 8.0
    },
    "humidity": {
        "min": 45.0,
        "max": 65.0
    }
}


def detect_abnormal_condition(reading, limits=None):
    """
    Check a storage reading against predefined acceptable limits.

    Expected reading fields:
    - temperature
    - humidity
    - status
    - unit_id

    Returns a dictionary describing whether the condition is abnormal,
    what caused the abnormality, and the resulting risk level.
    """

    if limits is None:
        limits = DEFAULT_LIMITS

    violations = []

    temperature = reading.get("temperature")
    humidity = reading.get("humidity")
    status = str(reading.get("status", "NORMAL")).upper()
    unit_id = reading.get("unit_id", "UNKNOWN")

    # Temperature check
    if temperature is not None:
        temp_min = limits["temperature"]["min"]
        temp_max = limits["temperature"]["max"]

        if temperature < temp_min:
            violations.append(
                f"Temperature too low: {temperature}°C"
            )

        elif temperature > temp_max:
            violations.append(
                f"Temperature too high: {temperature}°C"
            )

    # Humidity check
    if humidity is not None:
        humidity_min = limits["humidity"]["min"]
        humidity_max = limits["humidity"]["max"]

        if humidity < humidity_min:
            violations.append(
                f"Humidity too low: {humidity}%"
            )

        elif humidity > humidity_max:
            violations.append(
                f"Humidity too high: {humidity}%"
            )

    # Storage-unit status check
    if status not in {"NORMAL", "OK"}:
        violations.append(
            f"Storage unit status is abnormal: {status}"
        )

    # Determine abnormal condition
    abnormal = len(violations) > 0

    # Calculate simple prototype severity
    if len(violations) == 0:
        severity = 0
        risk_level = "LOW"

    elif len(violations) == 1:
        severity = 40
        risk_level = "MEDIUM"

    elif len(violations) == 2:
        severity = 70
        risk_level = "HIGH"

    else:
        severity = 100
        risk_level = "CRITICAL"

    return {
        "unit_id": unit_id,
        "abnormal": abnormal,
        "violations": violations,
        "severity": severity,
        "risk_level": risk_level
    }


def check_storage_condition(
    unit_id,
    temperature,
    humidity,
    status="NORMAL"
):
    """
    Convenience function for checking one storage unit.
    """

    reading = {
        "unit_id": unit_id,
        "temperature": temperature,
        "humidity": humidity,
        "status": status
    }

    return detect_abnormal_condition(reading)


if __name__ == "__main__":

    # Normal example
    normal_reading = check_storage_condition(
        "UNIT-001",
        6.2,
        54.5,
        "NORMAL"
    )

    print("Normal reading:")
    print(normal_reading)

    # Abnormal example
    abnormal_reading = check_storage_condition(
        "UNIT-002",
        12.5,
        78.0,
        "NORMAL"
    )

    print("\nAbnormal reading:")
    print(abnormal_reading)
