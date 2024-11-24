import streamlit as st
from utils.file_handler import load_document, process_document
from utils.navigation import generate_index
from utils.comments import CommentManager

# Inicializar gestor de comentarios
comment_manager = CommentManager()

# Configuración de la página
st.set_page_config(page_title="Gestor Interactivo de Documentos", layout="wide")
st.title("📄 Gestor Interactivo de Documentos")

# Carga del documento
uploaded_file = st.file_uploader("📤 Cargar documento (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"])

if uploaded_file:
    try:
        # Cargar y procesar documento
        with st.spinner("Procesando el documento..."):
            content, structure = load_document(uploaded_file)
            # Corregir la llamada a process_document pasándole el argumento 'structure'
            sections = process_document(content, structure)
            index = generate_index(structure)

        # Mostrar mensaje de éxito
        st.success("¡Documento procesado correctamente!")

        # Crear dos columnas para la interfaz
        col1, col2 = st.columns([1, 3])

        # Panel izquierdo: Índice
        with col1:
            st.subheader("📑 Índice de Contenido")
            selected_section = st.selectbox("Navegar:", list(index.keys()), key="navigation")
            if st.button("Ir a sección"):
                comment_manager.set_active_section(selected_section)

        # Panel derecho: Contenido
        with col2:
            st.subheader("📖 Contenido del Documento")
            active_section = comment_manager.get_active_section()
            if active_section:
                st.markdown(f"### {active_section}")
                st.write(index[active_section])

                # Mostrar y agregar comentarios
                st.markdown("#### ✍️ Agregar comentario:")
                comment_text = st.text_area("Escribe tu comentario aquí:")
                if st.button("💾 Guardar comentario"):
                    comment_manager.add_comment(active_section, comment_text)
                    st.success("Comentario guardado con éxito.")

                # Mostrar comentarios existentes
                st.markdown("#### 🗒️ Comentarios existentes:")
                comments = comment_manager.get_comments(active_section)
                if comments:
                    for idx, comment in enumerate(comments, 1):
                        st.markdown(f"- {idx}: {comment}")
                else:
                    st.info("No hay comentarios para esta sección.")
            else:
                st.info("Selecciona una sección desde el índice para comenzar.")

    except Exception as e:
        st.error(f"Error al procesar el documento: {e}")
else:
    st.info("Por favor, carga un documento para comenzar.")