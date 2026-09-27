import io
import re
from pypdf import PdfReader
import docx

def extract_text(file) -> str:
    """Extracts raw text from uploaded PDF or DOCX files."""
    text = ""
    file_name = getattr(file, "name", "").lower()

    try:
        if file_name.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif file_name.endswith(".docx"):
            doc = docx.Document(file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        else:
            content = file.read()
            if isinstance(content, bytes):
                text = content.decode("utf-8", errors="ignore")
            else:
                text = str(content)
    except Exception as e:
        print(f"Error extracting text: {e}")

    return text.strip()


def extract_skills(text: str) -> list:
    """Extracts technical and professional skills from text."""
    if not text:
        return []

    SKILL_DATABASE = [
        "python", "java", "c++", "c#", "javascript", "typescript", "html", "css",
        "react", "angular", "vue", "django", "flask", "fastapi", "spring boot",
        "sql", "mysql", "postgresql", "mongodb", "oracle", "nosql",
        "aws", "azure", "gcp", "docker", "kubernetes", "git", "ci/cd", "linux",
        "machine learning", "deep learning", "nlp", "llm", "genai", "rag", "pandas",
        "numpy", "scikit-learn", "tensorflow", "pytorch", "rest api", "api",
        "content moderation", "data analysis", "agile", "scrum", "communication"
    ]

    lower_text = text.lower()
    found_skills = []

    for skill in SKILL_DATABASE:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, lower_text):
            found_skills.append(skill)

    return list(dict.fromkeys(found_skills))