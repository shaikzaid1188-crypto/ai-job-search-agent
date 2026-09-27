import re
from src.parser import extract_skills

def calculate_ats_match(candidate_skills: list, job: dict, job_description: str = "") -> tuple:
    """
    Calculates a realistic ATS match percentage by evaluating candidate skills against
    the job tags, title, and full description text.
    """
    if not candidate_skills:
        return 0, [], []

    cand_set = {s.strip().lower() for s in candidate_skills if s}
    job_skills = set()

    if isinstance(job, dict):
        for tag in job.get("tags", []):
            job_skills.add(tag.strip().lower())
        combined_text = f"{job.get('title', '')} {job.get('description', '')}"
        job_skills.update(extract_skills(combined_text))

    if job_description:
        job_skills.update(extract_skills(job_description))

    # Match candidate skills found in the combined description
    combined_desc = (job.get("description", "") if isinstance(job, dict) else "") + " " + job_description
    for skill in cand_set:
        if re.search(r"\b" + re.escape(skill) + r"\b", combined_desc.lower()):
            job_skills.add(skill)

    if not job_skills:
        return 50, list(cand_set)[:2], []

    matching = list(cand_set.intersection(job_skills))
    missing = list(job_skills.difference(cand_set))

    score = int((len(matching) / len(job_skills)) * 100)
    if matching and score < 40:
        score = min(92, 40 + len(matching) * 15)

    return min(100, score), matching, missing