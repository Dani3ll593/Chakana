from PyPDF2 import PdfReader
from docx import Document

def extract_text(file):
    """
    Extrae texto de un archivo cargado. Soporta archivos PDF, DOCX y TXT.
    """
    try:
        # Determinar el tipo de archivo
        if hasattr(file, "type"):  # Streamlit File Uploader
            if file.type == "application/pdf":
                return extract_text_from_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return extract_text_from_docx(file)
            elif file.type == "text/plain":
                return extract_text_from_txt(file)
            else:
                raise ValueError(f"Tipo de archivo no soportado: {file.type}")
        else:
            raise ValueError("El archivo cargado no tiene un tipo válido.")
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo: {e}")

def extract_text_from_pdf(file):
    """
    Extrae texto de un archivo PDF utilizando PyPDF2.
    """
    try:
        reader = PdfReader(file)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Asegurarse de que la página contiene texto
                text.append(page_text)
        return " ".join(text).strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del PDF: {e}")

def extract_text_from_docx(file):
    """
    Extrae texto de un archivo DOCX utilizando python-docx.
    """
    try:
        doc = Document(file)
        text = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
        return " ".join(text).strip()
    except Exception as e:
        raise ValueError(f"Error al extraer texto del archivo DOCX: {e}")

def extract_text_from_txt(file):
    """
    Extrae texto de un archivo TXT.
    """
    try:
        return file.getvalue().decode("utf-8").strip()
    except UnicodeDecodeError:
        raise ValueError("Error al decodificar el archivo TXT. Asegúrate de que esté en formato UTF-8.")
    except Exception as e:
        raise ValueError(f"Error al extraer texto del archivo TXT: {e}")