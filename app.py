import streamlit as st
from components.document_loader import load_document
from components.highlight_comments import render_highlight_comment_section
from components.ai_analysis import analyze_text
from components.persistence import save_annotations, export_document

st.set_page_config(layout="wide", page_title="Document Review App")

# Sección: Cargar y visualizar documentos
st.sidebar.title("Document Loader")
file = st.sidebar.file_uploader("Upload a document", type=["docx", "pdf"])
if file:
    document_content, file_type = load_document(file)
    st.session_state['document'] = document_content
    st.session_state['file_type'] = file_type
    st.write(document_content)

# Sección: Subrayado y comentarios
if "document" in st.session_state:
    render_highlight_comment_section(st.session_state['document'])

# Sección: Análisis con IA
if st.sidebar.button("Analyze with AI") and "highlighted_text" in st.session_state:
    analysis_results = analyze_text(st.session_state['highlighted_text'])
    st.sidebar.write(analysis_results)

# Persistencia y exportación
if st.sidebar.button("Save Annotations"):
    save_annotations()
if st.sidebar.button("Export Document"):
    export_document()