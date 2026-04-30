import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Normalizer", page_icon="📊")

st.title("📊 Financial Data Normalizer")
st.write("Upload any financial document and get back clean, standardized data — instantly.")

st.info("📂 Supports PDF, CSV, Excel and more — no manual formatting needed.")

uploaded_file = st.file_uploader(
    "Upload your financial document here",
    type=["pdf", "csv", "xlsx", "xls", "txt"]
)

if uploaded_file is not None:
    try:
        st.success("✅ Your file has been uploaded successfully!")
        st.info("⏳ Our AI is extracting your data — your standardized file will be ready to download shortly.")
        st.warning("🔗 AI processing will be available once the pipeline is connected.")
    except Exception as e:
        st.error("❌ Something went wrong with your file. Please try the following:")
        st.write("- Make sure the file is a PDF, CSV, or Excel file")
        st.write("- Check the file isn't corrupted or password protected")
        st.write("- Try uploading again")
