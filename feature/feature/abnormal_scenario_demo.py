from sensor_simulator import generate_reading
from alert_management import evaluate_reading
from management_dashboard import build_dashboard


def run_demo():
    print("=" * 60)
    print("SAFESTORE ABNORMAL STORAGE CONDITION DEMONSTRATION")
    print("=" * 60)

    # Step 1: Generate an abnormal storage reading
    reading = generate_reading(
        unit_id="UNIT-DEMO-001",
        facility_id="FACILITY-DEMO-001",
        abnormal=True
    )

    print("\n1. Simulated abnormal storage condition")
    print("-" * 60)
    print(reading)

    # Step 2: Evaluate the reading and generate an alert
    alert = evaluate_reading(reading)

    print("\n2. Detection and alert response")
    print("-" * 60)
    print(alert)

    # Step 3: Present the abnormal condition through the dashboard
    dashboard = build_dashboard([reading])

    print("\n3. Management dashboard presentation")
    print("-" * 60)
    print(dashboard)

    # Step 4: Verify the complete system response
    assert alert["triggered"] is True, (
        "FAIL: abnormal storage condition did not trigger an alert."
    )

    assert len(dashboard["abnormal_readings"]) == 1, (
        "FAIL: abnormal condition was not presented on the dashboard."
    )

    print("\n" + "=" * 60)
    print("DEMONSTRATION RESULT: PASS")
    print("=" * 60)
    print(
        "Abnormal storage condition detected, "
        "alert generated and condition presented successfully."
    )


if __name__ == "__main__":
    run_demo()
