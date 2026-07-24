import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ==========================
# CONFIGURATION
# ==========================
API_URL = "https://smart-footwear-api.onrender.com/data"

st.set_page_config(
    page_title="Smart Footwear Dashboard",
    page_icon="🩺",
    layout="wide"
)

# ==========================
# CUSTOM CSS
# ==========================

st.markdown("""
<style>

html, body, [class*="css"]{
    background-color:#0E1117;
    color:white;
}

.title{
    text-align:center;
    font-size:48px;
    font-weight:800;
    color:white;
    text-shadow:
        0 0 8px rgba(0,170,255,.45),
        0 0 20px rgba(0,170,255,.30);
    margin-bottom:5px;
}

.subtitle{
    text-align:center;
    color:#9CA3AF;
    margin-bottom:25px;
}

.clock{
    text-align:right;
    font-size:18px;
    color:#7DD3FC;
    margin-bottom:10px;
}

div[data-testid="metric-container"]{
    background:#161B22;
    border:1px solid rgba(0,170,255,.20);
    border-radius:15px;
    padding:12px;
    box-shadow:0 0 15px rgba(0,170,255,.12);
}

div[data-testid="metric-container"]:hover{
    box-shadow:0 0 22px rgba(0,170,255,.25);
}

div[data-testid="stDataFrame"]{
    border-radius:15px;
    border:1px solid rgba(0,170,255,.20);
    box-shadow:0 0 18px rgba(0,170,255,.12);
}

button[kind="secondary"]{
    border-radius:10px;
    border:1px solid #38BDF8;
}

button[kind="secondary"]:hover{
    box-shadow:0 0 18px rgba(56,189,248,.45);
}

</style>
""", unsafe_allow_html=True)

# ==========================
# TITLE
# ==========================

st.markdown("""
<div class="title">
Smart Footwear for Ulcer Detection
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"<div class='clock'>🕒 {datetime.now().strftime('%d %b %Y | %H:%M:%S')}</div>",
    unsafe_allow_html=True
)

# ==========================
# REFRESH BUTTON
# ==========================

if st.button("🔄 Refresh Live Data"):
    st.rerun()

# ==========================
# GET DATA
# ==========================

try:

    response = requests.get(API_URL, timeout=10)

    if response.status_code == 200:

        data = response.json()

        if data:

            df = pd.DataFrame(data)

            # -----------------------
            # Add Time Column
            # -----------------------

            if "timestamp" in df.columns:
                df["Time"] = pd.to_datetime(
                    df["timestamp"]
                ).dt.strftime("%H:%M:%S")
            else:
                df["Time"] = datetime.now().strftime("%H:%M:%S")

            latest = df.iloc[-1]

            # ==========================
            # METRICS
            # ==========================

            st.subheader("Live Sensor Values")

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric("F1", f"{latest['fsr1']:.0f}")
            c2.metric("F2", f"{latest['fsr2']:.0f}")
            c3.metric("F3", f"{latest['fsr3']:.0f}")
            c4.metric("F4", f"{latest['fsr4']:.0f}")
            c5.metric("Temperature", f"{latest['temp1']:.2f} °C")

            st.divider()

            # ==========================
            # CHARTS
            # ==========================

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Pressure Analysis")

                st.line_chart(
                    df[['fsr1', 'fsr2', 'fsr3', 'fsr4']],
                    use_container_width=True
                )

            with col2:

                st.subheader("Temperature Analysis")

                st.line_chart(
                    df[['temp1']],
                    use_container_width=True
                )

            st.divider()

            # ==========================
            # STATUS
            # ==========================

            def status_text(status):

                if status == "Critical":
                    return "🔴 Critical"

                elif status == "Normal":
                    return "🟡 Normal"

                else:
                    return "🟢 Good"

            df["Status"] = df["status"].apply(status_text)

            # ==========================
            # TABLE
            # ==========================

            st.subheader("Latest Entries & Status")

            display_df = df[
                [
                    "Time",
                    "Status",
                    "fsr1",
                    "fsr2",
                    "fsr3",
                    "fsr4",
                    "temp1"
                ]
            ].rename(
                columns={
                    "fsr1": "F1",
                    "fsr2": "F2",
                    "fsr3": "F3",
                    "fsr4": "F4",
                    "temp1": "Temperature (°C)"
                }
            )

            st.dataframe(
                display_df.tail(10),
                use_container_width=True,
                hide_index=True
            )

        else:
            st.warning("Waiting for live sensor data...")

    else:
        st.error(f"Server Error : {response.status_code}")

except Exception as e:

    st.error(f"Connection Failed\n\n{e}")
