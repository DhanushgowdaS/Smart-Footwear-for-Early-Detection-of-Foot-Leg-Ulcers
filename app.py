import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Smart Footwear Dashboard",
    page_icon="🩺",
    layout="wide"
)
st_autorefresh(interval=1000, key="clock")
# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

html, body, [class*="css"]{
    font-family: Arial, sans-serif;
}

.stApp{
    background:#081421;
}

/* Title */

.title{
    text-align:center;
    font-size:46px;
    font-weight:800;
    color:white;
    margin-top:20px;
    margin-bottom:55px;
    text-shadow:
        0px 0px 8px rgba(0,191,255,.45),
        0px 0px 18px rgba(0,191,255,.25);
}

/* Refresh Button */

.stButton>button{

    background: linear-gradient(135deg,#00C6FF,#0072FF);
    color:white;
    border:none;
    border-radius:12px;
    padding:14px 30px;
    font-size:18px;
    font-weight:700;
    box-shadow:0 8px 20px rgba(0,114,255,.35);
    transition:all .3s ease;

}

.stButton>button:hover{

    transform:scale(1.08);
    background:linear-gradient(135deg,#4FACFE,#00F2FE);
    box-shadow:0 10px 25px rgba(0,255,255,.45);
    cursor:pointer;

}



/* Time */

.time{
    text-align:right;
    font-size:18px;
    font-weight:bold;
    color:#D6EAF8;
    margin-top:12px;
}

/* Prediction Card */

.status{
    background:#102842;
    border-radius:18px;
    padding:45px;
    text-align:center;
    font-size:36px;
    font-weight:700;
    color:white;
    box-shadow:0 0 30px rgba(0,191,255,.30);
    margin-top:40px;
    margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.markdown("""
<div class='title'>
SMART FOOTWEAR FOR EARLY ULCER DETECTION
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Refresh & Time
# -----------------------------
left, right = st.columns([1,3])

with left:
    if st.button("🔄 Refresh"):
        st.rerun()

with right:
    st.markdown(
        f"<div class='time'>{datetime.now().strftime('%d %B %Y | %I:%M:%S %p')}</div>",
        unsafe_allow_html=True
    )

# -----------------------------
# Prediction Card
# -----------------------------
prediction = "Waiting for Sensor Data..."

st.markdown(f"""
<div class='status'>
Prediction<br><br>
{prediction}
</div>
""", unsafe_allow_html=True)
