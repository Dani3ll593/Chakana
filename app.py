import streamlit as st
from components.document_loader import load_document
from components.highlight_comments import render_highlight_comment_section
from components.ai_analysis import analyze_text
from components.persistence import save_annotations, export_document

# Configuración general de la aplicación
st.set_page_config(
    layout="wide",
    page_title="📄 Document Review App",
    page_icon="📚"
)

# Estilo inicial
st.markdown("""
<style>
    .main-container {
        padding-top: 20px;
    }
    .sidebar .stButton>button {
        color: white;
        background-color: #4CAF50; /* Green */
        border: none;
        border-radius: 4px;
        font-size: 16px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .highlight {
        background-color: yellow;
        font-weight: bold;
        cursor: pointer;
    }
    .comment-box {
        margin-top: 10px;
        padding: 10px;
        border-left: 2px solid blue;
        background-color: #f9f9f9;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.title("📚 Document Review App")
st.markdown("Simplifica la revisión de documentos con herramientas de **anotación, comentarios** y análisis asistido por **IA**.")

# Sección: Cargar y visualizar documentos
with st.sidebar:
    st.header("📂 Cargar Documento")
    file = st.file_uploader(
        "Sube un archivo Word (.docx) o PDF (.pdf):",
        type=["docx", "pdf"],
        help="Selecciona un documento para empezar."
    )
    st.markdown("---")
    st.header("⚙️ Acciones")

if file:
    # Cargar documento
    with st.spinner("📥 Procesando documento..."):
        document_content, file_type = load_document(file)
        st.session_state['document'] = document_content
        st.session_state['file_type'] = file_type
        st.success("✅ Documento cargado exitosamente.")
    
    # Visualización del documento
    st.subheader("📄 Visualización del Documento")
    st.markdown("Interactúa con el texto subrayando y añadiendo comentarios.")
    col1, col2 = st.columns([3, 1])
    with col1:
        render_highlight_comment_section(st.session_state['document'])
    with col2:
        st.markdown("### Comentarios")
        if "document" in st.session_state:
    st.markdown("---")
    st.subheader("🖍️ Subrayar y Añadir Comentarios")
    st.write("Selecciona texto y añade comentarios para mejorar la revisión del documento.")
    col1, col2 = st.columns([3, 1])
    with col1:
        render_highlight_comment_section(st.session_state['document'])
    with col2:
        st.markdown("### Comentarios")
        if "comments" in st.session_state and st.session_state["comments"]:
            for i, comment in enumerate(st.session_state["comments"]):
                st.markdown(
                    f'<div class="comment-box"><b>Texto Subrayado:</b> {st.session_state["highlights"][i]}<br><b>Comentario:</b> {comment}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.write("No hay comentarios aún. Selecciona texto en el documento para añadir comentarios.")

# Sección: Análisis con IA
if "document" in st.session_state:
    st.markdown("---")
    st.subheader("🧠 Análisis con Inteligencia Artificial")
    st.write("Selecciona texto y utiliza el análisis asistido por IA para evaluar la calidad.")
    if st.button("🔍 Analizar Texto Seleccionado"):
        if "highlighted_text" in st.session_state:
            with st.spinner("🔄 Enviando texto al modelo de IA..."):
                analysis_results = analyze_text(st.session_state['highlighted_text'])
                st.success("✅ Análisis completado.")
                st.markdown("**Resultados del Análisis:**")
                st.write(analysis_results)
        else:
            st.warning("⚠️ No se ha seleccionado texto para analizar.")

# Persistencia y exportación
if "document" in st.session_state:
    st.markdown("---")
    st.subheader("💾 Guardar y Exportar Anotaciones")
    st.write("Guarda tus comentarios y subrayados para seguir trabajando más tarde o exporta el documento con anotaciones.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Guardar Anotaciones"):
            save_annotations()
            st.success("✅ Anotaciones guardadas exitosamente.")
    with col2:
        if st.button("📤 Exportar Documento"):
            export_document()
            st.success("✅ Documento exportado exitosamente.")

# Mensaje para usuarios nuevos
if not file:
    st.info(
        "👈 Carga un documento para comenzar. Utiliza la barra lateral para explorar las herramientas."
    )