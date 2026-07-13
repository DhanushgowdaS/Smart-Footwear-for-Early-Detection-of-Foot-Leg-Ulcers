from fastapi import FastAPI
from pydantic import BaseModel
import csv
from datetime import datetime
import os

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
    try:
        # Check if file exists to know if we need a header
        file_exists = os.path.isfile(DATA_FILE)
        
        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            # Write header if new file
            if not file_exists:
                writer.writerow(['timestamp', 'fsr1', 'fsr2', 'fsr3', 'fsr4', 'temp1', 'temp2'])
            
            # Write data
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                data.fsr1, data.fsr2, data.fsr3, data.fsr4, 
                data.temp1, data.temp2
            ])
        print(f"DEBUG: Successfully wrote to {DATA_FILE}")
        return {"status": "saved"}
    except Exception as e:
        print(f"DEBUG: Error writing to file: {e}")
        return {"status": "error", "detail": str(e)}
