import docx
import pdfplumber
from typing import Tuple

def process_uploaded_file(uploaded_file) -> Tuple[str, dict]:
    """Procesa el archivo subido y lo divide en secciones."""
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type == "docx":
        return process_docx(uploaded_file)
    elif file_type == "pdf":
        return process_pdf(uploaded_file)
    elif file_type == "txt":
        content = uploaded_file.read().decode("utf-8")
        return content, {"Texto Completo": content}
    else:
        raise ValueError("Formato no soportado. Use .docx, .pdf, o .txt.")

def process_docx(file):
    doc = docx.Document(file)
    content = []
    sections = {}
    current_section = "Inicio"

    for para in doc.paragraphs:
        if para.style.name.startswith("Heading"):
            current_section = para.text
            sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(para.text)

    # Unir el contenido en texto y organizar secciones
    for key in sections:
        sections[key] = "\n".join(sections[key])
    return "\n".join(content), sections

def process_pdf(file):
    with pdfplumber.open(file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
        content = "\n".join(pages)
        sections = {f"Página {i+1}": page for i, page in enumerate(pages)}
        return content, sections