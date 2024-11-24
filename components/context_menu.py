import streamlit as st
from services.api_client import analyze_text_with_ai
from utils.comment_manager import save_comment

# Menú contextual para agregar comentarios y analizar texto
def context_menu():
    if st.button("Añadir comentario"):
        add_comment()
    if st.button("Analizar con IA"):
        analyze_selection()

def add_comment():
    selected_text = st.text_area("Texto seleccionado:", "", placeholder="Pegue el texto aquí", key="selected_text")
    if selected_text:
        comment = st.text_input("Ingrese su comentario", key="comment_input")
        if st.button("Guardar comentario"):
            save_comment(selected_text, "Usuario", comment)
            st.success("Comentario añadido exitosamente.")

def analyze_selection():
    selected_text = st.text_area("Texto seleccionado:", "", placeholder="Pegue el texto aquí", key="selected_analysis_text")
    if selected_text:
        analysis = analyze_text_with_ai(selected_text)
        st.json(analysis)