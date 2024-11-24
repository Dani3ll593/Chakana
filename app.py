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
    
    # Visualización del documento con funcionalidad interactiva
    st.subheader("📄 Visualización del Documento")
    st.markdown("Interactúa con el texto subrayando y añadiendo comentarios.")
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