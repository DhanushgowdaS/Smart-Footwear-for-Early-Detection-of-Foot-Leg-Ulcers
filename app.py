import streamlit as st
import pandas as pd
import requests

API_URL = "https://smart-footwear-api.onrender.com/data"

st.set_page_config(page_title="Smart Footwear Dashboard", layout="wide")
st.title("🥾 Smart Footwear: Real-Time Monitoring")

# Manual Refresh Button
if st.button("Refresh Live Data"):
    st.rerun()

# --- DATA FETCHING ---
try:
    response = requests.get(API_URL, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            
            # --- LAYOUT: CHARTS ---
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Pressure Analysis")
                st.line_chart(df[['fsr1', 'fsr2', 'fsr3', 'fsr4']])
            with col2:
                st.subheader("Temperature")
                st.line_chart(df[['temp1']])
            
            # --- LAYOUT: ML STATUS & TABLE ---
            st.subheader("Latest Entries & ML Status")
            
            # Mapping status to emojis for better visual representation
            def add_emoji(val):
                if val == "Critical": return "🔴 Critical"
                if val == "Normal": return "🟡 Normal"
                return "🟢 Good"

            df['Display_Status'] = df['status'].apply(add_emoji)
            
            # Reorder columns to show status first
            cols = ['Display_Status', 'fsr1', 'fsr2', 'fsr3', 'fsr4', 'temp1']
            st.dataframe(df[cols].tail(10), use_container_width=True)
        else:
            st.warning("No data yet. Waiting for ESP32...")
    else:
        st.error(f"Backend returned error: {response.status_code}")
except Exception as e:
    st.error(f"Connection error: {e}")
