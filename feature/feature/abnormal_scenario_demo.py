from datetime import datetime, timezone

from sensor_simulator import generate_reading
from alert_management import evaluate_reading
from management_dashboard import build_dashboard


def run_demo():
    print("=" * 60)
    print("SAFESTORE ABNORMAL STORAGE CONDITION DEMONSTRATION")
    print("=" * 60)

    reading = generate_reading(
        unit_id="UNIT-DEMO-001",
        facility_id="FACILITY-DEMO-001",
        abnormal=True
    )

    print("\n1. Simulated abnormal storage condition")
    print(reading)

    alert = evaluate_reading(reading)

    print("\n2. Detection and alert response")
    print(alert)

    dashboard = build_dashboard([reading])

    print("\n3. Management presentation")
    print(dashboard)

    assert alert["triggered"] is True
    assert len(dashboard["abnormal_readings"]) == 1

    print("\nDEMONSTRATION RESULT: PASS")
    print("Abnormal condition detected, alerted and presented successfully.")


if __name__ == "__main__":
    run_demo()
