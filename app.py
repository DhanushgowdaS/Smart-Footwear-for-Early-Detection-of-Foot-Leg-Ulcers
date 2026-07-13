import streamlit as st
import pandas as pd
import os

# --- Page Config ---
st.set_page_config(page_title="Smart Footwear Dashboard", layout="wide")

st.title("🥾 Smart Footwear: Ulcer Risk Analysis Dashboard")
st.markdown("---")

# --- Sidebar ---
st.sidebar.header("Manual Controls")
p_input = st.sidebar.slider('Test Pressure (FSR)', 0, 4000, 500)
t_input = st.sidebar.slider('Test Temperature (°C)', 20.0, 50.0, 28.0)

# --- Main Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Live Sensor Data")
    if os.path.exists("sensor_data.csv"):
        df = pd.read_csv("sensor_data.csv")
        st.dataframe(df.tail(10), use_container_width=True)
        if st.button("Refresh Data"):
            st.rerun()
    else:
        st.warning("sensor_data.csv not found.")

with col2:
    st.subheader("Sensor Trends")
    if os.path.exists("sensor_data.csv"):
        df = pd.read_csv("sensor_data.csv")
        # Visualizing all 4 FSRs
        st.line_chart(df[['fsr1', 'fsr2', 'fsr3', 'fsr4']])
    else:
        st.info("Waiting for data to visualize...")

st.markdown("---")
# --- ML Analysis Section ---
st.subheader("AI Risk Assessment")
if st.button("Analyze Current Risk Profile"):
    # This calls your model logic
    with st.spinner('AI analyzing sensor data...'):
        # Placeholder for your model prediction logic
        st.success("Risk Level: Low | Current Status: Stable")
