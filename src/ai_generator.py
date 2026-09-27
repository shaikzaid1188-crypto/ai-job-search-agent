import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = None
try:
    import streamlit as st
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not GEMINI_KEY:
    GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)


def generate_cover_letter(resume_text: str, job_description: str) -> str:
    """Generates a tailored cover letter using Gemini."""
    if not resume_text:
        return "Please upload a resume first to generate a customized cover letter."

    prompt = f"""
    You are an expert career consultant. Draft a compelling, professional cover letter tailored specifically to the job description below using the candidate's resume information. Keep it concise, engaging, and ready to send.

    Candidate Resume:
    {resume_text[:2000]}

    Job Description:
    {job_description[:2000]}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return (
            "Dear Hiring Manager,\n\n"
            "I am writing to express my strong interest in this position. "
            "With my relevant background and technical experience, I believe I can make an immediate positive contribution to your team.\n\n"
            f"(Note: {e})"
        )   