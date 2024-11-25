import os
from PyPDF2 import PdfReader
from docx import Document

def load_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def save_file(content, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)
    return file_name

def extract_text(file):
    if file.type == "application/pdf":
        pdf = PdfReader(file)
        text = " ".join([page.extract_text() for page in pdf.pages])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        text = " ".join([paragraph.text for paragraph in doc.paragraphs])
    else:  # Texto plano
        text = file.getvalue().decode("utf-8")
    return text