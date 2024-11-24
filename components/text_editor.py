import streamlit as st

# Editor de texto con funcionalidades básicas
def text_editor(text):
    st.session_state.text = st.text_area("Editor de texto", text, height=400, key="editor")
    st.write("Seleccione texto y utilice las opciones del menú contextual para añadir comentarios o analizar.")
    context_menu()