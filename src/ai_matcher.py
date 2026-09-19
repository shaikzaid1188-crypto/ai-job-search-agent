def calculate_match(resume_skills: list, job_tags: list) -> tuple:
    """
    Computes matching percentage and skill gaps between candidate and job requirements.
    Returns: (match_percentage, matching_skills, missing_skills)
    """
    if not job_tags:
        return 0, [], []

    resume_set = set(s.lower() for s in resume_skills)
    job_set = set(t.lower() for t in job_tags)

    matching_skills = list(resume_set.intersection(job_set))
    missing_skills = list(job_set.difference(resume_set))

    score = int((len(matching_skills) / len(job_set)) * 100)
    return score, sorted(matching_skills), sorted(missing_skills)