import os
import streamlit as st
from dotenv import load_dotenv

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

st.set_page_config(page_title="Procesador de Documentos Inteligente", layout="wide")
st.title("📄 Procesador de Documentos Inteligente")

st.markdown("""
Esta herramienta permite:
- Analizar redacción y coherencia de textos.
- Evaluar calidad académica por secciones.
- Generar reportes personalizados.
""")

uploaded_file = st.sidebar.file_uploader("📤 Cargar documento", type=["txt", "pdf", "docx"])

st.subheader("Pegue su texto aquí")
pasted_text = st.text_area("Pegue un párrafo:", placeholder="Escriba o pegue texto aquí...", height=200)

if st.button("🔍 Analizar texto pegado"):
    if pasted_text.strip():
        try:
            with st.spinner("Analizando texto..."):
                analysis_result = analyze_text(pasted_text)
                st.json(analysis_result)
                academic_quality_result = client.analyze_academic_quality(pasted_text)
                st.markdown("### Análisis de calidad académica")
                for result in academic_quality_result:
                    st.markdown(f"**{result['section_title']}**")
                    st.json(result['analysis'])
                    st.markdown(f"**Párrafo de análisis:** {result['analysis']['paragraph']}")
        except Exception as e:
            st.error(f"Error al analizar el texto: {e}")
    else:
        st.warning("Por favor, ingrese texto para analizar.")

if uploaded_file:
    try:
        with st.spinner("Procesando archivo..."):
            text = extract_text(uploaded_file)
            st.success("Documento cargado con éxito.")
            st.text_area("Texto del documento", text, height=300)

            if st.button("🔍 Analizar archivo"):
                analysis_result = analyze_text(text)
                st.json(analysis_result)
                academic_quality_result = client.analyze_academic_quality(text)
                st.markdown("### Análisis de calidad académica")
                for result in academic_quality_result:
                    st.markdown(f"**{result['section_title']}**")
                    st.json(result['analysis'])
                    st.markdown(f"**Párrafo de análisis:** {result['analysis']['paragraph']}")
                st.pyplot(generate_wordcloud(text))
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")