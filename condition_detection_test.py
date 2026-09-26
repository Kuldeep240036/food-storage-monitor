# condition_detection_test.py
# SCRUM-12: Tests for abnormal storage condition detection

from condition_detection import detect_abnormal_condition


# Test 1: Normal storage condition
normal_reading = {
    "unit_id": "UNIT-001",
    "temperature": 6.0,
    "humidity": 55.0,
    "status": "NORMAL"
}

result = detect_abnormal_condition(normal_reading)

assert result["abnormal"] is False
assert result["violations"] == []
assert result["risk_level"] == "LOW"


# Test 2: Abnormal temperature
high_temperature = {
    "unit_id": "UNIT-002",
    "temperature": 12.0,
    "humidity": 55.0,
    "status": "NORMAL"
}

result = detect_abnormal_condition(high_temperature)

assert result["abnormal"] is True
assert len(result["violations"]) == 1
assert result["risk_level"] == "MEDIUM"


# Test 3: Abnormal humidity
high_humidity = {
    "unit_id": "UNIT-003",
    "temperature": 6.0,
    "humidity": 80.0,
    "status": "NORMAL"
}

result = detect_abnormal_condition(high_humidity)

assert result["abnormal"] is True
assert len(result["violations"]) == 1
assert result["risk_level"] == "MEDIUM"


# Test 4: Abnormal storage-unit status
abnormal_status = {
    "unit_id": "UNIT-004",
    "temperature": 6.0,
    "humidity": 55.0,
    "status": "FAULT"
}

result = detect_abnormal_condition(abnormal_status)

assert result["abnormal"] is True
assert len(result["violations"]) == 1
assert result["risk_level"] == "MEDIUM"


# Test 5: Multiple abnormal conditions
multiple_problems = {
    "unit_id": "UNIT-005",
    "temperature": 12.0,
    "humidity": 80.0,
    "status": "FAULT"
}

result = detect_abnormal_condition(multiple_problems)

assert result["abnormal"] is True
assert len(result["violations"]) == 3
assert result["risk_level"] == "CRITICAL"
assert result["severity"] == 100


print("All SCRUM-12 condition detection tests passed.")
