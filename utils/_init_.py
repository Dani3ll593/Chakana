import os
from PyPDF2 import PdfReader
from docx import Document

SUPPORTED_FILE_TYPES = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain"
}

def load_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"Archivo no encontrado: {file_path}")
    except Exception as e:
        raise ValueError(f"Error al cargar el archivo: {e}")

def save_file(content, file_name):
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        return file_name
    except Exception as e:
        raise ValueError(f"Error al guardar el archivo: {e}")

def extract_text(file):
    try:
        file_type = getattr(file, "type", None)
        if not file_type:
            raise ValueError("El archivo cargado no tiene un tipo definido.")

        if file_type == SUPPORTED_FILE_TYPES["pdf"]:
            return extract_text_from_pdf(file)
        elif file_type == SUPPORTED_FILE_TYPES["docx"]:
            return extract_text_from_docx(file)
        elif file_type == SUPPORTED_FILE_TYPES["txt"]:
            return extract_text_from_txt(file)
        else:
            raise ValueError(f"Tipo de archivo no soportado: {file_type}")
    except Exception as e:
        raise ValueError(f"Error al extraer texto: {e}")

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return " ".join(text).strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del PDF: {e}")

def extract_text_from_docx(file):
    try:
        doc = Document(file)
        return " ".join([p.text for p in doc.paragraphs if p.text.strip()]).strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del archivo DOCX: {e}")

def extract_text_from_txt(file):
    try:
        return file.getvalue().decode("utf-8").strip()
    except UnicodeDecodeError:
        raise ValueError("Error al decodificar el archivo TXT. Verifica que esté en formato UTF-8.")
    except Exception as e:
        raise ValueError(f"Error al extraer texto del archivo TXT: {e}")

def is_supported_file(file):
    try:
        return getattr(file, "type", None) in SUPPORTED_FILE_TYPES.values()
    except AttributeError:
        return False

def get_file_extension(file_name):
    _, ext = os.path.splitext(file_name)
    return ext.lower()