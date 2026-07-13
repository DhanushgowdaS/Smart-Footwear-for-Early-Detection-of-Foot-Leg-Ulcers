from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import joblib
import os

app = FastAPI()

# Path to your database and ML model
DB_NAME = "sensor_data.db"
MODEL_PATH = "model.pkl" 

# Load the ML model
# If the file doesn't exist, this will raise an error on startup
model = joblib.load(MODEL_PATH)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    # Added 'status' column to store ML results
    conn.execute("""CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    fsr1 REAL, fsr2 REAL, fsr3 REAL, fsr4 REAL, temp1 REAL, status TEXT)""")
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
    # 1. Prepare data for ML model
    features = [[data.fsr1, data.fsr2, data.fsr3, data.fsr4, data.temp1]]
    
    # 2. ML Prediction (Assuming your model returns 0, 1, or 2)
    prediction = model.predict(features)[0] 
    status_map = {0: "Good", 1: "Normal", 2: "Critical"}
    status = status_map.get(prediction, "Unknown")
    
    # 3. Save to Database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings (fsr1, fsr2, fsr3, fsr4, temp1, status) VALUES (?,?,?,?,?,?)",
                   (data.fsr1, data.fsr2, data.fsr3, data.fsr4, data.temp1, status))
    
    # Keep only the last 1000 entries
    cursor.execute("DELETE FROM readings WHERE id <= (SELECT MAX(id) - 1000 FROM readings)")
    
    conn.commit()
    conn.close()
    return {"status": "success", "ml_result": status}

@app.get("/data")
def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("SELECT fsr1, fsr2, fsr3, fsr4, temp1, status FROM readings ORDER BY id DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    return [{"fsr1": r[0], "fsr2": r[1], "fsr3": r[2], "fsr4": r[3], "temp1": r[4], "status": r[5]} for r in rows]
