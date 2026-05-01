import streamlit as st
import pandas as pd
import io
import json
import google.generativeai as genai
from PyPDF2 import PdfReader

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

def clean_dataframe(df):
    df = df.astype(str)
    df = df.dropna(how='all')
    df = df[~df.iloc[:, 0].str.startswith('Total')]
    df = df[~df.iloc[:, 0].str.startswith('Fund')]
    df = df[~df.iloc[:, 0].str.startswith('Note')]
    df = df[~df.iloc[:, 0].str.startswith('Source')]
    df = df[~df.iloc[:, 0].str.startswith('nan')]
    df = df.reset_index(drop=True)
    return df

def process_file(uploaded_file):
    file_content = uploaded_file.read()
    filename = uploaded_file.name
    file_extension = filename.split('.')[-1].lower()

    if file_extension == 'csv':
        try:
            df = pd.DataFrame()
            for skiprows in [0, 1, 2, 3]:
                try:
                    df = pd.read_csv(
                        io.StringIO(file_content.decode('utf-8')),
                        skiprows=skiprows,
                        on_bad_lines='skip'
                    )
                    if len(df.columns) > 2:
                        break
                except Exception:
                    continue
            df = clean_dataframe(df)
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return pd.DataFrame()

    elif file_extension == 'pdf':
        try:
            reader = PdfReader(io.BytesIO(file_content))
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text()
            gemini_prompt = (
                "Extract structured data from the following document text. "
                "Ignore any header metadata, footnotes, or footer text. "
                "Focus only on the main data table. "
                "Return the data in JSON format as an array of objects. "
                "Document text:\n" + text_content[:30000]
            )
            response = gemini_model.generate_content(gemini_prompt)
            structured_data = json.loads(response.text)
            df = pd.DataFrame(structured_data)
            df = clean_dataframe(df)
            return df
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return pd.DataFrame()

    elif file_extension in ['xlsx', 'xls']:
        try:
            df = pd.DataFrame()
            for skiprows in [0, 1, 2, 3]:
                try:
                    df = pd.read_excel(
                        io.BytesIO(file_content),
                        skiprows=skiprows
                    )
                    if len(df.columns) > 2:
                        break
                except Exception:
                    continue
            df = clean_dataframe(df)
            return df
        except Exception as e:
            st.error(f"Error reading Excel: {e}")
            return pd.DataFrame()

    else:
        st.error("Unsupported file type.")
        return pd.DataFrame()

st.set_page_config(page_title="Financial Data Normalizer", page_icon="📊")
st.title("📊 Financial Data Normalizer")
st.write("Upload any financial document and get back clean, standardized data — instantly.")
st.info("📂 Supports PDF, CSV, Excel and more — no manual formatting needed.")

uploaded_file = st.file_uploader(
    "Upload your financial document here",
    type=["pdf", "csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        with st.spinner("Processing your file..."):
            df = process_file(uploaded_file)
        if not df.empty:
            st.success("✅ Done! Here's your standardized data:")
            st.dataframe(df)
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download as CSV",
                data=csv,
                file_name="normalized_data.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No data could be extracted from your file.")
    except Exception as e:
        st.error("❌ Something went wrong. Please try again.")
