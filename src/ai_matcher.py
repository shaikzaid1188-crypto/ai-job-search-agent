import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured in the .env file.")

client = genai.Client(api_key=API_KEY)


def extract_skills_from_resume(resume_text: str) -> list[str]:
    """Extract skills using Gemini with a local fallback."""

    if not resume_text.strip():
        return []

    prompt = f"""
You are a resume skill extraction assistant.

Extract the important skills from the following resume.

Include:
- Programming languages
- Frameworks and libraries
- Databases
- Cloud and developer tools
- AI/ML skills
- Other relevant technical skills
- Important professional skills

Return ONLY a comma-separated list of skills.
Do not add explanations.

Resume:
{resume_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        skills_text = response.text.strip()

        skills = [
            skill.strip()
            for skill in skills_text.split(",")
            if skill.strip()
        ]

        return skills

    except Exception as e:
        print(f"Gemini skill extraction failed: {e}")

        # Local fallback when Gemini quota is unavailable
        known_skills = [
            "python",
            "java",
            "javascript",
            "typescript",
            "c",
            "c++",
            "c#",
            "sql",
            "html",
            "css",
            "react",
            "node",
            "node.js",
            "fastapi",
            "django",
            "flask",
            "spring",
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "ai",
            "nlp",
            "rag",
            "langchain",
            "gemini",
            "git",
            "github",
            "docker",
            "aws",
            "azure",
            "mongodb",
            "mysql",
            "postgresql",
            "power bi",
            "streamlit",
        ]

        resume_lower = resume_text.lower()

        fallback_skills = []

        for skill in known_skills:
            if skill in resume_lower:
                fallback_skills.append(skill.title())

        return fallback_skills


def calculate_job_match(
    resume_skills: list[str],
    job: dict
) -> dict:
    """
    Calculate job match using local skill matching.

    This avoids consuming Gemini API quota.
    """

    if not resume_skills:
        return {
            "score": 0,
            "reason": "No resume skills were detected."
        }

    job_tags = job.get("tags", [])

    candidate_skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    required_skills = {
        skill.lower().strip()
        for skill in job_tags
    }

    matched = candidate_skills.intersection(required_skills)
    missing = required_skills - candidate_skills

    if required_skills:
        score = round(
            (len(matched) / len(required_skills)) * 100
        )
    else:
        score = 0

    if matched:
        matched_text = ", ".join(
            sorted(skill.title() for skill in matched)
        )
    else:
        matched_text = "none"

    if missing:
        missing_text = ", ".join(
            sorted(skill.title() for skill in missing)
        )
    else:
        missing_text = "none"

    reason = (
        f"Matched skills: {matched_text}. "
        f"Missing job skills: {missing_text}."
    )

    return {
        "score": score,
        "reason": reason
    }


def analyze_skill_gap(
    resume_skills: list[str],
    job: dict
) -> dict:
    """
    Analyze missing skills locally without using Gemini.
    """

    if not resume_skills:
        return {
            "missing_skills": [],
            "recommendation": "Upload a resume with relevant skills."
        }

    job_tags = job.get("tags", [])

    candidate_skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    missing = []

    for skill in job_tags:
        if skill.lower().strip() not in candidate_skills:
            missing.append(skill)

    if missing:
        missing_text = ", ".join(missing)

        recommendation = (
            f"Focus on learning {missing_text}. "
            "Build a practical project using these technologies "
            "to gain hands-on experience."
        )
    else:
        recommendation = (
            "Your current skills cover the main requirements "
            "listed for this job."
        )

    return {
        "missing_skills": missing,
        "recommendation": recommendation
    }