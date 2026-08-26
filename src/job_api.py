def fetch_jobs(tag: str = "python", limit: int = 10) -> list:
    """
    Returns curated job postings and supports both
    simple keywords and natural-language search queries.
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

    query = tag.lower().strip()

    # Words that don't help identify a job
    stop_words = {
        "find",
        "me",
        "jobs",
        "job",
        "for",
        "a",
        "an",
        "the",
        "in",
        "at",
        "with",
        "and",
        "or",
        "to",
        "of",
        "beginner",
        "entry",
        "level",
        "developer",
        "developers",
        "please"
    }

    # Extract useful words from the query
    keywords = [
        word.strip(".,!?")
        for word in query.split()
        if word.strip(".,!?") not in stop_words
    ]

    filtered = []

    for job in custom_jobs:

        tags = [t.lower() for t in job["tags"]]
        title = job["title"].lower()
        company = job["company"].lower()
        description = job["description"].lower()

        # Check whether any keyword matches the job
        matched = any(
            keyword in tags
            or keyword in title
            or keyword in company
            or keyword in description
            for keyword in keywords
        )

        if matched:
            filtered.append(job)

    return filtered[:limit]