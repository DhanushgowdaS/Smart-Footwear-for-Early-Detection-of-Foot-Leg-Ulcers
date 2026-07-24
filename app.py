import streamlit as st
import pandas as pd
import requests
from datetime import datetime

API_BASE="https://smart-footwear-api.onrender.com"
DATA_API=f"{API_BASE}/data"
CSV_API=f"{API_BASE}/download_csv"

st.set_page_config(page_title="Smart Footwear Dashboard",page_icon="🩺",layout="wide")

st.title("🩺 Smart Footwear for Early Ulcer Detection")
st.caption("AI Powered IoT Monitoring Dashboard")

st.write("**Server:**",API_BASE)
st.write(datetime.now().strftime("%d %b %Y %H:%M:%S"))

if st.button("🔄 Refresh"):
    st.rerun()

try:
    r=requests.get(DATA_API,timeout=10)
    r.raise_for_status()
    data=r.json()
    if not data:
        st.warning("Waiting for sensor data...")
        st.stop()

    df=pd.DataFrame(data)
    df["timestamp"]=pd.to_datetime(df["timestamp"])
    df=df.sort_values("timestamp")
    latest=df.iloc[-1]

    a,b,c,d,e=st.columns(5)
    a.metric("FSR1",f"{latest['fsr1']:.0f}")
    b.metric("FSR2",f"{latest['fsr2']:.0f}")
    c.metric("FSR3",f"{latest['fsr3']:.0f}")
    d.metric("FSR4",f"{latest['fsr4']:.0f}")
    e.metric("Temperature",f"{latest['temp1']:.2f} °C")

    a,b,c,d=st.columns(4)
    a.metric("Average",f"{latest['avg_pressure']:.2f}")
    b.metric("Maximum",f"{latest['max_pressure']:.2f}")
    c.metric("Scenario",latest["scenario"])
    d.metric("Prediction",latest["prediction"])

    st.subheader("Pressure")
    st.line_chart(df.set_index("timestamp")[["fsr1","fsr2","fsr3","fsr4"]],use_container_width=True)

    st.subheader("Temperature")
    st.line_chart(df.set_index("timestamp")[["temp1"]],use_container_width=True)

    risk=latest["prediction"].lower()
    if risk=="safe":
        st.success(latest["prediction"])
    elif risk=="low risk":
        st.info(latest["prediction"])
    elif risk=="medium risk":
        st.warning(latest["prediction"])
    else:
        st.error(latest["prediction"])

    df["Time"]=df["timestamp"].dt.strftime("%H:%M:%S")
    st.dataframe(df[["Time","scenario","prediction","fsr1","fsr2","fsr3","fsr4","temp1","avg_pressure","max_pressure"]].tail(20),hide_index=True,use_container_width=True)

    csv=requests.get(CSV_API).content
    st.download_button("Download CSV",csv,file_name="dataset.csv",mime="text/csv")

except Exception as e:
    st.error(str(e))
