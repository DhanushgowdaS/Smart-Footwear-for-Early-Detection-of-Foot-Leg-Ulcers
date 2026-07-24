import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Smart Footwear Dashboard",
    page_icon="🩺",
    layout="wide"
)
st.markdown("""
<style>

html, body, [class*="css"]{
    font-family:Arial, sans-serif;
}

.stApp{
    background:#081421;
}

/* Main Title */

.title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:white;
    text-shadow:
        0px 0px 10px #00BFFF,
        0px 0px 20px #00BFFF,
        0px 0px 40px #00BFFF;
    animation: glow 2s infinite alternate;
}

@keyframes glow{

from{
text-shadow:
0px 0px 5px #00BFFF;
}

to{
text-shadow:
0px 0px 25px #00BFFF,
0px 0px 50px #00BFFF;
}

}

/* Card */

.card{

background:#122235;

padding:20px;

border-radius:15px;

border:1px solid #1b4f72;

box-shadow:0px 0px 15px rgba(0,191,255,0.25);

}

/* Refresh Button */

.stButton>button{

background:#008CFF;

color:white;

border:none;

border-radius:10px;

padding:12px 22px;

font-size:18px;

transition:0.3s;

}

.stButton>button:hover{

transform:scale(1.10);

background:#00BFFF;

cursor:pointer;

}

/* Time */

.time{

text-align:right;

font-size:18px;

font-weight:bold;

color:#D6EAF8;

}

/* Status Box */

.status{

background:#0D2B45;

border-radius:15px;

padding:25px;

text-align:center;

font-size:30px;

font-weight:bold;

color:white;

box-shadow:0px 0px 20px rgba(0,191,255,.35);

margin-top:20px;

margin-bottom:20px;

}

</style>
""", unsafe_allow_html=True)
st.markdown(
"""
<div class='title'>
🩺 SMART FOOTWEAR FOR EARLY ULCER DETECTION
</div>
""",
unsafe_allow_html=True
)
left,right=st.columns([1,3])

with left:

    if st.button("🔄 Refresh"):

        st.rerun()

with right:

    st.markdown(
    f"<div class='time'>{datetime.now().strftime('%d %B %Y | %I:%M:%S %p')}</div>",
    unsafe_allow_html=True
    )
    prediction="Waiting..."

st.markdown(
f"""
<div class='status'>
Prediction<br>
{prediction}
</div>
""",
unsafe_allow_html=True
)
