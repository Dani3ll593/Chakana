import openai
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import docx


# Cargar configuraciones del entorno
def analyze_text_with_api(text):
    system_prompt = "Eres un asistente experto en análisis textual. Analiza el texto a nivel de coherencia interna y externa."
    user_prompt = f"Texto para analizar:\n{text}"
    
    try:
        response = openai.ChatCompletion.acreate(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        return response["choices"][0]["message"]["content"]
    except openai.OpenAIError as e:
        return f"Error al procesar la solicitud: {e}"



# Función para leer archivos .docx
def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

# Función para leer archivos PDF
def read_pdf(file):
    pdf_reader = PdfReader(file)
    return "\n".join([page.extract_text() for page in pdf_reader.pages])

# Función para cargar y procesar archivos
def process_uploaded_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1]

    if file_type == "docx":
        return read_docx(uploaded_file)
    elif file_type == "pdf":
        return read_pdf(uploaded_file)
    elif file_type == "xlsx":
        return pd.read_excel(uploaded_file)
    elif file_type == "csv":
        return pd.read_csv(uploaded_file)
    else:
        return "Formato no soportado. Por favor sube un archivo .docx, .pdf, .xlsx o .csv."



# Configuración de la aplicación en Streamlit
st.title("Análisis de Documentos con Llama")

# Subida de archivos
uploaded_file = st.file_uploader("Sube un archivo para análisis (.docx, .pdf, .xlsx, .csv)", type=["docx", "pdf", "xlsx", "csv"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]

    # Procesar el archivo subido
    if file_type in ["docx", "pdf"]:
        text_content = process_uploaded_file(uploaded_file)
        st.write("Texto extraído:")
        st.text_area("Vista previa", text_content, height=300)

        # Enviar texto a la API
        if st.button("Analizar con Llama"):
            result = analyze_text_with_api(text_content)
            st.write("Resultado del Análisis:")
            st.text_area("Análisis", result, height=300)
    elif file_type in ["xlsx", "csv"]:
        data_content = process_uploaded_file(uploaded_file)
        st.write("Vista previa de los datos:")
        st.dataframe(data_content)
    else:
        st.error("Formato no soportado.")