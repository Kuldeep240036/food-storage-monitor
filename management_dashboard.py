from datetime import datetime, timezone


def calculate_kpis(readings: list[dict]) -> dict:
    """Calculate management-level storage monitoring KPIs."""

    if not readings:
        return {
            "total_units": 0,
            "normal_units": 0,
            "abnormal_units": 0,
            "average_temperature": 0.0,
            "average_humidity": 0.0
        }

    total_units = len(readings)
    normal_units = sum(
        reading.get("storage_unit_status", "").upper() == "NORMAL"
        for reading in readings
    )
    abnormal_units = total_units - normal_units

    average_temperature = round(
        sum(reading["temperature"] for reading in readings) / total_units,
        2
    )

    average_humidity = round(
        sum(reading["humidity"] for reading in readings) / total_units,
        2
    )

    return {
        "total_units": total_units,
        "normal_units": normal_units,
        "abnormal_units": abnormal_units,
        "average_temperature": average_temperature,
        "average_humidity": average_humidity
    }


def build_dashboard(readings: list[dict]) -> dict:
    """Build a management dashboard summary."""

    kpis = calculate_kpis(readings)

    abnormal_readings = [
        reading for reading in readings
        if reading.get("storage_unit_status", "").upper() != "NORMAL"
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "kpis": kpis,
        "abnormal_readings": abnormal_readings
    }


def print_dashboard(dashboard: dict) -> None:
    """Display the dashboard in a management-friendly format."""

    kpis = dashboard["kpis"]

    print("\n" + "=" * 55)
    print("        SAFESTORE MANAGEMENT DASHBOARD")
    print("=" * 55)

    print(f"Generated:          {dashboard['generated_at']}")
    print(f"Total storage units:{kpis['total_units']}")
    print(f"Normal units:      {kpis['normal_units']}")
    print(f"Abnormal units:    {kpis['abnormal_units']}")
    print(f"Average temp:      {kpis['average_temperature']} °C")
    print(f"Average humidity:  {kpis['average_humidity']} %")

    print("\nAbnormal storage conditions")

    if not dashboard["abnormal_readings"]:
        print("No abnormal storage conditions detected.")
    else:
        for reading in dashboard["abnormal_readings"]:
            print(
                f"- {reading['storage_unit_id']} | "
                f"Temperature: {reading['temperature']} °C | "
                f"Humidity: {reading['humidity']} % | "
                f"Status: {reading['storage_unit_status']}"
            )

    print("=" * 55)


if __name__ == "__main__":
    sample_readings = [
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "facility_id": "FACILITY-001",
            "storage_unit_id": "UNIT-001",
            "temperature": 5.8,
            "humidity": 52.0,
            "storage_unit_status": "NORMAL"
        },
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "facility_id": "FACILITY-001",
            "storage_unit_id": "UNIT-002",
            "temperature": 10.7,
            "humidity": 73.5,
            "storage_unit_status": "ABNORMAL"
        }
    ]

    dashboard = build_dashboard(sample_readings)
    print_dashboard(dashboard)
