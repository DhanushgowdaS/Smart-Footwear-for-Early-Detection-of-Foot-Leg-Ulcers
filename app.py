import streamlit as st
import pandas as pd
import requests
import io

# --- Page Config ---
st.set_page_config(page_title="Smart Footwear Dashboard", layout="wide")

st.title("🥾 Smart Footwear: Real-Time Monitoring")
st.markdown("---")

# --- Configuration ---
# REPLACE with your actual Render API URL
RENDER_API_URL = "https://smart-footwear-api.onrender.com/download"

# --- Data Fetching Function ---
def get_data():
    try:
        response = requests.get(RENDER_API_URL)
        if response.status_code == 200:
            # Load the CSV data from the response content
            return pd.read_csv(io.StringIO(response.text))
        else:
            return None
    except Exception:
        return None

# --- Dashboard Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Control Panel")
    if st.button("Refresh Live Data"):
        st.rerun()
    st.info("Data is being pulled from your live backend API.")

# --- Display Data ---
df = get_data()

if df is not None and not df.empty:
    with col1:
        st.write("### Latest Entries")
        st.dataframe(df.tail(5), use_container_width=True)
        
    with col2:
        st.write("### Pressure Trend Analysis (FSRs)")
        st.line_chart(df[['fsr1', 'fsr2', 'fsr3', 'fsr4']])
        
        st.write("### Temperature Trend")
        st.line_chart(df[['temp1', 'temp2']])
else:
    st.warning("No data detected. Ensure your ESP32 is sending data to the FastAPI /log endpoint!")
