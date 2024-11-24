import streamlit as st
from services.api_client import analyze_text_with_ai

# Menú contextual para agregar comentarios y analizar texto
def context_menu():
    st.write("Opciones del menú contextual:")
    st.button("Añadir comentario", on_click=add_comment)
    st.button("Analizar con IA", on_click=analyze_selection)

def add_comment():
    selected_text = st.session_state.get("text")
    if selected_text:
        comment = st.text_input("Ingrese su comentario", key="comment_input")
        if comment:
            st.session_state.comments = st.session_state.get("comments", [])
            st.session_state.comments.append({"text": selected_text, "comment": comment})
            st.success("Comentario añadido exitosamente.")

def analyze_selection():
    selected_text = st.session_state.get("text")
    if selected_text:
        analysis = analyze_text_with_ai(selected_text)
        st.json(analysis)