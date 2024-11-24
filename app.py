import streamlit as st
from utils.file_handler import load_document, process_document
from utils.comment_manager import CommentManager

# Inicializar gestor de comentarios
comment_manager = CommentManager()

st.set_page_config(layout="wide")
st.title("Gestor de Documentos")

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
            for i, section in enumerate(sections):
                if st.button(f"Seleccionar Sección {i + 1}", key=f"section_{i}"):
                    comment_manager.set_active_section(i)
                st.write(section)

        with col2:
            st.subheader("Panel de Comentarios")
            active_section = comment_manager.get_active_section()
            if active_section is not None:
                comment_text = st.text_area("Agregar comentario", key=f"comment_{active_section}")
                if st.button("Guardar comentario", key="save_comment"):
                    comment_manager.add_comment(active_section, comment_text)
            st.write("Comentarios:")
            for idx, (section, comment) in enumerate(comment_manager.get_comments().items()):
                st.write(f"Sección {section + 1}: {comment}")
                if st.button("Eliminar", key=f"delete_{idx}"):
                    comment_manager.delete_comment(section)
        
        # Exportar documento con comentarios
        if st.button("Exportar Documento"):
            output_path = comment_manager.export_with_comments(uploaded_file.name, content, sections)
            st.success(f"Documento exportado: {output_path}")

    except Exception as e:
        st.error(f"Error al procesar el documento: {e}")
