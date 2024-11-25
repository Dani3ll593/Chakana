import os
import streamlit as st
from dotenv import load_dotenv
import logging

try:
    from utils.aiml_client import AIMLClient
    from utils.file_utils import extract_text
    from utils.text_analysis import analyze_text, generate_wordcloud
except ImportError as e:
    st.error(f"Error al importar módulos: {e}")
    raise

load_dotenv()
API_URL = os.getenv("AIML_BASE_URL")
API_KEY = os.getenv("AIML_API_KEY")

if not API_URL or not API_KEY:
    st.error("Faltan configuraciones en el archivo .env para la API.")
    raise ValueError("Configuración inválida para la API.")

client = AIMLClient(api_url=API_URL, api_key=API_KEY)

# Configurar logging
logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Procesador de Documentos Inteligente", layout="wide", initial_sidebar_state="auto")
st.title("📄 Procesador de Documentos Inteligente")

st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .stTextArea textarea {
        border-radius: 12px;
        padding: 10px;
    }
    .stTextArea label {
        font-weight: bold;
    }
    .stMarkdown h3 {
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
Esta herramienta permite:
- Analizar redacción y coherencia de textos.
- Evaluar calidad académica por secciones.
- Generar reportes personalizados.
""")

uploaded_file = st.sidebar.file_uploader("📤 Cargar documento", type=["txt", "pdf", "docx"], accept_multiple_files=False, key="file_uploader", help="Límite de tamaño de archivo: 50 MB")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Pegue su texto aquí")
    pasted_text = st.text_area("Pegue un párrafo:", placeholder="Escriba o pegue texto aquí...", height=200, key="pasted_text")

    if st.button("🔍 Analizar texto pegado"):
        if pasted_text.strip():
            try:
                with st.spinner("Analizando texto..."):
                    analysis_result = analyze_text(pasted_text)
                    st.json(analysis_result)
                    academic_quality_result = client.analyze_academic_quality(pasted_text)
                    logging.info(f"Academic Quality Result: {academic_quality_result}")  # Agregar log para la respuesta de calidad académica
                    if academic_quality_result and 'analysis' in academic_quality_result[0]:
                        # Generar dos párrafos de resumen basados en el análisis del modelo
                        summary_paragraph_1 = academic_quality_result[0]['analysis'].get('summary_paragraph_1', "No se pudo generar el resumen.")
                        summary_paragraph_2 = academic_quality_result[0]['analysis'].get('summary_paragraph_2', "No se pudo generar el resumen.")
                        st.markdown("### Resumen del Análisis")
                        st.write(summary_paragraph_1)
                        st.write(summary_paragraph_2)
                    else:
                        st.warning("No se pudo generar el análisis de calidad académica.")
            except Exception as e:
                st.error(f"Error al analizar el texto: {e}")
        else:
            st.warning("Por favor, ingrese texto para analizar.")

if uploaded_file:
    if uploaded_file.size > 50 * 1024 * 1024:
        st.error("El archivo supera el límite de tamaño de 50 MB. Por favor, sube un archivo más pequeño.")
    else:
        try:
            with st.spinner("Procesando archivo..."):
                text = extract_text(uploaded_file)
                st.success("Documento cargado con éxito.")
                st.text_area("Texto del documento", text, height=300, key="uploaded_text")

                if st.button("🔍 Analizar archivo"):
                    analysis_result = analyze_text(text)
                    st.json(analysis_result)
                    academic_quality_result = client.analyze_academic_quality(text)
                    logging.info(f"Academic Quality Result: {academic_quality_result}")  # Agregar log para la respuesta de calidad académica
                    if academic_quality_result and 'analysis' in academic_quality_result[0]:
                        # Generar dos párrafos de resumen basados en el análisis del modelo
                        summary_paragraph_1 = academic_quality_result[0]['analysis'].get('summary_paragraph_1', "No se pudo generar el resumen.")
                        summary_paragraph_2 = academic_quality_result[0]['analysis'].get('summary_paragraph_2', "No se pudo generar el resumen.")
                        st.markdown("### Resumen del Análisis")
                        st.write(summary_paragraph_1)
                        st.write(summary_paragraph_2)
                        st.pyplot(generate_wordcloud(text))
                    else:
                        st.warning("No se pudo generar el análisis de calidad académica.")
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

with col2:
    st.subheader("Resultados del Análisis")
    if 'analysis_result' in locals():
        st.json(analysis_result)
    if 'academic_quality_result' in locals() and academic_quality_result and 'analysis' in academic_quality_result[0]:
        summary_paragraph_1 = academic_quality_result[0]['analysis'].get('summary_paragraph_1', "No se pudo generar el resumen.")
        summary_paragraph_2 = academic_quality_result[0]['analysis'].get('summary_paragraph_2', "No se pudo generar el resumen.")
        st.markdown("### Resumen del Análisis")
        st.write(summary_paragraph_1)
        st.write(summary_paragraph_2)