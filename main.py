from fastapi import FastAPI, Request
import csv
from datetime import datetime

app = FastAPI()

@app.post("/log")
async def log_sensor_data(request: Request):
    data = await request.json()
    # Expects data format: {"pressure": 120, "temp": 37.5}
    pressure = data.get("pressure")
    temp = data.get("temp")
    
    # Save the data to a local CSV file
    with open("daily_log.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pressure, temp])
    
    return {"status": "success", "received": data}
