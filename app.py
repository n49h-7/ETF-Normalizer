import streamlit as st
import pandas as pd

st.set_page_config(page_title="ETF Normalizer", page_icon="📊")

st.title("📊 ETF Data Normalizer")
st.write("Upload any ETF PDF and get back a clean, standardized CSV.")

uploaded_file = st.file_uploader("Upload ETF PDF here", type=["pdf"])

if uploaded_file is not None:
    st.success("File uploaded! Processing coming soon once Dinu's code is connected.")
    st.info("Output columns will be: Ticker | Name | Weight | Sector")
