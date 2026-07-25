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


# -----------------------------
# Graphs
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pressure Analysis")

    if not df.empty:
        pressure_cols = [c for c in ["fsr1", "fsr2", "fsr3", "fsr4"] if c in df.columns]
        if pressure_cols:
            st.line_chart(df[pressure_cols])

with col2:
    st.subheader("Temperature")

    if not df.empty:
        if "temp1" in df.columns:
            st.line_chart(df[["temp1"]])
