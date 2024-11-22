import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import docx
from dotenv import load_dotenv
import os
import openai
from docx import Document
import matplotlib.pyplot as plt
import plotly.express as px

# Configurar la clave de API y la base URL
load_dotenv()
openai.api_key = os.getenv("AIML_API_KEY")
openai.api_base = os.getenv("AIML_BASE_URL")

# Función para analizar texto con la API
def analyze_text(text):
    system_prompt = "Eres un asistente que analiza texto en términos de coherencia y estructura."
    user_prompt = f"Por favor analiza el siguiente texto:\n{text}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usa el modelo correcto disponible
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al procesar la solicitud: {e}"

# Función para generar un reporte en Word
def generate_report(text, analysis):
    doc = Document()
    doc.add_heading("Reporte de Análisis", level=1)
    doc.add_heading("Texto Original", level=2)
    doc.add_paragraph(text)
    doc.add_heading("Resultados del Análisis", level=2)
    doc.add_paragraph(analysis)
    doc.save("reporte.docx")
    return "reporte.docx"

# Título de la aplicación
st.title("Chakana: Asesor de Tesis")

# Carga de documentos
uploaded_file = st.file_uploader("Sube tu archivo (.docx, .pdf, .xlsx, .csv)", type=["docx", "pdf", "xlsx", "csv"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    
    if file_type == "docx":
        doc = docx.Document(uploaded_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        st.write("Contenido del documento:")
        st.text_area("Vista previa", text, height=300)

    elif file_type == "pdf":
        pdf_reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in pdf_reader.pages])
        st.write("Contenido del documento:")
        st.text_area("Vista previa", text, height=300)

    elif file_type == "xlsx":
        df = pd.read_excel(uploaded_file)
        st.write("Vista previa de los datos cargados:")
        st.dataframe(df)

    elif file_type == "csv":
        df = pd.read_csv(uploaded_file)
        st.write("Vista previa de los datos cargados:")
        st.dataframe(df)

    # Análisis con la API
    if file_type in ["docx", "pdf"]:
        analysis = analyze_text(text)
        st.write("Resultados del Análisis:")
        st.text_area("Análisis", analysis, height=300)

        # Generar reporte
        if st.button("Generar Reporte"):
            report_path = generate_report(text, analysis)
            st.success("Reporte generado exitosamente.")
            with open(report_path, "rb") as file:
                st.download_button("Descargar Reporte", file, file_name="reporte.docx")

    # Visualización de datos
    if file_type in ["xlsx", "csv"]:
        st.write("Visualización de Datos:")
        fig, ax = plt.subplots()
        df.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        st.write("Gráfico Interactivo:")
        fig = px.bar(df, x=df.columns[0], y=df.columns[1])
        st.plotly_chart(fig)