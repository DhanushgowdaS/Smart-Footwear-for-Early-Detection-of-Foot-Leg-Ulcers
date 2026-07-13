import streamlit as st
import pandas as pd
import requests
import time

# --- CONFIGURATION ---
# Replace with your actual Render/Backend URL
API_URL = "https://your-backend-service.onrender.com/data"

st.set_page_config(page_title="Smart Footwear Dashboard", layout="wide")

st.title("🥾 Smart Footwear: Real-Time Monitoring")

# --- DATA FETCHING ---
def get_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return pd.DataFrame()

# --- DASHBOARD LAYOUT ---
placeholder = st.empty()

# Refresh loop
while True:
    df = get_data()
    
    if not df.empty:
        # Keep only the columns we actually want to see
        # This completely ignores any rogue temp2 or other error columns
        target_cols = ['fsr1', 'fsr2', 'fsr3', 'fsr4', 'temp1']
        df = df[[c for c in target_cols if c in df.columns]]
        
        with placeholder.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Pressure Trend (FSRs)")
                fsr_cols = [c for c in ['fsr1', 'fsr2', 'fsr3', 'fsr4'] if c in df.columns]
                if fsr_cols:
                    st.line_chart(df[fsr_cols])
            
            with col2:
                st.subheader("Temperature Trend")
                # Strictly only plot temp1
                if 'temp1' in df.columns:
                    st.line_chart(df[['temp1']])
            
            st.subheader("Latest Entries")
            st.dataframe(df.tail(10))

    else:
        st.warning("No data received from backend yet.")
    
    time.sleep(5) # Refresh every 5 seconds
    st.rerun()
