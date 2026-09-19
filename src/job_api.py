import requests

INDIA_COMPANIES_DATABASE = [
    {
        "id": "ind-1",
        "title": "Python Backend Engineer",
        "company_name": "Razorpay",
        "candidate_required_location": "Bengaluru, Karnataka, India",
        "url": "https://razorpay.com/jobs",
        "tags": ["python", "django", "fastapi", "sql", "redis", "docker"],
        "description": "Build high-throughput, fault-tolerant payment gateway microservices. Collaborate with platform engineers to design scalable REST and gRPC APIs using Python, PostgreSQL, and AWS."
    },
    {
        "id": "ind-2",
        "title": "Software Development Engineer (Python / SDE-1)",
        "company_name": "Swiggy",
        "candidate_required_location": "Bengaluru, Karnataka / Remote (India)",
        "url": "https://careers.swiggy.com",
        "tags": ["python", "django", "aws", "docker", "rest"],
        "description": "Develop and maintain core delivery and order management dispatch services. Optimize database queries in PostgreSQL and manage asynchronous tasks using Redis and Kafka."
    },
    {
        "id": "ind-3",
        "title": "Backend Platform Engineer",
        "company_name": "PhonePe",
        "candidate_required_location": "Pune, Maharashtra, India",
        "url": "https://www.phonepe.com/careers",
        "tags": ["python", "fastapi", "sql", "kubernetes", "aws"],
        "description": "Engineer highly secure transaction platforms and settlement infrastructure handling millions of daily UPI operations with Python and cloud services."
    },
    {
        "id": "ind-4",
        "title": "Full Stack Web Developer",
        "company_name": "Zoho",
        "candidate_required_location": "Chennai, Tamil Nadu, India",
        "url": "https://www.zoho.com/careers",
        "tags": ["javascript", "react", "python", "html", "css", "sql"],
        "description": "Build responsive SaaS interfaces and robust backend integration APIs for Zoho Workplace suites using React, Python, and relational database systems."
    },
    {
        "id": "ind-5",
        "title": "Data & Backend Engineer",
        "company_name": "Zomato",
        "candidate_required_location": "Gurugram, Haryana, India",
        "url": "https://www.zomato.com/careers",
        "tags": ["python", "sql", "redis", "fastapi", "docker"],
        "description": "Design live kitchen event streaming pipelines and RESTful microservices supporting real-time tracking, customer notifications, and partner dashboard APIs."
    }
]

def fetch_jobs(query: str = "python", *args, **kwargs) -> list:
    """
    Fetches curated Indian tech roles and live remote listings.
    Accepts arbitrary args/kwargs to avoid signature mismatches with Streamlit cache wrappers.
    """
    url = f"https://remotive.com/api/remote-jobs?search={query}&limit=10"
    jobs = []
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json().get("jobs", [])
            for item in data:
                location = item.get("candidate_required_location", "").lower()
                if any(k in location for k in ["india", "worldwide", "anywhere"]):
                    jobs.append({
                        "id": str(item.get("id")),
                        "title": item.get("title"),
                        "company_name": item.get("company_name"),
                        "candidate_required_location": item.get("candidate_required_location", "Remote"),
                        "url": item.get("url"),
                        "tags": [t.lower() for t in item.get("tags", [])],
                        "description": item.get("description", "")
                    })
    except Exception:
        pass

    combined = INDIA_COMPANIES_DATABASE + jobs
    
    seen = set()
    unique_jobs = []
    for j in combined:
        key = (j["title"].lower(), j["company_name"].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(j)
            
    return unique_jobs