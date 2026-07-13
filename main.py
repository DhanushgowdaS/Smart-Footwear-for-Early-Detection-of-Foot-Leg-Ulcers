from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import csv
from datetime import datetime
import os

app = FastAPI()

# Data model for incoming sensor data
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
        # Check if file exists to determine if we need to write a header
        file_exists = os.path.isfile(DATA_FILE)
        
        # Append data to the CSV file
        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            
            # Write header if it's a new file
            if not file_exists:
                writer.writerow(['timestamp', 'fsr1', 'fsr2', 'fsr3', 'fsr4', 'temp1', 'temp2'])
            
            # Write the sensor reading
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                data.fsr1, data.fsr2, data.fsr3, data.fsr4, 
                data.temp1, data.temp2
            ])
            
        print(f"DEBUG: Successfully saved data to {DATA_FILE}")
        return {"status": "saved"}
        
    except Exception as e:
        print(f"DEBUG: Error writing to file: {e}")
        return {"status": "error", "detail": str(e)}

@app.get("/download")
async def download_data():
    if os.path.exists(DATA_FILE):
        return FileResponse(DATA_FILE, media_type='text/csv', filename='sensor_data_exported.csv')
    return {"status": "error", "detail": "File not found"}
