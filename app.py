import sqlite3
import hmac
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
# PROTOTYPE AUTHENTICATION
# ---------------------------------------------------------
# Demo-only credentials for the assessment prototype.
# For production, use a proper identity provider and secrets manager.
DEMO_USERS = {
    "manager": {"password": "SafeStore123", "role": "Manager"},
    "staff": {"password": "Staff123", "role": "Staff"},
}


def authenticate(username: str, password: str):
    user = DEMO_USERS.get(username.strip().lower())
    if not user:
        return None
    if not hmac.compare_digest(password, user["password"]):
        return None
    return user["role"]


def show_login():
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem 0;">
        <h1>FreshChoice SafeStore</h1>
        <p>Smart Storage Monitoring & Risk Management System</p>
        <p><b>Prototype Login</b></p>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        with st.form("login_form"):
            st.subheader("Sign in")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            if submitted:
                role = authenticate(username, password)
                if role:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username.strip().lower()
                    st.session_state["role"] = role
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        st.caption("Prototype roles: Manager and Staff")


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    show_login()
    st.stop()


def logout():
    for key in ["authenticated", "username", "role"]:
        st.session_state.pop(key, None)
    st.rerun()


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

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS inspections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                storage_unit_id TEXT NOT NULL,
                staff_name TEXT NOT NULL,
                outcome TEXT NOT NULL,
                notes TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS equipment_problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                storage_unit_id TEXT NOT NULL,
                staff_name TEXT NOT NULL,
                priority TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL
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


def save_inspection(staff_name, outcome, notes):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO inspections (
                timestamp,
                storage_unit_id,
                staff_name,
                outcome,
                notes
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                "UNIT-001",
                staff_name,
                outcome,
                notes,
            ),
        )


def save_equipment_problem(staff_name, priority, description):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO equipment_problems (
                timestamp,
                storage_unit_id,
                staff_name,
                priority,
                description,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                "UNIT-001",
                staff_name,
                priority,
                description,
                "OPEN",
            ),
        )


def get_inspections():
    initialise_database()
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            """
            SELECT timestamp, storage_unit_id, staff_name, outcome, notes
            FROM inspections
            ORDER BY id DESC
            """,
            conn,
        )


def get_equipment_problems():
    initialise_database()
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            """
            SELECT timestamp, storage_unit_id, staff_name, priority, description, status
            FROM equipment_problems
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
    "Monitor storage conditions, detect abnormal readings, review alerts and analyse historical storage performance."
)

st.sidebar.success(
    f"Signed in: {st.session_state['username']} ({st.session_state['role']})"
)
if st.sidebar.button("Log out", use_container_width=True):
    logout()

st.sidebar.markdown("---")
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
# APPLICATION VIEWS
# ---------------------------------------------------------

if st.session_state["role"] == "Manager":
    st.markdown("## Management Dashboard")
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

        st.line_chart(
            chart_data.set_index("timestamp")[
                ["temperature", "humidity"]
            ]
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

elif st.session_state["role"] == "Staff":
    st.markdown("## Staff Monitoring Portal")
    st.subheader("Staff Monitoring Portal")
    st.caption("Operational view for current conditions, alerts, inspections and equipment reporting.")

    # Current conditions
    staff_readings = get_readings()
    staff_alerts = get_alerts()
    staff_inspections = get_inspections()
    staff_equipment = get_equipment_problems()

    if not staff_readings.empty:
        current = staff_readings.iloc[0]

        s1, s2, s3 = st.columns(3)
        s1.metric("Temperature", f"{current['temperature']:.2f} °C")
        s2.metric("Humidity", f"{current['humidity']:.2f} %")
        s3.metric("Unit Status", current["storage_unit_status"])

        st.markdown("### Current & Historical Readings")
        st.dataframe(
            staff_readings[
                [
                    "timestamp",
                    "storage_unit_id",
                    "temperature",
                    "humidity",
                    "storage_unit_status",
                ]
            ].head(10),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No sensor readings available yet. Generate a reading from the Sensor Controls.")

    # Alerts
    st.markdown("### Alerts")
    if staff_alerts.empty:
        st.success("No alerts recorded.")
    else:
        st.dataframe(
            staff_alerts[
                [
                    "timestamp",
                    "storage_unit_id",
                    "temperature",
                    "humidity",
                    "risk_level",
                    "severity",
                    "message",
                ]
            ].head(10),
            use_container_width=True,
            hide_index=True,
        )

    # Inspection form
    st.markdown("### Record Storage Inspection")
    inspection_staff = st.text_input("Staff name", key="inspection_staff")
    inspection_outcome = st.selectbox(
        "Inspection outcome",
        ["PASS", "MINOR ISSUE", "FAIL"],
        key="inspection_outcome",
    )
    inspection_notes = st.text_area("Inspection notes", key="inspection_notes")

    if st.button("Save Inspection", key="save_inspection"):
        if not inspection_staff.strip():
            st.error("Please enter the staff name.")
        else:
            save_inspection(
                inspection_staff.strip(),
                inspection_outcome,
                inspection_notes.strip(),
            )
            st.success("Inspection recorded successfully.")
            st.rerun()

    # Equipment problem form
    st.markdown("### Report Equipment Problem")
    equipment_staff = st.text_input("Staff name", key="equipment_staff")
    equipment_priority = st.selectbox(
        "Priority",
        ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        key="equipment_priority",
    )
    equipment_description = st.text_area(
        "Problem description",
        key="equipment_description",
    )

    if st.button("Submit Equipment Problem", key="save_equipment"):
        if not equipment_staff.strip():
            st.error("Please enter the staff name and problem description.")
        else:
            save_equipment_problem(
                equipment_staff.strip(),
                equipment_priority,
                equipment_description.strip(),
            )
            st.success("Equipment problem recorded successfully.")
            st.rerun()

    # Existing records
    st.markdown("### Inspection History")
    if staff_inspections.empty:
        st.info("No inspections recorded yet.")
    else:
        st.dataframe(
            staff_inspections.head(10),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("### Equipment Problems")
    if staff_equipment.empty:
        st.info("No equipment problems recorded yet.")
    else:
        st.dataframe(
            staff_equipment.head(10),
            use_container_width=True,
            hide_index=True,
        )

    # Notification status
    st.markdown("### Notification Status")
    if not staff_alerts.empty:
        st.warning(
            "Notification path: SIMULATION MODE. "
            "The dashboard records and displays alerts. Live SMS requires provider configuration."
        )
    else:
        st.success("No notification event pending.")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "FreshChoice SafeStore | Prototype demonstration | "
    f"Last dashboard refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
