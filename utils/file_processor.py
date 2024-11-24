import os
import docx
import pdfplumber


def extract_text(file):
    """
    Extracts text from .docx, .pdf, or .txt files and organizes content into sections based on titles or headings.
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
    """
    Extracts text and organizes sections based on headings (H1, H2, H3) from a .docx file.
    """
    doc = docx.Document(file)
    sections = {}
    current_section = "Untitled Section"
    section_content = []

    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith("Heading"):
            # Save current section before moving to the next
            if section_content:
                sections[current_section] = "\n".join(section_content)
                section_content = []

            # Update the current section name
            current_section = paragraph.text.strip()

        elif paragraph.text.strip():
            # Add paragraph to the current section
            section_content.append(paragraph.text.strip())

    # Add the last section
    if section_content:
        sections[current_section] = "\n".join(section_content)

    # Combine all text for general processing
    all_text = "\n".join([f"{title}\n{content}" for title, content in sections.items()])
    return all_text, sections


def _extract_pdf(file):
    """
    Extracts text and organizes sections based on heuristics (e.g., capitalized lines or spacing) from a .pdf file.
    """
    with pdfplumber.open(file) as pdf:
        sections = {}
        current_section = "Untitled Section"
        section_content = []

        for page in pdf.pages:
            lines = page.extract_text().splitlines()
            for line in lines:
                # Identify potential section titles (all caps, bolded heuristics could be added)
                if line.isupper():
                    if section_content:
                        sections[current_section] = "\n".join(section_content)
                        section_content = []
                    current_section = line.strip()
                elif line.strip():
                    section_content.append(line.strip())

        # Add the last section
        if section_content:
            sections[current_section] = "\n".join(section_content)

    # Combine all text for general processing
    all_text = "\n".join([f"{title}\n{content}" for title, content in sections.items()])
    return all_text, sections


def _extract_txt(file):
    """
    Extracts text and organizes sections based on paragraphs separated by double newlines.
    """
    text = file.read().decode("utf-8")
    paragraphs = text.split("\n\n")
    sections = {f"Paragraph {i+1}": para.strip() for i, para in enumerate(paragraphs) if para.strip()}
    all_text = "\n".join(paragraphs)
    return all_text, sections