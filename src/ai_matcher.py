import re

# Comprehensive list of industry-standard tech and domain skills
TECH_SKILLS_DATABASE = [
    # Languages
    "python", "java", "c++", "c#", "c", "javascript", "typescript", "ruby", "php", "go", "rust", "scala", "kotlin", "swift",
    # Web & Frameworks
    "react", "angular", "vue", "next.js", "django", "fastapi", "flask", "spring boot", "express", "node.js", "html", "css", "tailwind",
    # Databases & Big Data
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite", "oracle", "snowflake", "spark", "hadoop",
    # AI / ML / Data Science
    "machine learning", "deep learning", "nlp", "computer vision", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", 
    "power bi", "tableau", "data analysis", "data visualization", "data science", "llm", "genai",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "git", "github", "linux", "terraform", "rest api", "graphql", "microservices"
]

def extract_skills_from_resume(resume_text: str) -> list:
    """Extracts known tech skills found in the parsed resume text using regex boundaries."""
    if not resume_text:
        return []
        
    text_lower = resume_text.lower()
    detected_skills = []
    
    for skill in TECH_SKILLS_DATABASE:
        # Match standalone words or terms cleanly
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        if re.search(pattern, text_lower):
            detected_skills.append(skill.title())
            
    return sorted(list(set(detected_skills)))

def calculate_job_match(resume_skills: list, job_tags: list, job_description: str) -> int:
    """Calculates a realistic match percentage based on skills overlap and role keywords."""
    if not resume_skills:
        return 0
    
    resume_skills_lower = set([s.lower() for s in resume_skills])
    job_tags_lower = set([t.lower() for t in job_tags])
    
    # Check overlap with tags
    tag_overlap = resume_skills_lower.intersection(job_tags_lower)
    
    # Check description mentions
    desc_lower = job_description.lower()
    desc_matches = sum(1 for skill in resume_skills_lower if skill in desc_lower)
    
    if not job_tags:
        score = min(int((desc_matches / max(len(resume_skills_lower), 1)) * 100) + 30, 95)
        return score

    tag_score = (len(tag_overlap) / len(job_tags_lower)) * 70
    desc_score = min((desc_matches / max(len(job_tags_lower), 1)) * 30, 30)
    
    final_score = int(tag_score + desc_score)
    # Clamp score realistically between 15% and 98%
    return min(max(final_score, 15), 98)

def analyze_skill_gap(resume_skills: list, job_tags: list) -> dict:
    """Categorizes skills into matching and missing recommendations."""
    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([t.lower() for t in job_tags])
    
    matching = [t.title() for t in job_set if t in resume_set]
    missing = [t.title() for t in job_set if t not in resume_set]
    
    return {
        "matching": matching,
        "missing": missing
    }