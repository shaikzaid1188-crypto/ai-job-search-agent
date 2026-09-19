import io
import re
from pypdf import PdfReader

COMMON_SKILLS = [
    "python", "java", "c++", "c#", "javascript", "typescript", "golang",
    "react", "angular", "vue", "node", "django", "flask", "fastapi",
    "sql", "postgresql", "mysql", "mongodb", "redis",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "ci/cd",
    "rest", "graphql", "grpc", "html", "css", "tailwind"
]

def extract_text_from_pdf(uploaded_file) -> str:
    """Extracts raw text from an uploaded PDF resume."""
    try:
        reader = PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_skills(text: str) -> list:
    """Identifies technical skills present within the resume text."""
    if not text:
        return []
    lower_text = text.lower()
    found_skills = []
    for skill in COMMON_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, lower_text):
            found_skills.append(skill)
    return sorted(list(set(found_skills)))