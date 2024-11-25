import os
from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO

SUPPORTED_FILE_TYPES = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain"
}

def load_file(file_path):
    """
    Carga un archivo de texto plano desde el disco.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"Archivo no encontrado: {file_path}")
    except Exception as e:
        raise ValueError(f"Error al cargar el archivo: {e}")

def save_file(content, file_name):
    """
    Guarda contenido en un archivo de texto plano.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        return file_name
    except Exception as e:
        raise ValueError(f"Error al guardar el archivo: {e}")

def extract_text(file):
    """
    Extrae texto de archivos PDF, DOCX o TXT.
    """
    try:
        if file.type == SUPPORTED_FILE_TYPES["pdf"]:
            return extract_text_from_pdf(file)
        elif file.type == SUPPORTED_FILE_TYPES["docx"]:
            return extract_text_from_docx(file)
        elif file.type == SUPPORTED_FILE_TYPES["txt"]:
            return file.getvalue().decode("utf-8")
        else:
            raise ValueError(f"Tipo de archivo no soportado: {file.type}")
    except Exception as e:
        raise ValueError(f"Error al extraer texto: {e}")

def extract_text_from_pdf(file):
    """
    Extrae texto de un archivo PDF.
    """
    try:
        pdf_reader = PdfReader(file)
        text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del PDF: {e}")

def extract_text_from_docx(file):
    """
    Extrae texto de un archivo DOCX.
    """
    try:
        docx_reader = Document(file)
        text = " ".join([paragraph.text for paragraph in docx_reader.paragraphs])
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del archivo DOCX: {e}")

def is_supported_file(file):
    """
    Verifica si el archivo es de un tipo soportado.
    """
    return file.type in SUPPORTED_FILE_TYPES.values()

def get_file_extension(file_name):
    """
    Obtiene la extensión del archivo.
    """
    _, ext = os.path.splitext(file_name)
    return ext.lower()