import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv(override=True)


def get_gemini_api_key() -> str:
    """Dynamically fetches the Gemini key from Streamlit secrets or env vars."""
    key = ""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if not key:
        key = os.getenv("GEMINI_API_KEY", "")
    return key.strip() if key else ""


def generate_cover_letter(*args, **kwargs) -> str:
    """Flexible wrapper for generating cover letters.

    Supports both:
      - generate_cover_letter(resume_text, job_description)
      - generate_cover_letter(resume_text, job_title, company, job_description)
    """
    resume_text = ""
    job_title = "Candidate"
    company = "the Hiring Team"
    job_description = ""

    # Parse arguments based on how app.py calls it
    if len(args) == 2:
        resume_text, job_description = args[0], args[1]
    elif len(args) >= 4:
        resume_text, job_title, company, job_description = args[0], args[1], args[2], args[3]
    else:
        resume_text = kwargs.get("resume_text", "")
        job_description = kwargs.get("job_description", "")
        job_title = kwargs.get("job_title", "Candidate")
        company = kwargs.get("company", "the Hiring Team")

    # Extract detected skills from resume for realistic personalization
    skills_corpus = [
        "python", "javascript", "react", "django", "sql", "aws", "git", "html",
        "css", "docker", "rest api", "postgresql", "mysql", "java", "node.js"
    ]
    detected_skills = [
        s.title() for s in skills_corpus if re.search(rf"\b{re.escape(s)}\b", resume_text, re.IGNORECASE)
    ]
    primary_skills = ", ".join(detected_skills[:4]) if detected_skills else "Python, full-stack development, and software engineering"

    fallback_letter = (
        f"Dear Hiring Manager,\n\n"
        f"I am writing to express my strong enthusiasm for this position. "
        f"With hands-on background and proficiency in {primary_skills}, I am well-prepared to contribute "
        f"effectively to your engineering projects and help drive your technical objectives.\n\n"
        f"Reviewing the requirements for this role, I was excited to see the focus on quality execution, "
        f"clean architecture, and scalable design. My practical experience analyzing problem requirements, "
        f"collaborating across teams, and building maintainable software directly aligns with the challenges "
        f"faced by your group.\n\n"
        f"I would welcome the opportunity to discuss further how my skills and proactive problem-solving mindset "
        f"can add value to your team. Thank you for your time and consideration.\n\n"
        f"Sincerely,\nCandidate"
    )

    api_key = get_gemini_api_key()
    if not api_key:
        return fallback_letter

    prompt = (
        f"Write a polished 3-paragraph cover letter for a candidate applying to this job.\n\n"
        f"Job Details / Description:\n{job_description[:700]}\n\n"
        f"Candidate Resume Details:\n{resume_text[:1200]}\n\n"
        f"Requirements:\n"
        f"- Address directly to 'Dear Hiring Manager,'\n"
        f"- Sign off with 'Sincerely,\nCandidate'\n"
        f"- Do NOT use bracketed placeholders like [Your Name] or [Date].\n"
        f"- Integrate the candidate's verified skills naturally."
    )

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    model_endpoints = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro"
    ]

    for model_name in model_endpoints:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            response = requests.post(url, headers=headers, json=payload, timeout=8)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and parts[0].get("text"):
                        return parts[0]["text"].strip()
        except Exception:
            continue

    return fallback_letter