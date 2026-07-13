import streamlit as st
import pandas as pd
import joblib
import os

st.title("Smart Footwear: Ulcer Risk Analysis")

# Load model (make sure model.pkl is in your folder)
@st.cache_resource
def load_model():
    return joblib.load('model.pkl')

model = load_model()

# Analyze data
if st.button("Generate Daily Report"):
    if os.path.exists("daily_log.csv"):
        df = pd.read_csv("daily_log.csv", names=["timestamp", "pressure", "temp"])
        
        # Get the latest data for prediction
        latest_data = df.tail(1)
        prediction = model.predict(latest_data[["pressure", "temp"]])
        
        st.write(f"### Analysis Result: {prediction[0]}")
        st.line_chart(df[["pressure", "temp"]])
    else:
        st.error("No data found! Please ensure the ESP32 is sending data.")
