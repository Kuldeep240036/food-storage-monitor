from datetime import datetime, timezone


def create_equipment_report(
    storage_unit_id: str,
    reporter: str,
    problem_type: str,
    description: str,
    severity: str = "Medium"
) -> dict:
    """Create a structured storage-equipment problem report."""

    if not storage_unit_id.strip():
        raise ValueError("Storage unit ID is required.")

    if not reporter.strip():
        raise ValueError("Reporter name is required.")

    if not problem_type.strip():
        raise ValueError("Problem type is required.")

    if not description.strip():
        raise ValueError("Problem description is required.")

    valid_severity = {"Low", "Medium", "High", "Critical"}
    if severity not in valid_severity:
        raise ValueError(
            f"Severity must be one of: {', '.join(sorted(valid_severity))}"
        )

    return {
        "report_id": f"EQ-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "storage_unit_id": storage_unit_id,
        "reporter": reporter,
        "problem_type": problem_type,
        "description": description.strip(),
        "severity": severity,
        "status": "OPEN"
    }


if __name__ == "__main__":
    report = create_equipment_report(
        storage_unit_id="UNIT-001",
        reporter="Staff Member",
        problem_type="Cooling malfunction",
        description="Storage unit temperature is not maintaining the expected range.",
        severity="High"
    )

    print(report)
