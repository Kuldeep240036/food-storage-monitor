import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st

from sensor_simulator import generate_reading


# ---------------------------------------------------------
# SafeStore Dashboard
# ---------------------------------------------------------

st.set_page_config(
    page_title="FreshChoice SafeStore",
    page_icon="🌡️",
    layout="wide"
)

DB_PATH = Path("data") / "safestore.db"


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

def initialise_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                facility_id TEXT NOT NULL,
                storage_unit_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                storage_unit_status TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                storage_unit_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                risk_level TEXT NOT NULL,
                severity INTEGER NOT NULL,
                message TEXT NOT NULL
            )
            """
        )


def save_reading(reading):
    initialise_database()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO sensor_readings (
                timestamp,
                facility_id,
                storage_unit_id,
                temperature,
                humidity,
                storage_unit_status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                reading["timestamp"],
                reading["facility_id"],
                reading["storage_unit_id"],
                reading["temperature"],
                reading["humidity"],
                reading["storage_unit_status"],
            ),
        )


def save_alert(reading, risk_level, severity, message):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO alerts (
                timestamp,
                storage_unit_id,
                temperature,
                humidity,
                risk_level,
                severity,
                message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                reading["timestamp"],
                reading["storage_unit_id"],
                reading["temperature"],
                reading["humidity"],
                risk_level,
                severity,
                message,
            ),
        )


def get_readings():
    initialise_database()

    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            """
            SELECT
                timestamp,
                facility_id,
                storage_unit_id,
                temperature,
                humidity,
                storage_unit_status
            FROM sensor_readings
            ORDER BY id DESC
            """,
            conn,
        )


def get_alerts():
    initialise_database()

    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            """
            SELECT
                timestamp,
                storage_unit_id,
                temperature,
                humidity,
                risk_level,
                severity,
                message
            FROM alerts
            ORDER BY id DESC
            """,
            conn,
        )


# ---------------------------------------------------------
# CONDITION DETECTION
# ---------------------------------------------------------

def detect_condition(reading):
    violations = []

    temperature = reading["temperature"]
    humidity = reading["humidity"]
    status = reading["storage_unit_status"]

    if temperature < 2:
        violations.append(f"Temperature too low: {temperature}°C")

    elif temperature > 8:
        violations.append(f"Temperature too high: {temperature}°C")

    if humidity < 45:
        violations.append(f"Humidity too low: {humidity}%")

    elif humidity > 65:
        violations.append(f"Humidity too high: {humidity}%")

    if status != "NORMAL":
        violations.append(f"Storage unit status: {status}")

    if len(violations) == 0:
        return {
            "abnormal": False,
            "risk_level": "LOW",
            "severity": 0,
            "violations": [],
        }

    if len(violations) == 1:
        risk_level = "MEDIUM"
        severity = 40

    elif len(violations) == 2:
        risk_level = "HIGH"
        severity = 70

    else:
        risk_level = "CRITICAL"
        severity = 100

    return {
        "abnormal": True,
        "risk_level": risk_level,
        "severity": severity,
        "violations": violations,
    }


# ---------------------------------------------------------
# GENERATE SENSOR READING
# ---------------------------------------------------------

def generate_and_store(abnormal=False):
    reading = generate_reading(
        unit_id="UNIT-001",
        facility_id="FACILITY-001",
        abnormal=abnormal,
    )

    save_reading(reading)

    result = detect_condition(reading)

    if result["abnormal"]:
        message = " | ".join(result["violations"])

        save_alert(
            reading,
            result["risk_level"],
            result["severity"],
            message,
        )

    return reading, result


# ---------------------------------------------------------
# START DATABASE
# ---------------------------------------------------------

initialise_database()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("FreshChoice SafeStore")
st.caption("Smart Storage Monitoring & Risk Management System")

st.markdown(
    """
    Monitor storage conditions, detect abnormal readings,
    review alerts and analyse historical storage performance.
    """
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Sensor Controls")

if st.sidebar.button("Generate Normal Reading", use_container_width=True):
    reading, result = generate_and_store(abnormal=False)

    st.sidebar.success(
        f"Reading saved: {reading['temperature']}°C / "
        f"{reading['humidity']}% RH"
    )

if st.sidebar.button("Generate Abnormal Reading", use_container_width=True):
    reading, result = generate_and_store(abnormal=True)

    st.sidebar.error(
        f"ABNORMAL: {reading['temperature']}°C / "
        f"{reading['humidity']}% RH"
    )

st.sidebar.markdown("---")
st.sidebar.write("Facility: FACILITY-001")
st.sidebar.write("Storage Unit: UNIT-001")


# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------

readings = get_readings()
alerts = get_alerts()


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

if not readings.empty:
    latest = readings.iloc[0]

    col1.metric(
        "Temperature",
        f"{latest['temperature']:.2f} °C"
    )

    col2.metric(
        "Humidity",
        f"{latest['humidity']:.2f} %"
    )

    col3.metric(
        "Unit Status",
        latest["storage_unit_status"]
    )

else:
    col1.metric("Temperature", "--")
    col2.metric("Humidity", "--")
    col3.metric("Unit Status", "NO DATA")

col4.metric(
    "Total Alerts",
    len(alerts)
)


# ---------------------------------------------------------
# CURRENT CONDITION
# ---------------------------------------------------------

st.markdown("## Current Storage Condition")

if not readings.empty:

    latest = readings.iloc[0]

    latest_reading = {
        "temperature": latest["temperature"],
        "humidity": latest["humidity"],
        "storage_unit_status": latest["storage_unit_status"],
        "storage_unit_id": latest["storage_unit_id"],
    }

    condition = detect_condition(latest_reading)

    if condition["abnormal"]:
        st.error(
            f"⚠️ ABNORMAL CONDITION DETECTED — "
            f"{condition['risk_level']} RISK"
        )

        for violation in condition["violations"]:
            st.warning(violation)

    else:
        st.success(
            "✅ Storage conditions are within the acceptable range."
        )

else:
    st.info(
        "No sensor readings available yet. "
        "Use the sidebar to generate a sensor reading."
    )


# ---------------------------------------------------------
# CURRENT READING TABLE
# ---------------------------------------------------------

st.markdown("## Current Storage Reading")

if not readings.empty:

    display_columns = [
        "timestamp",
        "facility_id",
        "storage_unit_id",
        "temperature",
        "humidity",
        "storage_unit_status",
    ]

    st.dataframe(
        readings[display_columns].head(10),
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------
# ALERTS
# ---------------------------------------------------------

st.markdown("## Alerts & Notifications")

if alerts.empty:

    st.success("No alerts recorded.")

else:

    for _, alert in alerts.head(5).iterrows():

        st.error(
            f"🚨 {alert['risk_level']} RISK | "
            f"{alert['storage_unit_id']} | "
            f"{alert['temperature']}°C | "
            f"{alert['humidity']}% RH"
        )

        st.write(alert["message"])

        st.caption(
            f"Generated: {alert['timestamp']}"
        )


# ---------------------------------------------------------
# HISTORICAL TRENDS
# ---------------------------------------------------------

st.markdown("## Historical Temperature & Humidity")

if len(readings) >= 2:

    chart_data = readings.copy()

    chart_data["timestamp"] = pd.to_datetime(
        chart_data["timestamp"]
    )

    chart_data = chart_data.sort_values("timestamp")

    st.markdown("### Historical Readings")

    st.dataframe(
        chart_data[
            [
                "timestamp",
                "temperature",
                "humidity",
                "storage_unit_status"
            ]
        ].tail(10),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Generate at least two sensor readings to display historical trends."
    )


# ---------------------------------------------------------
# STORAGE RISK SUMMARY
# ---------------------------------------------------------

st.markdown("## Storage Risk Summary")

if not readings.empty:

    risk_counts = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0,
    }

    for _, row in readings.iterrows():

        test_reading = {
            "temperature": row["temperature"],
            "humidity": row["humidity"],
            "storage_unit_status": row["storage_unit_status"],
            "storage_unit_id": row["storage_unit_id"],
        }

        result = detect_condition(test_reading)

        risk_counts[result["risk_level"]] += 1

    r1, r2, r3, r4 = st.columns(4)

    r1.metric("Low Risk", risk_counts["LOW"])
    r2.metric("Medium Risk", risk_counts["MEDIUM"])
    r3.metric("High Risk", risk_counts["HIGH"])
    r4.metric("Critical Risk", risk_counts["CRITICAL"])


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "FreshChoice SafeStore | Prototype demonstration | "
    f"Last dashboard refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
