import os

import streamlit as st
from dotenv import load_dotenv

from generate_response import generate_document_response

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
# Page title
st.set_page_config(page_title=" 📄? Knowledge Base")
st.title("📄? Knowledge Base")
# File upload
uploaded_file = st.file_uploader("Upload an article", type="txt")
# Query text
query_text = st.text_input(
    "Enter your question:",
    placeholder="Ask the knowlege base a question",
    disabled=not uploaded_file,
)
# Form input and query
result = []
with st.form("myform", clear_on_submit=True):
    submitted = st.form_submit_button(
        "Submit", disabled=not (uploaded_file and query_text)
    )
    if submitted:
        with st.spinner("Calculating..."):
            response = generate_document_response(
                uploaded_file=submitted, query_text=query_text
            )
            result.append(response)
if len(result):
    st.info(response)
