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

def extract_text(file_path):
    try:
        file_extension = get_file_extension(file_path)
        if file_extension == ".pdf":
            return extract_text_from_pdf(file_path)
        elif file_extension == ".docx":
            return extract_text_from_docx(file_path)
        elif file_extension == ".txt":
            return extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Tipo de archivo no soportado: {file_extension}")
    except Exception as e:
        raise ValueError(f"Error al extraer texto: {e}")

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return " ".join(text).strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del PDF: {e}")

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return " ".join([p.text for p in doc.paragraphs if p.text.strip()]).strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del archivo DOCX: {e}")

def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except UnicodeDecodeError:
        raise ValueError("Error al decodificar el archivo TXT. Verifica que esté en formato UTF-8.")
    except Exception as e:
        raise ValueError(f"Error al extraer texto del archivo TXT: {e}")

def is_supported_file(file_path):
    try:
        file_extension = get_file_extension(file_path)
        return file_extension in SUPPORTED_FILE_TYPES.keys()
    except Exception as e:
        raise ValueError(f"Error al verificar el tipo de archivo: {e}")

def get_file_extension(file_name):
    _, ext = os.path.splitext(file_name)
    return ext.lower()