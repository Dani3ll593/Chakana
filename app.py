import os
import streamlit as st
from dotenv import load_dotenv

# Intentar importar módulos de utils
try:
    from utils.aiml_client import AIMLClient
    from utils.file_utils import extract_text
    from utils.text_analysis import analyze_text, generate_wordcloud
except ImportError as e:
    st.error(f"Error al importar módulos: {e}")
    raise

# Cargar variables de entorno
load_dotenv()
API_URL = os.getenv("AIML_BASE_URL")
API_KEY = os.getenv("AIML_API_KEY")

# Validar configuraciones de la API
if not API_URL or not API_KEY:
    st.error("Faltan configuraciones en el archivo .env para la API.")
    raise ValueError("Configuración inválida para la API.")

# Inicialización del cliente de IA
client = AIMLClient(api_url=API_URL, api_key=API_KEY)

# Configuración de la página
st.set_page_config(page_title="Procesador de Documentos Inteligente", layout="wide")
st.title("📄 Procesador de Documentos Inteligente")

# Introducción
st.markdown("""
Esta herramienta permite:
- Analizar redacción y coherencia de textos.
- Evaluar calidad académica por secciones.
- Generar reportes personalizados.
""")

# Widget para cargar archivo
uploaded_file = st.sidebar.file_uploader("📤 Cargar documento", type=["txt", "pdf", "docx"])

# Área para texto pegado
st.subheader("Pegue su texto aquí")
pasted_text = st.text_area("Pegue un párrafo:", placeholder="Escriba o pegue texto aquí...", height=200)

# Análisis de texto pegado
if st.button("🔍 Analizar texto pegado"):
    if pasted_text.strip():
        with st.spinner("Analizando texto..."):
            try:
                basic_analysis = analyze_text(pasted_text)
                st.write("### Resultados del análisis básico:")
                st.json(basic_analysis)

                advanced_analysis = client.analyze_academic_quality(pasted_text)
                st.write("### Resultados del análisis avanzado:")
                st.json(advanced_analysis)
            except Exception as e:
                st.error(f"Error al analizar el texto: {e}")
    else:
        st.warning("Por favor, ingrese texto para analizar.")

# Procesamiento de archivo cargado
if uploaded_file:
    with st.spinner("Procesando archivo..."):
        try:
            text = extract_text(uploaded_file)
            st.success("Documento cargado con éxito.")
            st.write(f"### Contenido del documento ({len(text.split())} palabras):")
            st.text_area("Texto del documento", text, height=300)

            if st.button("🔍 Analizar archivo"):
                with st.spinner("Analizando archivo..."):
                    try:
                        basic_analysis = analyze_text(text)
                        st.write("### Resultados del análisis básico:")
                        st.json(basic_analysis)

                        st.write("### Análisis por Sección:")
                        results = client.analyze_academic_quality(text)
                        for result in results:
                            st.write(f"**Sección: {result['section_title']}**")
                            st.json(result.get("analysis", result.get("error", "No se encontró análisis.")))

                        st.subheader("Nube de Palabras")
                        wordcloud_fig = generate_wordcloud(text)
                        st.pyplot(wordcloud_fig)
                    except Exception as e:
                        st.error(f"Error al analizar el archivo: {e}")
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")