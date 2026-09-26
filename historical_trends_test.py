from historical_trends import analyse_historical_trends


readings = [
    {"unit_id": "UNIT-001", "status": "ABNORMAL"},
    {"unit_id": "UNIT-001", "status": "ABNORMAL"},
    {"unit_id": "UNIT-002", "status": "NORMAL"},
    {"unit_id": "UNIT-003", "status": "NORMAL"},
]

result = analyse_historical_trends(readings)

assert result["total_readings"] == 4
assert result["abnormal_readings"] == 2
assert result["normal_readings"] == 2
assert result["abnormal_rate"] == 50.0
assert result["repeated_problem_units"][0]["unit_id"] == "UNIT-001"

print("SCRUM-11 historical trend test: PASS")
print(result)
