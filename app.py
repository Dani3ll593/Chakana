import os
import streamlit as st
from dotenv import load_dotenv
from utils.aiml_client import AIMLClient
from utils.file_utils import extract_text
from utils.text_analysis import analyze_text

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
st.sidebar.header("Carga de Documentos")
uploaded_file = st.sidebar.file_uploader("Carga un documento (.txt, .pdf, .docx):", type=["txt", "pdf", "docx"])

# Área para pegar texto
st.subheader("Pegue su texto aquí para analizar")
pasted_text = st.text_area("Pegue un párrafo:", placeholder="Escriba o pegue texto aquí...", height=200)

if st.button("Analizar texto con IA"):
    if pasted_text.strip():
        with st.spinner("Analizando texto con IA..."):
            try:
                analysis_results = analyze_text(pasted_text)
                st.write("### Resultados del análisis:")
                st.json(analysis_results)
            except Exception as e:
                st.error(f"Error al analizar el texto: {e}")
    else:
        st.warning("Por favor, pegue un texto antes de analizar.")

# Procesamiento del archivo si se carga
if uploaded_file:
    with st.spinner("Cargando documento..."):
        text = extract_text(uploaded_file)
        st.success("Documento cargado con éxito.")
        st.write(f"### Contenido del documento ({len(text.split())} palabras):")
        st.text_area("Texto del documento", text, height=300)

    # Botón para analizar el texto del archivo
    if st.button("Analizar texto del documento con IA"):
        with st.spinner("Analizando texto del documento con IA..."):
            try:
                analysis_results = analyze_text(text)
                st.write("### Resultados del análisis:")
                st.json(analysis_results)
            except Exception as e:
                st.error(f"Error al analizar el texto: {e}")

st.sidebar.markdown("**Hecho con ❤️ por Streamlit**")