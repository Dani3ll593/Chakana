import streamlit as st
from components.context_menu import context_menu

# Editor de texto con funcionalidades básicas
def text_editor(text):
    if "text" not in st.session_state:
        st.session_state["text"] = text
    
    st.session_state["text"] = st.text_area("Editor de texto", st.session_state["text"], height=400, key="editor")
    st.write("Seleccione texto y utilice las opciones del menú contextual para añadir comentarios o analizar.")
    context_menu()