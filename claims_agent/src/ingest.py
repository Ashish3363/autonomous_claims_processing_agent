import os
import pdfplumber

def read_file(file_path: str) -> str:
    """
    Reads the content of a file (TXT or PDF) and returns it as a string.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.pdf':
        return _extract_text_from_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def _extract_text_from_pdf(path: str) -> str:
    text_content = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content.append(extracted)
        return "\n".join(text_content)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
