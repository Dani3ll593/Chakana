import streamlit as st
from components.text_editor import text_editor
from components.context_menu import context_menu
from utils.file_handler import load_word_file
import os

# Cargar estilos personalizados
def load_styles():
    try:
        with open("./static/styles.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Error al cargar los estilos CSS.")

# Configuración de la barra lateral
def configure_sidebar():
    st.sidebar.title("Opciones")
    return st.sidebar.radio("Seleccione una opción", ["Inicio", "Carga de Documento", "Analizar Documento"])

# Inicio de la app
def main():
    load_styles()
    option = configure_sidebar()

    if option == "Inicio":
        st.title("Procesador de Documentos con IA")
        st.write("Cargue documentos, resalte texto y utilice IA para análisis avanzado.")
    elif option == "Carga de Documento":
        st.title("Carga de Documento")
        uploaded_file = st.file_uploader("Cargue un documento .docx", type="docx")
        if uploaded_file:
            try:
                document_text = load_word_file(uploaded_file)
                text_editor(document_text)
            except Exception as e:
                st.error(f"Error al procesar el documento: {e}")
    elif option == "Analizar Documento":
        st.title("Análisis de Documento con IA")
        st.write("Seleccione texto en el editor para analizar.")

if __name__ == "__main__":
    main()