import streamlit as st
from components.context_menu import context_menu

# Editor de texto con menú contextual
def text_editor(text):
    if "text" not in st.session_state:
        st.session_state["text"] = text

    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state["text"] = st.text_area("Editor de texto", st.session_state["text"], height=400, key="editor")
        context_menu()
    with col2:
        st.markdown("### Opciones")
        st.button("Añadir Comentario")
        st.button("Analizar Selección")