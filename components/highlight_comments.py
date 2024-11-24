import streamlit as st

def render_highlight_comment_section(document_content):
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
            border-left: 2px solid blue;
            background-color: #f9f9f9;
            font-size: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Inicializa estado para subrayados y comentarios
    if "highlights" not in st.session_state:
        st.session_state["highlights"] = []
    if "comments" not in st.session_state:
        st.session_state["comments"] = []

    # Mostrar el documento con subrayados aplicados
    st.write("### Documento")
    document_html = document_content
    for highlight in st.session_state["highlights"]:
        document_html = document_html.replace(
            highlight, f'<span class="highlight">{highlight}</span>'
        )
    st.markdown(document_html, unsafe_allow_html=True)

    # Selección y subrayado de texto
    selected_text = st.text_input("Texto seleccionado para resaltar:")
    if st.button("Añadir subrayado"):
        if selected_text and selected_text not in st.session_state["highlights"]:
            st.session_state["highlights"].append(selected_text)
            st.session_state["comments"].append("")  # Placeholder para comentario
            st.success("Subrayado añadido correctamente.")

    # Mostrar comentarios asociados
    st.write("### Comentarios")
    for i, highlight in enumerate(st.session_state["highlights"]):
        st.text_area(
            f"Comentario para: {highlight}",
            value=st.session_state["comments"][i],
            key=f"comment_{i}",
            on_change=update_comment,
            args=(i,)
        )


def update_comment(index):
    """
    Actualiza un comentario específico basado en la posición del subrayado.
    """
    st.session_state["comments"][index] = st.session_state[f"comment_{index}"]