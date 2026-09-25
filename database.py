import sqlite3
from pathlib import Path


DB_PATH = Path("data") / "safestore.db"


def initialise_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
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


def save_reading(reading: dict) -> None:
    initialise_database()

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
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


def get_recent_readings(limit: int = 10) -> list[tuple]:
    initialise_database()

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
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
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()


if __name__ == "__main__":
    initialise_database()
    print(f"Database initialised at: {DB_PATH}")
