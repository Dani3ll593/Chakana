import streamlit as st
from utils.api_handler import analyze_text, generate_report
from utils.document_processor import process_uploaded_file
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
API_BASE_URL = os.getenv("AIML_BASE_URL", "https://api.aimlapi.com/v1")
API_KEY = os.getenv("AIML_API_KEY")

st.set_page_config(page_title="Revisión de Documentos", layout="wide")
st.title("📄 Revisor de Redacción y Coherencia")

st.markdown("""
Esta herramienta analiza documentos para verificar la redacción, coherencia con la teoría, y alineación con los objetivos de investigación.
Carga tu archivo para comenzar.
""")

# Cargar documento
uploaded_file = st.file_uploader("📤 Cargar documento", type=["docx", "pdf", "txt"])

if uploaded_file:
    with st.spinner("Procesando el archivo..."):
        try:
            content, sections = process_uploaded_file(uploaded_file)

            # Mostrar contenido dividido por secciones
            st.sidebar.header("Navegación del Documento")
            selected_section = st.sidebar.selectbox(
                "Selecciona una sección para analizar:",
                options=list(sections.keys()),
                format_func=lambda x: f"Sección: {x}"
            )

            # Mostrar contenido de la sección seleccionada
            st.subheader(f"📖 Contenido de la Sección: {selected_section}")
            st.write(sections[selected_section])

            # Análisis con la API
            if st.button("🔍 Analizar esta sección"):
                with st.spinner("Analizando..."):
                    analysis_result = analyze_text(sections[selected_section])
                    st.success("Análisis completado:")
                    st.json(analysis_result)

            # Generar reporte
            if st.button("📋 Generar Reporte de Observaciones"):
                with st.spinner("Generando reporte..."):
                    report = generate_report(sections)
                    st.success("Reporte generado:")
                    st.download_button(
                        "Descargar Reporte",
                        data=report,
                        file_name="reporte_observaciones.txt",
                        mime="text/plain"
                    )
        except Exception as e:
            st.error(f"Error al procesar el documento: {e}")
else:
    st.info("Por favor, carga un documento para comenzar.")