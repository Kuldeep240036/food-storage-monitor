from collections import Counter, defaultdict
from database import get_recent_readings


def analyse_historical_trends(readings):
    """
    Analyse historical storage readings and identify repeated problems.
    """

    if not readings:
        return {
            "total_readings": 0,
            "abnormal_readings": 0,
            "normal_readings": 0,
            "abnormal_rate": 0.0,
            "repeated_problem_units": []
        }

    total_readings = len(readings)
    abnormal_readings = 0
    normal_readings = 0
    problem_units = Counter()

    for reading in readings:
        status = str(reading.get("status", "NORMAL")).upper()
        unit_id = reading.get("unit_id", "UNKNOWN")

        if status == "ABNORMAL" or reading.get("abnormal") is True:
            abnormal_readings += 1
            problem_units[unit_id] += 1
        else:
            normal_readings += 1

    abnormal_rate = round(
        (abnormal_readings / total_readings) * 100,
        2
    )

    repeated_problem_units = [
        {
            "unit_id": unit_id,
            "problem_count": count
        }
        for unit_id, count in problem_units.items()
        if count >= 2
    ]

    return {
        "total_readings": total_readings,
        "abnormal_readings": abnormal_readings,
        "normal_readings": normal_readings,
        "abnormal_rate": abnormal_rate,
        "repeated_problem_units": repeated_problem_units
    }


def generate_historical_report():
    """
    Retrieve recent readings and generate a historical trend report.
    """

    readings = get_recent_readings(limit=100)

    report = analyse_historical_trends(readings)

    print("=" * 60)
    print("SAFESTORE HISTORICAL TREND ANALYSIS")
    print("=" * 60)

    print(f"Total readings: {report['total_readings']}")
    print(f"Normal readings: {report['normal_readings']}")
    print(f"Abnormal readings: {report['abnormal_readings']}")
    print(f"Abnormal rate: {report['abnormal_rate']}%")

    print("\nRepeated storage problems")
    print("-" * 60)

    if report["repeated_problem_units"]:
        for problem in report["repeated_problem_units"]:
            print(
                f"Unit {problem['unit_id']}: "
                f"{problem['problem_count']} abnormal readings"
            )
    else:
        print("No repeated storage problems detected.")

    return report


if __name__ == "__main__":
    generate_historical_report()
