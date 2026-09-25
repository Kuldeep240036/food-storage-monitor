from datetime import datetime, timezone


def create_inspection(
    storage_unit_id: str,
    inspector: str,
    condition: str,
    notes: str = ""
) -> dict:
    """
    Create a structured storage inspection record.
    """

    if not storage_unit_id.strip():
        raise ValueError("Storage unit ID is required.")

    if not inspector.strip():
        raise ValueError("Inspector name is required.")

    if not condition.strip():
        raise ValueError("Inspection condition is required.")

    return {
        "inspection_id": f"INS-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "storage_unit_id": storage_unit_id,
        "inspector": inspector,
        "condition": condition,
        "notes": notes.strip()
    }


if __name__ == "__main__":
    inspection = create_inspection(
        storage_unit_id="UNIT-001",
        inspector="Staff Member",
        condition="Normal",
        notes="Routine storage inspection completed."
    )

    print(inspection)
