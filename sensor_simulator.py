import argparse
import json
import random
import time
from datetime import datetime, timezone


def generate_reading(
    unit_id: str,
    facility_id: str,
    abnormal: bool = False
) -> dict:
    """Generate a simulated storage-condition reading."""

    temperature = round(random.uniform(2.0, 8.0), 2)
    humidity = round(random.uniform(45.0, 65.0), 2)
    status = "NORMAL"

    if abnormal:
        temperature = round(
            random.choice([
                random.uniform(-2.0, 1.5),
                random.uniform(8.5, 13.0)
            ]),
            2
        )
        humidity = round(
            random.choice([
                random.uniform(20.0, 39.0),
                random.uniform(71.0, 90.0)
            ]),
            2
        )
        status = "ABNORMAL"

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "facility_id": facility_id,
        "storage_unit_id": unit_id,
        "temperature": temperature,
        "humidity": humidity,
        "storage_unit_status": status
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="SafeStore storage-condition sensor simulator"
    )
    parser.add_argument("--unit", default="UNIT-001")
    parser.add_argument("--facility", default="FACILITY-001")
    parser.add_argument("--interval", type=int, default=5)
    parser.add_argument("--abnormal", action="store_true")

    args = parser.parse_args()

    print("SafeStore Sensor Simulator")
    print(f"Facility: {args.facility}")
    print(f"Storage Unit: {args.unit}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            reading = generate_reading(
                unit_id=args.unit,
                facility_id=args.facility,
                abnormal=args.abnormal
            )

            print(json.dumps(reading))
            time.sleep(max(args.interval, 1))

    except KeyboardInterrupt:
        print("\nSensor simulator stopped.")


if __name__ == "__main__":
    main()
