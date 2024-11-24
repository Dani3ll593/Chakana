import streamlit as st
from utils.file_handler import load_document, process_document
from utils.comment_manager import CommentManager

# Inicializar gestor de comentarios
comment_manager = CommentManager()

st.set_page_config(layout="wide")
st.title("Gestor de Documentos con Comentarios")

# CSS para estilizar la interfaz como Word
st.markdown("""
    <style>
    .document-container {
        background-color: #f9f9f9;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 5px;
        max-height: 70vh;
        overflow-y: auto;
    }
    .comment-container {
        background-color: #ffffff;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .highlight {
        background-color: #fffdcc;
    }
    </style>
""", unsafe_allow_html=True)

# Carga del documento
uploaded_file = st.file_uploader("Cargar documento (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"])
if uploaded_file:
    try:
        # Cargar y procesar documento
        content = load_document(uploaded_file)
        sections = process_document(content)
        
        # Interfaz de usuario
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("Visualización del Documento")
            st.markdown('<div class="document-container">', unsafe_allow_html=True)
            for i, section in enumerate(sections):
                section_html = f'<p id="section_{i}">{section}</p>'
                if i == comment_manager.get_active_section():
                    section_html = f'<span class="highlight">{section_html}</span>'
                st.markdown(section_html, unsafe_allow_html=True)
                if st.button(f"Seleccionar Sección {i + 1}", key=f"section_btn_{i}"):
                    comment_manager.set_active_section(i)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.subheader("Panel de Comentarios")
            active_section = comment_manager.get_active_section()
            if active_section is not None:
                st.write(f"Sección seleccionada: {active_section + 1}")
                comment_text = st.text_area("Agregar comentario", key=f"comment_{active_section}")
                if st.button("Guardar comentario", key="save_comment"):
                    comment_manager.add_comment(active_section, comment_text)
            st.markdown('<div class="comment-container">', unsafe_allow_html=True)
            st.write("Comentarios:")
            for idx, (section, comment) in enumerate(comment_manager.get_comments().items()):
                st.markdown(f"<strong>Sección {section + 1}:</strong> {comment}", unsafe_allow_html=True)
                if st.button("Eliminar", key=f"delete_{idx}"):
                    comment_manager.delete_comment(section)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Exportar documento con comentarios
        if st.button("Exportar Documento"):
            output_path = comment_manager.export_with_comments(uploaded_file.name, content, sections)
            st.success(f"Documento exportado: {output_path}")

    except Exception as e:
        st.error(f"Error al procesar el documento: {e}")