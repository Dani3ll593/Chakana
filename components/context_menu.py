import streamlit as st
from services.api_client import analyze_text_with_ai
from utils.comment_manager import save_comment

# Menú contextual para añadir comentarios y analizar con IA
def context_menu():
    selected_text = st.text_area("Texto seleccionado", "", placeholder="Pegue texto aquí para análisis.", key="selected_text")
    if st.button("Analizar con IA"):
        if selected_text:
            analysis = analyze_text_with_ai(selected_text)
            st.write("**Resultados del análisis:**")
            st.write(analysis)
        else:
            st.warning("Seleccione texto antes de analizar.")
    if st.button("Añadir Comentario"):
        comment = st.text_input("Ingrese su comentario", key="comment_input")
        if comment:
            save_comment(selected_text, "Usuario", comment)
            st.success("Comentario añadido.")