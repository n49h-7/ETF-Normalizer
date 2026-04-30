import streamlit as st
import pandas as pd

st.set_page_config(page_title="ETF Normalizer", page_icon="📊")

st.title("📊 ETF Data Normalizer")
st.write("Upload any ETF PDF and get back a clean, standardized CSV.")

uploaded_file = st.file_uploader("Upload ETF PDF here", type=["pdf"])

if uploaded_file is not None:
    try:
        st.success("✅ Your PDF has been uploaded successfully!")
        st.info("⏳ Your file is being processed — your standardized CSV will be ready to download shortly.")
        st.warning("🔗 AI processing will be available once the pipeline is connected.")
    except Exception as e:
        st.error("❌ Something went wrong with your file. Please try the following:")
        st.write("- Make sure the file is a PDF")
        st.write("- Check the file isn't corrupted or password protected")
        st.write("- Try uploading again")
