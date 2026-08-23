import pdfplumber

def extract_text_from_pdf(uploaded_file) -> str:
    """Extracts text from an uploaded PDF file."""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"
    return text.strip()