from fastapi import FastAPI
from pydantic import BaseModel
import csv
from datetime import datetime

app = FastAPI()

class SensorData(BaseModel):
    fsr1: int
    fsr2: int
    fsr3: int
    fsr4: int
    temp1: float
    temp2: float

DATA_FILE = "sensor_data.csv"

@app.post("/log")
async def log_data(data: SensorData):
    # This appends the new data to your sensor_data.csv file
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            data.fsr1, data.fsr2, data.fsr3, data.fsr4, 
            data.temp1, data.temp2
        ])
    return {"status": "saved"}
