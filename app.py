import streamlit as st
from utils.file_handler import load_document, process_document
from utils.navigation import generate_index
from utils.comments import CommentManager

# Inicializar gestor de comentarios
comment_manager = CommentManager()

# Configuración de página
st.set_page_config(page_title="Gestor Interactivo de Documentos", layout="wide")
st.title("📄 Gestor Interactivo de Documentos")

# Información introductoria
st.markdown("""
Bienvenido al gestor interactivo de documentos. Aquí puedes cargar archivos en formato `.docx`, `.pdf` o `.txt`, 
explorar su contenido a través de un índice interactivo, y añadir comentarios directamente a secciones específicas. 
""")

# Carga del documento
uploaded_file = st.file_uploader(
    "📤 Cargar documento", 
    type=["docx", "pdf", "txt"],
    help="Selecciona un archivo compatible para procesarlo."
)

if uploaded_file:
    try:
        # Cargar y procesar documento
        with st.spinner("Procesando el documento..."):
            content, structure = load_document(uploaded_file)
            sections = process_document(content, structure)
            index = generate_index(structure)

        # Mostrar un mensaje de éxito
        st.success("¡Documento procesado correctamente!")

        # Dividir la interfaz en dos columnas: índice y contenido
        col1, col2 = st.columns([1, 3], gap="medium")

        # Panel izquierdo: Índice de contenido
        with col1:
            st.subheader("📑 Índice de Contenido")
            st.markdown("""
            Usa el índice para navegar rápidamente entre las secciones del documento.
            """)

            # Mostrar un árbol de navegación (expandible)
            with st.expander("Navegar por el documento"):
                for key, value in index.items():
                    if st.button(value, key=f"navigate_{key}"):
                        comment_manager.set_active_section(key)

        # Panel derecho: Contenido del documento
        with col2:
            st.subheader("📖 Contenido del Documento")

            # Verificar si hay una sección activa
            active_section = comment_manager.get_active_section()
            if active_section:
                # Mostrar contenido de la sección activa
                st.markdown(f"### {active_section}")
                st.write(index[active_section])

                # Comentarios asociados a la sección
                st.markdown("#### ✍️ Agregar comentario:")
                comment_text = st.text_area(
                    "Escribe tu comentario aquí:",
                    key=f"comment_box_{active_section}"
                )
                if st.button("💾 Guardar comentario", key=f"save_comment_{active_section}"):
                    comment_manager.add_comment(active_section, comment_text)
                    st.success("Comentario guardado con éxito.")

                # Mostrar comentarios existentes
                st.markdown("#### 🗒️ Comentarios existentes:")
                comments = comment_manager.get_comments().get(active_section, [])
                if comments:
                    for idx, comment in enumerate(comments, 1):
                        st.markdown(f"- {comment} (Comentario {idx})")
                else:
                    st.info("No hay comentarios asociados a esta sección.")
            else:
                st.info("Selecciona una sección desde el índice para comenzar.")

        # Exportar documento con comentarios
        st.markdown("---")
        st.subheader("📤 Exportar Documento")
        if st.button("Exportar con comentarios"):
            st.warning("Función de exportación en desarrollo. ¡Pronto estará disponible!")

    except Exception as e:
        st.error(f"Error al procesar el documento: {e}")
else:
    # Mostrar un mensaje cuando no hay documento cargado
    st.info("Por favor, carga un documento para comenzar.")