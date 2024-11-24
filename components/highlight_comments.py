import streamlit as st

def render_highlight_comment_section(document_content):
    """
    Renderiza el documento con funcionalidad para seleccionar texto, resaltarlo y añadir comentarios.
    """
    st.markdown(
        """
        <style>
        .highlight {
            background-color: yellow;
            font-weight: bold;
            cursor: pointer;
        }
        .comment-box {
            margin-top: 10px;
            padding: 10px;
            border-left: 3px solid #007BFF;
            background-color: #f8f9fa;
            font-size: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Inicializa el estado de las anotaciones y comentarios si no existe
    if "highlights" not in st.session_state:
        st.session_state["highlights"] = []
    if "comments" not in st.session_state:
        st.session_state["comments"] = []

    # Renderiza el contenido del documento
    st.write("### Documento")
    document_html = document_content
    for highlight in st.session_state["highlights"]:
        document_html = document_html.replace(
            highlight, f'<span class="highlight">{highlight}</span>'
        )
    st.markdown(document_html, unsafe_allow_html=True)

    # Entrada para seleccionar texto
    selected_text = st.text_input("Texto seleccionado para resaltar:")
    if st.button("Añadir subrayado"):
        if selected_text and selected_text not in st.session_state["highlights"]:
            st.session_state["highlights"].append(selected_text)
            st.session_state["comments"].append("")  # Placeholder para comentarios
            st.success("Texto resaltado correctamente.")

    # Mostrar y permitir editar comentarios
    st.write("### Comentarios")
    for i, highlight in enumerate(st.session_state["highlights"]):
        st.text_area(
            f"Comentario para: {highlight}",
            value=st.session_state["comments"][i],
            key=f"comment_{i}",
            on_change=update_comment,
            args=(i,),
        )


def update_comment(index):
    """
    Actualiza el comentario asociado a un texto resaltado.
    """
    st.session_state["comments"][index] = st.session_state[f"comment_{index}"]