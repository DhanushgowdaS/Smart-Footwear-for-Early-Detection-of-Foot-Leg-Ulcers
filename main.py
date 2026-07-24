from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import csv
import os
from datetime import datetime

app = FastAPI()

DB_NAME = "sensor_data.db"
CSV_FILE = "dataset.csv"


# -------------------- DATABASE --------------------

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        scenario TEXT,
        fsr1 REAL,
        fsr2 REAL,
        fsr3 REAL,
        fsr4 REAL,
        temp1 REAL,
        avg_pressure REAL,
        max_pressure REAL
    )
    """)
    conn.commit()
    conn.close()


init_db()


# -------------------- CSV --------------------

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Timestamp",
                "Scenario",
                "FSR1",
                "FSR2",
                "FSR3",
                "FSR4",
                "Temperature",
                "AveragePressure",
                "MaximumPressure"
            ])


init_csv()


# -------------------- MODEL --------------------

class SensorData(BaseModel):
    scenario: str
    fsr1: float
    fsr2: float
    fsr3: float
    fsr4: float
    temp1: float


# -------------------- LOG DATA --------------------

@app.post("/log")
def log_data(data: SensorData):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    avg_pressure = (
        data.fsr1 +
        data.fsr2 +
        data.fsr3 +
        data.fsr4
    ) / 4

    max_pressure = max(
        data.fsr1,
        data.fsr2,
        data.fsr3,
        data.fsr4
    )

    try:

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO readings
        (
            timestamp,
            scenario,
            fsr1,
            fsr2,
            fsr3,
            fsr4,
            temp1,
            avg_pressure,
            max_pressure
        )

        VALUES (?,?,?,?,?,?,?,?,?)
        """,
        (
            timestamp,
            data.scenario,
            data.fsr1,
            data.fsr2,
            data.fsr3,
            data.fsr4,
            data.temp1,
            avg_pressure,
            max_pressure
        ))

        cursor.execute("""
        DELETE FROM readings
        WHERE id <= (
            SELECT MAX(id)-5000
            FROM readings
        )
        """)

        conn.commit()
        conn.close()

        with open(CSV_FILE, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                data.scenario,
                data.fsr1,
                data.fsr2,
                data.fsr3,
                data.fsr4,
                data.temp1,
                avg_pressure,
                max_pressure
            ])

        return {
            "status": "success",
            "message": "Data Saved"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -------------------- LAST 100 DATA --------------------

@app.get("/data")
def get_data():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute("""

    SELECT

    timestamp,
    scenario,
    fsr1,
    fsr2,
    fsr3,
    fsr4,
    temp1,
    avg_pressure,
    max_pressure

    FROM readings

    ORDER BY id DESC

    LIMIT 100

    """)

    rows = cursor.fetchall()

    conn.close()

    return [

        {

            "timestamp": r[0],
            "scenario": r[1],
            "fsr1": r[2],
            "fsr2": r[3],
            "fsr3": r[4],
            "fsr4": r[5],
            "temp1": r[6],
            "avg_pressure": r[7],
            "max_pressure": r[8]

        }

        for r in rows

    ]


# -------------------- LATEST --------------------

@app.get("/latest")
def latest():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute("""

    SELECT

    timestamp,
    scenario,
    fsr1,
    fsr2,
    fsr3,
    fsr4,
    temp1,
    avg_pressure,
    max_pressure

    FROM readings

    ORDER BY id DESC

    LIMIT 1

    """)

    row = cursor.fetchone()

    conn.close()

    if row is None:

        return {}

    return {

        "timestamp": row[0],
        "scenario": row[1],
        "fsr1": row[2],
        "fsr2": row[3],
        "fsr3": row[4],
        "fsr4": row[5],
        "temp1": row[6],
        "avg_pressure": row[7],
        "max_pressure": row[8]

    }


# -------------------- DOWNLOAD CSV --------------------

@app.get("/download_csv")
def download_csv():

    return FileResponse(
        CSV_FILE,
        filename="dataset.csv",
        media_type="text/csv"
    )
