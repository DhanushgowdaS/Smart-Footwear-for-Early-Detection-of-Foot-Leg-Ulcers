import streamlit as st
import pandas as pd
import requests

API_URL = "https://smart-footwear-api.onrender.com"

st.set_page_config(
    page_title="Smart Footwear Dashboard",
    layout="wide"
)

st.title("🩺 Smart Footwear for Early Detection of Foot Ulcers")

from datetime import datetime

# ---------------- REFRESH & LIVE TIME ----------------
left, right = st.columns([1, 1])

with left:
    if st.button("🔄 Refresh Live Data"):
        st.rerun()

with right:
    current_time = datetime.now().strftime("%d-%m-%Y  %I:%M:%S %p")
    st.markdown(
        f"<div style='text-align:right; font-size:18px;'>"
        f"🕒 <b>{current_time}</b>"
        f"</div>",
        unsafe_allow_html=True
    )

# ---------------- FETCH DATA ----------------
try:
    response = requests.get(f"{API_URL}/data", timeout=10)

    if response.status_code == 200:
        data = response.json()

        if data:
            df = pd.DataFrame(data)

            # ---------------- CHARTS ----------------
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Pressure Analysis")
                st.line_chart(df[["fsr1", "fsr2", "fsr3", "fsr4"]])

            with col2:
                st.subheader("Temperature")
                st.line_chart(df[["temp1"]])
    

                # ================= OVERALL RISK ASSESSMENT =================

            st.info("""
            ### Overall Risk Assessment

            🟢 Safe

            Based on Last 10 Readings
            """)



            
            # ---------------- STATUS ----------------
            st.subheader("Latest Entries & Status")

            def add_emoji(val):
                val = str(val).lower()

                if "critical" in val:
                    return "🔴 Critical"
                elif "normal" in val:
                    return "🟡 Normal"
                else:
                    return "🟢 " + str(val)

            df["Display_Status"] = df["prediction"].apply(add_emoji)

            cols = [
                "timestamp",
                "Display_Status",
                "fsr1",
                "fsr2",
                "fsr3",
                "fsr4",
                "temp1"
            ]

            st.dataframe(df[cols], use_container_width=True)

        else:
            st.warning("Waiting for sensor data...")

    else:
        st.error(f"Backend returned error: {response.status_code}")

except Exception as e:
    st.error(f"Connection failed: {e}")
