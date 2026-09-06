import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def generate_cover_letter(resume_text: str, job_title: str, company: str, job_desc: str) -> str:
    """Generates a tailored cover letter using an LLM based on resume and job specs."""
    if not api_key:
        return "⚠️ Gemini API Key not found. Please configure your .env file."

    prompt = f"""
    You are an expert career consultant. Write a professional, tailored 3-paragraph cover letter for a candidate.
    
    Candidate Resume Details:
    {resume_text[:2000]}
    
    Target Role: {job_title} at {company}
    Job Description: {job_desc}
    
    Keep the tone confident, polished, and directly highlight the candidate's matching experience.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"

def generate_resume_tips(resume_text: str, job_desc: str, missing_skills: list) -> str:
    """Provides actionable feedback on how to tailor the resume for the selected role."""
    if not api_key:
        return "⚠️ Gemini API Key not found. Please configure your .env file."

    prompt = f"""
    Act as a technical recruiter. The candidate is targeting this position:
    Job Description: {job_desc}
    Missing Skills Identified: {', '.join(missing_skills) if missing_skills else 'None'}
    
    Candidate Resume Extract:
    {resume_text[:2000]}
    
    Provide 3 to 4 concise, high-impact bullet points advising how the candidate can update their resume bullets or projects to better match this job opening.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating resume suggestions: {str(e)}"