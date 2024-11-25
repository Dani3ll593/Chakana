import os
import streamlit as st
from dotenv import load_dotenv
import logging
from fpdf import FPDF

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

st.set_page_config(page_title="Chakana - Procesador de Documentos Inteligente", layout="wide", initial_sidebar_state="auto")
st.title("📄 Chakana - Procesador de Documentos Inteligente")

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

col1, col2 = st.columns([1, 1])

def export_report(analysis_result, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3, file_name="reporte_analisis.pdf"):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, "Reporte de Análisis de Calidad Académica")
        pdf.ln(10)
        pdf.multi_cell(0, 10, "Análisis del Texto:")
        pdf.ln(5)
        pdf.multi_cell(0, 10, str(analysis_result))
        pdf.ln(10)
        pdf.multi_cell(0, 10, "Resumen del Análisis:")
        pdf.ln(5)
        pdf.multi_cell(0, 10, summary_paragraph_1)
        pdf.ln(10)
        pdf.multi_cell(0, 10, summary_paragraph_2)
        pdf.ln(10)
        pdf.multi_cell(0, 10, summary_paragraph_3)
        pdf.output(file_name)
        return file_name
    except Exception as e:
        logging.error(f"Error al exportar el reporte: {e}")
        raise ValueError(f"Error al exportar el reporte: {e}")

def split_text(text, max_length=5000):
    """Divide el texto en partes más pequeñas de longitud máxima."""
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def perform_analysis(text):
    try:
        if not text or len(text.strip()) == 0:
            raise ValueError("El texto proporcionado es inválido o está vacío.")
        analysis_result = analyze_text(text)
        text_segments = split_text(text)
        academic_quality_results = []
        for segment in text_segments:
            academic_quality_result = client.analyze_academic_quality(segment)
            academic_quality_results.extend(academic_quality_result)
        logging.info(f"Academic Quality Result: {academic_quality_results}")
        if academic_quality_results and 'analysis' in academic_quality_results[0]:
            summary_paragraph_1 = academic_quality_results[0]['analysis'].get('summary_paragraph_1', "No se pudo generar el resumen.")
            summary_paragraph_2 = academic_quality_results[0]['analysis'].get('summary_paragraph_2', "No se pudo generar el resumen.")
            summary_paragraph_3 = (
                f"Análisis de sentimiento: {analysis_result['Análisis de sentimiento']}\n"
                f"Legibilidad: {analysis_result['Legibilidad']}\n"
                f"Diversidad léxica: {analysis_result['Diversidad léxica']}"
            )
            return analysis_result, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3
        else:
            summary_paragraph_1 = "Error en la generación del análisis."
            summary_paragraph_2 = "Consulta los logs para más detalles."
            summary_paragraph_3 = ""
            return analysis_result, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3
    except ValueError as e:
        logging.error(f"Error al analizar el texto: {e}")
        st.error(f"Error al analizar el texto: {e}")
        return None, None, None, None
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        st.error(f"Error inesperado: {e}")
        return None, None, None, None

with col1:
    st.subheader("Texto para Análisis")
    pasted_text = st.text_area("Pegue un párrafo:", placeholder="Escriba o pegue texto aquí...", height=200, key="pasted_text")

    if st.button("🔍 Analizar texto pegado"):
        if pasted_text.strip():
            with st.spinner("Analizando texto..."):
                analysis_result, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3 = perform_analysis(pasted_text)
                if analysis_result:
                    with col2:
                        st.subheader("Resultados del Análisis")
                        st.json(analysis_result)
                        st.markdown("### Resumen del Análisis")
                        st.write(summary_paragraph_1)
                        st.write(summary_paragraph_2)
                        st.write(summary_paragraph_3)
                        try:
                            wordcloud_image = generate_wordcloud(pasted_text)
                            st.pyplot(wordcloud_image)
                        except ValueError as e:
                            st.error(f"Error al generar la nube de palabras: {e}")
        else:
            st.warning("Por favor, ingrese texto para analizar.")

    if uploaded_file:
        if uploaded_file.size > 50 * 1024 * 1024:
            st.error("El archivo supera el límite de tamaño de 50 MB. Por favor, sube un archivo más pequeño.")
        else:
            with st.spinner("Procesando archivo..."):
                try:
                    text = extract_text(uploaded_file)
                    if not text or len(text.strip()) == 0:
                        raise ValueError("El documento cargado no contiene texto válido.")
                    st.success("Documento cargado con éxito.")
                    st.text_area("Texto del documento", text, height=300, key="uploaded_text")

                    if st.button("🔍 Analizar archivo"):
                        analysis_result, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3 = perform_analysis(text)
                        if analysis_result:
                            with col2:
                                st.subheader("Resultados del Análisis")
                                st.json(analysis_result)
                                st.markdown("### Resumen del Análisis")
                                st.write(summary_paragraph_1)
                                st.write(summary_paragraph_2)
                                st.write(summary_paragraph_3)
                                try:
                                    wordcloud_image = generate_wordcloud(text)
                                    st.pyplot(wordcloud_image)
                                except ValueError as e:
                                    st.error(f"Error al generar la nube de palabras: {e}")
                except Exception as e:
                    st.error(f"Error al procesar el archivo: {e}")

with col2:
    st.subheader("Resultados del Análisis")
    if 'analysis_result' in locals():
        st.json(analysis_result)
    if 'summary_paragraph_1' in locals() and 'summary_paragraph_2' in locals() and 'summary_paragraph_3' in locals():
        st.markdown("### Resumen del Análisis")
        st.write(summary_paragraph_1)
        st.write(summary_paragraph_2)
        st.write(summary_paragraph_3)

st.markdown("---")
st.subheader("Términos más destacados")
if 'pasted_text' in locals() and pasted_text.strip():
    try:
        wordcloud_image = generate_wordcloud(pasted_text)
        st.pyplot(wordcloud_image)
    except ValueError as e:
        st.error(f"Error al generar la nube de palabras: {e}")
elif 'text' in locals() and text.strip():
    try:
        wordcloud_image = generate_wordcloud(text)
        st.pyplot(wordcloud_image)
    except ValueError as e:
        st.error(f"Error al generar la nube de palabras: {e}")

if st.button("📄 Exportar reporte"):
    if 'analysis_result' in locals() and 'summary_paragraph_1' in locals() and 'summary_paragraph_2' in locals() and 'summary_paragraph_3' in locals():
        try:
            report_file = export_report(analysis_result, summary_paragraph_1, summary_paragraph_2, summary_paragraph_3)
            st.success(f"Reporte exportado exitosamente: {report_file}")
            with open(report_file, "rb") as file:
                btn = st.download_button(
                    label="Descargar reporte",
                    data=file,
                    file_name=report_file,
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error al exportar el reporte: {e}")
    else:
        st.warning("No hay datos de análisis disponibles para exportar.")