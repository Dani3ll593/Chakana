import os
import streamlit as st
from dotenv import load_dotenv
from utils.aiml_client import AIMLClient
from utils.file_utils import load_file, save_file, extract_text
from utils.text_analysis import analyze_text, summarize_text, generate_wordcloud

# Cargar variables de entorno
load_dotenv()
API_URL = os.getenv("AIML_BASE_URL")
API_KEY = os.getenv("AIML_API_KEY")

# Inicialización del cliente IA
client = AIMLClient(api_url=API_URL, api_key=API_KEY)

# Configuración de la página de Streamlit
st.set_page_config(page_title="Procesador de Documentos Inteligente", layout="wide")

# Cabecera
st.title("📄 Procesador de Documentos Inteligente")

# Barra lateral para cargar archivos
st.sidebar.header("Carga y Configuración")
uploaded_file = st.sidebar.file_uploader("Carga un documento (.txt, .pdf, .docx):", type=["txt", "pdf", "docx"])
action = st.sidebar.radio("Acción", ["Visualizar", "Analizar", "Resumir"])

# Procesamiento del archivo
if uploaded_file:
    with st.spinner("Cargando documento..."):
        text = extract_text(uploaded_file)
        st.success("Documento cargado con éxito.")
        st.write(f"### Contenido del documento ({len(text.split())} palabras):")
        st.text_area("Texto", text, height=300)

    if action == "Analizar":
        st.subheader("Análisis del texto")
        with st.spinner("Analizando texto..."):
            analysis_results = analyze_text(text)
            st.json(analysis_results)

    elif action == "Resumir":
        st.subheader("Resumen del texto")
        with st.spinner("Resumiendo texto..."):
            summary = summarize_text(client, text)
            st.write(f"### Resumen:")
            st.markdown(summary)

# Widgets para edición de texto
st.sidebar.header("Herramientas Interactivas")
if "text" in locals():
    new_text = st.sidebar.text_area("Edita el texto:", text)
    if st.sidebar.button("Guardar texto modificado"):
        save_file(new_text, "edited_text.txt")
        st.sidebar.success("Texto modificado guardado.")

# Nube de palabras
if st.sidebar.checkbox("Generar Nube de Palabras"):
    st.subheader("Nube de Palabras")
    with st.spinner("Generando nube..."):
        wordcloud_fig = generate_wordcloud(text)
        st.pyplot(wordcloud_fig)

# Opciones para exportar
if st.sidebar.button("Exportar texto a archivo"):
    file_path = save_file(text, "output_text.txt")
    st.sidebar.download_button("Descargar Texto Exportado", data=open(file_path, "rb"), file_name="output_text.txt")

st.sidebar.markdown("**Hecho con ❤️ por Streamlit**")