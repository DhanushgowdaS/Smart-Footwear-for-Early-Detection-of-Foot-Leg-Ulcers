from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import requests

API_URL = "https://smart-footwear-api.onrender.com"

st.set_page_config(
    page_title="Smart Footwear Dashboard",
    layout="wide"
)

st_autorefresh(interval=1000, key="live_dashboard")

st.title("🩺 Smart Footwear for Early Detection of Foot Ulcers")

from datetime import datetime

# ---------------- REFRESH & LIVE TIME ----------------
left, right = st.columns([1, 1])

with left:
    if st.button("🔄 Refresh Live Data"):
        st.rerun()

with right:
    st.components.v1.html("""
    <div id="clock" style="text-align:right; font-size:18px; font-weight:bold;">
    </div>

    <script>
    function updateClock() {
        const now = new Date();

        const options = {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        };

        const date = now.toLocaleDateString('en-GB', options);
        const time = now.toLocaleTimeString();

        document.getElementById("clock").innerHTML =
            "🕒 " + date + " " + time;
    }

    updateClock();
    setInterval(updateClock, 1000);
    </script>
    """, height=35)

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
