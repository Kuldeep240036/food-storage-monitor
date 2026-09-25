from sensor_simulator import generate_reading
from database import initialise_database, save_reading, get_recent_readings
from alert_management import evaluate_reading
from management_dashboard import build_dashboard


def main():
    print("Starting SafeStore integration test...")

    # 1. Initialise the database.
    initialise_database()

    # 2. Generate an abnormal storage reading.
    reading = generate_reading(
        unit_id="UNIT-TEST-001",
        facility_id="FACILITY-TEST-001",
        abnormal=True
    )

    print("Generated reading:", reading)

    # 3. Store the reading.
    save_reading(reading)

    # 4. Evaluate the reading for abnormal conditions.
    alert = evaluate_reading(reading)

    print("Alert result:", alert)

    # 5. Confirm the reading can be retrieved.
    recent_readings = get_recent_readings(limit=10)

    assert len(recent_readings) > 0, (
        "Database test failed: no readings were retrieved."
    )

    # 6. Build the management dashboard from the same reading.
    dashboard = build_dashboard([reading])

    assert dashboard["kpis"]["total_units"] == 1, (
        "Dashboard test failed: incorrect unit count."
    )

    assert alert["triggered"] is True, (
        "Alert test failed: abnormal reading did not trigger an alert."
    )

    print("Database integration: PASS")
    print("Alert detection: PASS")
    print("Dashboard generation: PASS")
    print("SafeStore integration test completed successfully.")


if __name__ == "__main__":
    main()
