from datetime import datetime, timezone


def display_reading(reading: dict) -> None:
    print("\n--- Storage Reading ---")
    print(f"Time:          {reading.get('timestamp', 'N/A')}")
    print(f"Facility:      {reading.get('facility_id', 'N/A')}")
    print(f"Storage unit:  {reading.get('storage_unit_id', 'N/A')}")
    print(f"Temperature:   {reading.get('temperature', 'N/A')} °C")
    print(f"Humidity:      {reading.get('humidity', 'N/A')} %")
    print(f"Status:        {reading.get('storage_unit_status', 'N/A')}")


def create_inspection(
    storage_unit_id: str,
    inspector: str,
    condition: str,
    notes: str = ""
) -> dict:
    return {
        "inspection_id": (
            f"INS-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        ),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "storage_unit_id": storage_unit_id,
        "inspector": inspector,
        "condition": condition,
        "notes": notes
    }


def create_equipment_report(
    storage_unit_id: str,
    reporter: str,
    problem: str,
    severity: str = "Medium"
) -> dict:
    return {
        "report_id": (
            f"EQ-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        ),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "storage_unit_id": storage_unit_id,
        "reporter": reporter,
        "problem": problem,
        "severity": severity,
        "status": "OPEN"
    }


def show_menu() -> None:
    print("\n=== SafeStore Staff Application ===")
    print("1. View storage reading")
    print("2. Record storage inspection")
    print("3. Report equipment problem")
    print("4. Exit")


def main() -> None:
    sample_reading = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "facility_id": "FACILITY-001",
        "storage_unit_id": "UNIT-001",
        "temperature": 6.2,
        "humidity": 54.5,
        "storage_unit_status": "NORMAL"
    }

    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            display_reading(sample_reading)

        elif choice == "2":
            unit_id = input("Storage unit ID: ").strip()
            inspector = input("Inspector name: ").strip()
            condition = input("Condition: ").strip()
            notes = input("Notes: ").strip()

            inspection = create_inspection(
                unit_id,
                inspector,
                condition,
                notes
            )

            print("\nInspection recorded:")
            print(inspection)

        elif choice == "3":
            unit_id = input("Storage unit ID: ").strip()
            reporter = input("Reporter name: ").strip()
            problem = input("Problem description: ").strip()
            severity = input(
                "Severity [Low/Medium/High/Critical]: "
            ).strip() or "Medium"

            report = create_equipment_report(
                unit_id,
                reporter,
                problem,
                severity
            )

            print("\nEquipment problem reported:")
            print(report)

        elif choice == "4":
            print("SafeStore staff application closed.")
            break

        else:
            print("Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()
