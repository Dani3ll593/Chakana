from PyPDF2 import PdfReader
from docx import Document

def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    elif file.type == "text/plain":
        return file.getvalue().decode("utf-8")
    else:
        raise ValueError(f"Tipo de archivo no soportado: {file.type}")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_docx(file):
    doc = Document(file)
    return " ".join([p.text for p in doc.paragraphs])