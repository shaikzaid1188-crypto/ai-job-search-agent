import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_gemini_api_key():
    """Safely retrieves the Gemini API key from local .env or Streamlit secrets."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
        
    return None

def get_model():
    """Configures the API key and returns the active Gemini model."""
    api_key = get_gemini_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Check your .env or secrets configuration.")
    
    genai.configure(api_key=api_key)
    
    models_to_try = [
        "gemini-3.6-flash",
        "models/gemini-3.6-flash",
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-pro"
    ]
    
    for model_name in models_to_try:
        try:
            return genai.GenerativeModel(model_name)
        except Exception:
            continue
            
    return genai.GenerativeModel("gemini-3.6-flash")

def generate_cover_letter(resume_text: str, job_title: str, company: str, job_desc: str) -> str:
    """Generates a professional 3-paragraph cover letter without candidate contact headers or names."""
    try:
        model = get_model()
        prompt = f"""
You are an expert career consultant. Write a professional, concise, and persuasive 3-paragraph cover letter for a candidate applying to the position of {job_title} at {company}.

Candidate Resume Details:
{resume_text[:2000]}

Job Description:
{job_desc[:1500]}

Formatting rules:
- STRICT: Do NOT include any candidate contact header at the top (no names, addresses, emails, or phone numbers).
- Start directly with: "Dear {company} Engineering Team," or "Dear {company} Hiring Team,".
- Paragraph 1: Express strong interest and summarize core technical fit.
- Paragraph 2: Highlight concrete technical achievements that match the requirements in the job description.
- Paragraph 3: Reiterate fit with a confident closing.
- SIGN-OFF: End the letter strictly with:
Sincerely,
[Your Name]
- DO NOT use the candidate's actual name (e.g., Stephen Greet) anywhere in the sign-off or letter.
"""
        response = model.generate_content(prompt)
        text = response.text

        # Programmatic sanitization to catch any leftover occurrences
        text = text.replace("Stephen Greet", "[Your Name]")
        text = text.replace("Stephen", "[Your Name]")
        return text
    except Exception as e:
        return f"Error generating cover letter: {e}"

def generate_resume_tips(resume_text: str, job_desc: str, missing_skills: list) -> str:
    """Generates targeted ATS resume improvement suggestions."""
    try:
        model = get_model()
        missing_str = ", ".join(missing_skills) if missing_skills else "None explicitly detected"
        prompt = f"""
Act as an ATS resume reviewer and technical recruiter. Compare the candidate resume against the target role requirements.

Candidate Resume Excerpt:
{resume_text[:2000]}

Target Job Requirements:
{job_desc[:1500]}

Identified Missing Keyword Skills:
{missing_str}

Provide 3 concise, bulleted, actionable recommendations on how the candidate can strengthen their resume for this specific role.
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating resume tips: {e}"