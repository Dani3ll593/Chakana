import os
import streamlit as st
from dotenv import load_dotenv
from utils.api_handler import analyze_text, generate_report
from utils.document_processor import process_uploaded_file

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(page_title="Revisión de Documentos", layout="wide")
st.title("📄 Revisor de Redacción y Coherencia")

# Introducción de la herramienta
st.markdown("""
Esta herramienta analiza documentos para verificar:
- **Redacción y coherencia**.
- **Alineación con objetivos de investigación**.
- **Cumplimiento de estándares académicos**.

Carga tu archivo para comenzar.
""")

# Widget para cargar documento
uploaded_file = st.file_uploader("📤 Cargar documento", type=["docx", "pdf", "txt"])

if uploaded_file:
    with st.spinner("Procesando el archivo..."):
        try:
            # Procesar archivo cargado
            content, sections = process_uploaded_file(uploaded_file)

            # Barra lateral: Navegación por secciones
            st.sidebar.header("📚 Navegación del Documento")
            selected_section = st.sidebar.selectbox(
                "Selecciona una sección para analizar:",
                options=list(sections.keys()),
                format_func=lambda x: f"Sección: {x}"
            )

            # Mostrar contenido de la sección seleccionada
            st.subheader(f"📖 Contenido de la Sección: {selected_section}")
            st.write(sections[selected_section])

            # Análisis de la sección
            if st.button("🔍 Analizar esta sección"):
                with st.spinner("Realizando análisis..."):
                    try:
                        analysis_result = analyze_text(sections[selected_section])
                        st.success("Análisis completado:")
                        st.json(analysis_result)
                    except Exception as e:
                        st.error(f"Error al realizar el análisis: {e}")

            # Generar reporte de observaciones
            if st.button("📋 Generar Reporte de Observaciones"):
                with st.spinner("Generando reporte..."):
                    try:
                        report = generate_report(sections)
                        st.success("Reporte generado con éxito:")
                        st.download_button(
                            label="Descargar Reporte",
                            data=report,
                            file_name="reporte_observaciones.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Error al generar el reporte: {e}")

        except Exception as e:
            st.error(f"Error al procesar el documento: {e}")
else:
    st.info("Por favor, carga un documento para comenzar.")