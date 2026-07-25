import streamlit as st
import pandas as pd
import requests

API_URL = "https://smart-footwear-api.onrender.com"

st.set_page_config(
    page_title="Smart Footwear Dashboard",
    layout="wide"
)

st.title("Smart Footwear for Early Ulcer Detection")

if st.button("🔄 Refresh Live Data"):
    st.rerun()
