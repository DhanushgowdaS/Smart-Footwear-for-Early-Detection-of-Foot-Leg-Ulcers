from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DB_NAME = "sensor_data.db"

# Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    fsr1 REAL, fsr2 REAL, fsr3 REAL, fsr4 REAL, temp1 REAL)""")
    conn.commit()
    conn.close()

init_db()

class SensorData(BaseModel):
    fsr1: float
    fsr2: float
    fsr3: float
    fsr4: float
    temp1: float

@app.post("/log")
def log_data(data: SensorData):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings (fsr1, fsr2, fsr3, fsr4, temp1) VALUES (?,?,?,?,?)",
                   (data.fsr1, data.fsr2, data.fsr3, data.fsr4, data.temp1))
    # Keep only the last 1000 entries
    cursor.execute("DELETE FROM readings WHERE id <= (SELECT MAX(id) - 1000 FROM readings)")
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/data")
def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT fsr1, fsr2, fsr3, fsr4, temp1 FROM readings ORDER BY id DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    # Format for DataFrame
    return [{"fsr1": r[0], "fsr2": r[1], "fsr3": r[2], "fsr4": r[3], "temp1": r[4]} for r in rows]
