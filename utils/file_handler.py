import os
import docx
import pdfplumber

def load_document(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext == ".docx":
        return _load_docx(file)
    elif ext == ".pdf":
        return _load_pdf(file)
    elif ext == ".txt":
        return file.read().decode("utf-8")
    else:
        raise ValueError("Formato de archivo no soportado")

def _load_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def _load_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages])

def process_document(content):
    return content.split("\n\n")  # Dividir en bloques por párrafos