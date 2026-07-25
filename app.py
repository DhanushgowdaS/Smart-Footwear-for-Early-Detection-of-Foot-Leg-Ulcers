import streamlit as st
import pandas as pd
import requests

API_URL = "https://smart-footwear-api.onrender.com"

st.set_page_config(
    page_title="Smart Footwear Dashboard",
    layout="wide"
)

st.title("Smart Footwear for Early Ulcer Detection")

if st.button("🔄 Refresh Live Data"):
    st.rerun()
# -----------------------------
# Fetch Live Data
# -----------------------------
try:
    response = requests.get(f"{API_URL}/data", timeout=10)
    response.raise_for_status()

    data = response.json()

    if len(data) > 0:
        df = pd.DataFrame(data)

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")

        latest = df.iloc[-1]

    else:
        st.warning("Waiting for sensor data...")
        st.stop()

except Exception as e:
    st.error(f"Connection failed: {e}")
    st.stop()
