import pdfplumber

def extract_text_from_pdf(filepath):
    try:
        with pdfplumber.open(filepath) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return ""
