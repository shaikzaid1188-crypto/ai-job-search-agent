def fetch_jobs(tag: str = "python", limit: int = 10) -> list:
    """
    Returns custom, curated job postings tailored to your preferred companies and roles.
    """
    custom_jobs = [
        {
            "title": "Junior Python Developer",
            "company": "Google",
            "location": "Bengaluru, India / Remote",
            "url": "https://careers.google.com",
            "tags": ["python", "django", "fastapi", "sql"],
            "description": "Looking for an entry-level Python developer to build backend APIs and integrate automated workflows."
        },
        {
            "title": "AI & ML Intern",
            "company": "Microsoft",
            "location": "Hyderabad, India / Remote",
            "url": "https://careers.microsoft.com",
            "tags": ["python", "ai", "machine learning", "nlp"],
            "description": "Join our AI research team to build NLP matching algorithms and integrate large language model agents."
        },
        {
            "title": "Full Stack Developer",
            "company": "Amazon",
            "location": "Remote",
            "url": "https://amazon.jobs",
            "tags": ["react", "node", "python", "aws"],
            "description": "Develop high-scale web platforms and microservices using modern frontend frameworks and Python services."
        },
        {
            "title": "Data Analyst Trainee",
            "company": "Deloitte",
            "location": "Mumbai, India",
            "url": "https://deloitte.com/careers",
            "tags": ["python", "sql", "power bi", "data"],
            "description": "Analyze large business datasets, build interactive dashboards, and optimize ETL data pipelines."
        },
        {
            "title": "Software Engineer (Backend)",
            "company": "TCS",
            "location": "Chennai, India",
            "url": "https://tcs.com/careers",
            "tags": ["java", "python", "sql", "api"],
            "description": "Responsible for developing robust enterprise backend systems, database schemas, and REST APIs."
        }
    ]

    # Filter based on search input
    tag_lower = tag.lower().strip()
    filtered = []
    
    for job in custom_jobs:
        tags = [t.lower() for t in job["tags"]]
        title = job["title"].lower()
        company = job["company"].lower()
        
        # Match if search keyword is in tags, title, or company name
        if tag_lower in tags or tag_lower in title or tag_lower in company:
            filtered.append(job)
            
    # If no specific keyword matched, return all jobs up to limit
    results = filtered if filtered else custom_jobs
    return results[:limit]