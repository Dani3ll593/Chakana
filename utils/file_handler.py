from docx import Document
import io

# Leer y extraer texto de un archivo Word
def load_word_file(uploaded_file):
    try:
        doc = Document(io.BytesIO(uploaded_file.read()))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error al cargar el documento: {e}")

# Guardar texto actualizado en un archivo Word
def save_word_file(text, file_path):
    try:
        doc = Document()
        for line in text.split("\n"):
            doc.add_paragraph(line)
        doc.save(file_path)
    except Exception as e:
        raise ValueError(f"Error al guardar el documento: {e}")