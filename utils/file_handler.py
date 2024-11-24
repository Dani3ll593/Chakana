from docx import Document

# Leer y extraer texto de un archivo Word
def load_word_file(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()

# Guardar texto actualizado en un archivo Word
def save_word_file(text, file_path):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(file_path)