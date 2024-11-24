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
        content = file.read().decode("utf-8")
        structure = _generate_simple_structure(content)
        return content, structure
    else:
        raise ValueError("Formato no soportado")


def _load_docx(file):
    doc = docx.Document(file)
    content = []
    structure = {}
    current_hierarchy = []

    for i, paragraph in enumerate(doc.paragraphs):
        text = paragraph.text.strip()
        if not text:  # Ignorar líneas vacías
            continue

        content.append(text)

        if paragraph.style.name.startswith("Heading"):
            level = int(paragraph.style.name[-1])
            _update_structure(structure, current_hierarchy, level, text)
    return "\n".join(content), structure


def _load_pdf(file):
    with pdfplumber.open(file) as pdf:
        content = []
        structure = {}
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            content.append(page_text)
            structure[f"Page_{i + 1}"] = f"Página {i + 1}"
        return "\n".join(content), structure


def process_document(content, structure):
    """
    Procesa el contenido basado en la estructura.
    Cada bloque es una sección del documento según el índice generado.
    """
    sections = []
    if not structure:
        return content.split("\n\n")  # Dividir por párrafos si no hay estructura

    for key, section_title in structure.items():
        sections.append(f"{section_title}\n\n")
    return sections


def _generate_simple_structure(content):
    """
    Genera una estructura simple de bloques numerados si no hay encabezados.
    """
    blocks = content.split("\n\n")
    return {f"Block_{i + 1}": f"Bloque {i + 1}" for i in range(len(blocks))}


def _update_structure(structure, current_hierarchy, level, text):
    """
    Actualiza la estructura jerárquica del documento basado en el nivel del encabezado.
    """
    # Si es un encabezado de nivel menor, eliminar los niveles más profundos
    while len(current_hierarchy) >= level:
        current_hierarchy.pop()

    # Añadir el encabezado actual a la jerarquía
    current_hierarchy.append(text)

    # Generar la clave jerárquica
    key = " > ".join(current_hierarchy)
    structure[key] = text