from PyPDF2 import PdfReader
from docx import Document

def extract_text(file_path):
    """
    Extrae texto de un archivo cargado. Soporta archivos PDF, DOCX y TXT.
    """
    try:
        # Determinar el tipo de archivo
        if file_path.endswith(".pdf"):
            return extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            return extract_text_from_docx(file_path)
        elif file_path.endswith(".txt"):
            return extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Tipo de archivo no soportado: {file_path}")
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo: {e}")

def extract_text_from_pdf(file_path):
    """
    Extrae texto de un archivo PDF utilizando PyPDF2.
    """
    try:
        reader = PdfReader(file_path)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Asegurarse de que la página contiene texto
                text.append(page_text)
        return " ".join(text).strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del PDF: {e}")

def extract_text_from_docx(file_path):
    """
    Extrae texto de un archivo DOCX utilizando python-docx.
    """
    try:
        doc = Document(file_path)
        text = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
        return " ".join(text).strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del archivo DOCX: {e}")

def extract_text_from_txt(file_path):
    """
    Extrae texto de un archivo TXT.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except UnicodeDecodeError:
        raise ValueError("Error al decodificar el archivo TXT. Asegúrate de que esté en formato UTF-8.")
    except Exception as e:
        raise ValueError(f"Error al extraer texto del archivo TXT: {e}")