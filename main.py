from fastapi import FastAPI, Request
import csv
from datetime import datetime
import joblib
import pandas as pd

app = FastAPI()

# Load your ML model once when the server starts
model = joblib.load("model.pkl")

@app.post("/log")
async def log_sensor_data(request: Request):
    data = await request.json()
    pressure = data.get("pressure")
    temp = data.get("temp")
    
    # 1. Save the data to your CSV
    with open("daily_log.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pressure, temp])
    
    # 2. Prepare data for the model
    # Ensure the column names match what your model was trained on
    input_data = pd.DataFrame([[pressure, temp]], columns=['pressure', 'temp'])
    
    # 3. Get prediction
    prediction = model.predict(input_data)
    
    # 4. Return both the success status and the prediction result
    return {
        "status": "success", 
        "prediction": int(prediction[0])
    }
