import os
import docx
import pdfplumber

def extract_text(file):
    """
    Extracts text from .docx, .pdf, or .txt files.
    """
    ext = os.path.splitext(file.name)[1].lower()
    if ext == ".docx":
        return _extract_docx(file)
    elif ext == ".pdf":
        return _extract_pdf(file)
    elif ext == ".txt":
        return _extract_txt(file)
    else:
        raise ValueError("Unsupported file format.")

def _extract_docx(file):
    doc = docx.Document(file)
    text = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(text), {f"Paragraph {i+1}": para for i, para in enumerate(text)}

def _extract_pdf(file):
    with pdfplumber.open(file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
        return "\n".join(pages), {f"Page {i+1}": page for i, page in enumerate(pages)}

def _extract_txt(file):
    text = file.read().decode("utf-8")
    paragraphs = text.split("\n\n")
    return text, {f"Paragraph {i+1}": para for i, para in enumerate(paragraphs)}