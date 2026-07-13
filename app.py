import streamlit as st
import pandas as pd
import requests
import time

# --- CONFIGURATION ---
API_URL = "https://smart-footwear-api.onrender.com/data"

st.set_page_config(page_title="Smart Footwear Dashboard", layout="wide")
st.title("🥾 Smart Footwear: Real-Time Monitoring")

# --- DASHBOARD LAYOUT ---
placeholder = st.empty()

while True:
    try:
        # Request data from backend
        response = requests.get(API_URL, timeout=10)
        
        with placeholder.container():
            if response.status_code == 200:
                data = response.json()
                
                # Check if data is valid and not empty
                if isinstance(data, list) and len(data) > 0:
                    df = pd.DataFrame(data)
                    
                    # Ensure required columns exist before plotting
                    fsr_cols = ['fsr1', 'fsr2', 'fsr3', 'fsr4']
                    available_fsr = [c for c in fsr_cols if c in df.columns]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Pressure Trend (FSRs)")
                        if available_fsr:
                            st.line_chart(df[available_fsr])
                        else:
                            st.write("FSR data not available.")
                            
                    with col2:
                        st.subheader("Temperature Trend")
                        if 'temp1' in df.columns:
                            st.line_chart(df[['temp1']])
                        else:
                            st.write("Temperature data not available.")
                    
                    st.subheader("Latest Entries")
                    st.dataframe(df.head(10))
                else:
                    st.warning("Database is empty. Waiting for ESP32 data...")
            else:
                st.error(f"Backend API Error: {response.status_code}")
                
    except Exception as e:
        st.error(f"Connection issue: {e}")
        st.write("Check if your backend is running at: ", API_URL)
    
    time.sleep(5) # Refresh interval
    st.rerun()
