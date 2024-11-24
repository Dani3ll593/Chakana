import streamlit as st
from docx import Document
from PyPDF2 import PdfReader

def load_document(file):
    if file.name.endswith('.docx'):
        doc = Document(file)
        content = ''.join([f'<p>{p.text}</p>' for p in doc.paragraphs])
        return content, 'docx'
    elif file.name.endswith('.pdf'):
        pdf = PdfReader(file)
        content = ''.join([f'<p>{page.extract_text()}</p>' for page in pdf.pages])
        return content, 'pdf'
    else:
        st.error("Unsupported file type.")
        return None, None