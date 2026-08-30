def fetch_jobs(tag: str = "python", limit: int = 10) -> list:
    """Returns curated job postings with structured skill requirements."""
    custom_jobs = [
        {
            "id": 1,
            "title": "Junior Python Developer",
            "company": "Google",
            "location": "Bengaluru, India / Remote",
            "url": "https://careers.google.com",
            "tags": ["python", "django", "fastapi", "sql", "git", "docker"],
            "description": "Develop and maintain robust backend microservices, REST APIs, and automated data pipelines using Python and Docker."
        },
        {
            "id": 2,
            "title": "AI & ML Engineer Intern",
            "company": "Microsoft",
            "location": "Hyderabad, India / Remote",
            "url": "https://careers.microsoft.com",
            "tags": ["python", "machine learning", "nlp", "pytorch", "pandas", "llm"],
            "description": "Collaborate on LLM fine-tuning, prompt engineering frameworks, and natural language matching algorithms with PyTorch and NLP."
        },
        {
            "id": 3,
            "title": "Full Stack Software Engineer",
            "company": "Amazon",
            "location": "Remote",
            "url": "https://amazon.jobs",
            "tags": ["react", "node.js", "python", "aws", "typescript", "sql"],
            "description": "Design customer-facing web applications using React, modern Node microservices, and scalable AWS cloud infrastructure."
        },
        {
            "id": 4,
            "title": "Data Analyst Trainee",
            "company": "Deloitte",
            "location": "Mumbai, India",
            "url": "https://deloitte.com/careers",
            "tags": ["python", "sql", "power bi", "pandas", "tableau", "data analysis"],
            "description": "Perform exploratory data analysis, build business intelligence dashboards using Power BI and Tableau, and optimize SQL queries."
        },
        {
            "id": 5,
            "title": "Cloud & DevOps Associate",
            "company": "TCS",
            "location": "Chennai, India",
            "url": "https://tcs.com/careers",
            "tags": ["aws", "azure", "docker", "kubernetes", "linux", "ci/cd"],
            "description": "Manage cloud deployments, implement CI/CD pipelines, containerize backend microservices, and ensure cluster scalability."
        }
    ]

    tag_lower = tag.lower().strip()
    filtered = []
    
    for job in custom_jobs:
        tags = [t.lower() for t in job["tags"]]
        title = job["title"].lower()
        company = job["company"].lower()
        
        if not tag_lower or tag_lower in tags or tag_lower in title or tag_lower in company:
            filtered.append(job)
            
    results = filtered if filtered else custom_jobs
    return results[:limit]