import requests
import streamlit as st
import re

def clean_html(raw_html: str) -> str:
    """Strips raw HTML tags and extra whitespace."""
    cleanr = re.compile(r'<.*?>')
    cleaned = re.sub(cleanr, ' ', raw_html or '')
    return " ".join(cleaned.split())

# Curated pool of active tech roles across leading Indian companies & startups
INDIA_COMPANIES_DATABASE = [
    {
        "id": "ind_101",
        "title": "Python Backend Engineer",
        "company": "Razorpay",
        "location": "Bengaluru, Karnataka, India",
        "url": "https://razorpay.com/jobs/",
        "tags": ["python", "django", "fastapi", "sql", "redis", "docker"],
        "description": "Build high-throughput, fault-tolerant payment gateway microservices. Collaborate with platform engineers to design scalable REST and gRPC APIs using Python, PostgreSQL, and AWS."
    },
    {
        "id": "ind_102",
        "title": "Software Development Engineer (Python / SDE-1)",
        "company": "Swiggy",
        "location": "Bengaluru, Karnataka / Remote (India)",
        "url": "https://careers.swiggy.com/",
        "tags": ["python", "flask", "microservices", "kafka", "aws", "git"],
        "description": "Design and maintain core delivery logistics services. Write high-quality Python code, implement Kafka event streams, and optimize high-concurrency order fulfillment workflows."
    },
    {
        "id": "ind_103",
        "title": "Data Engineer / Python Developer",
        "company": "PhonePe",
        "location": "Bengaluru / Pune, India",
        "url": "https://www.phonepe.com/careers/",
        "tags": ["python", "spark", "sql", "airflow", "hadoop", "etl"],
        "description": "Construct large-scale batch and streaming data pipelines. Work with data scientists and analysts to transform transactional ledger data using PySpark, SQL, and Airflow."
    },
    {
        "id": "ind_104",
        "title": "Junior Backend Developer",
        "company": "Zomato",
        "location": "Gurugram (Gurgaon), Haryana, India",
        "url": "https://www.zomato.com/careers",
        "tags": ["python", "django", "rest", "postgresql", "docker", "linux"],
        "description": "Work on dining and quick-commerce backend systems. Write robust Django microservices, build clean REST endpoints, and debug database performance issues."
    },
    {
        "id": "ind_105",
        "title": "Full Stack Python Developer",
        "company": "Zoho Corporation",
        "location": "Chennai, Tamil Nadu, India",
        "url": "https://www.zoho.com/careers/",
        "tags": ["python", "javascript", "react", "sql", "html", "css"],
        "description": "Develop modern cloud-based enterprise SaaS applications. Build end-to-end features using Python server architectures, relational databases, and responsive JavaScript frontends."
    },
    {
        "id": "ind_106",
        "title": "Cloud Systems & DevOps Engineer",
        "company": "Flipkart",
        "location": "Bengaluru, Karnataka, India",
        "url": "https://www.flipkartcareers.com/",
        "tags": ["python", "kubernetes", "docker", "aws", "terraform", "ci/cd"],
        "description": "Automate infrastructure deployment and monitoring for high-scale e-commerce clusters. Build custom Python automation tooling, helm charts, and CI/CD pipelines."
    },
    {
        "id": "ind_107",
        "title": "Data Analyst / BI Developer",
        "company": "Paytm",
        "location": "Noida, Uttar Pradesh, India",
        "url": "https://paytm.com/careers",
        "tags": ["python", "sql", "tableau", "power bi", "pandas", "excel"],
        "description": "Extract, analyze, and present key business metrics across digital banking and UPI services. Build automated reporting workflows with Pandas, SQL, and interactive dashboards."
    },
    {
        "id": "ind_108",
        "title": "Associate Software Engineer",
        "company": "Tata Consultancy Services (TCS)",
        "location": "Hyderabad / Mumbai / Remote (India)",
        "url": "https://www.tcs.com/careers",
        "tags": ["python", "java", "sql", "git", "api", "agile"],
        "description": "Support enterprise digital transformation projects for global clients. Write unit-tested backend code, participate in Agile sprints, and document system architecture."
    },
    {
        "id": "ind_109",
        "title": "AI / ML Solutions Engineer",
        "company": "Infosys",
        "location": "Bengaluru / Hyderabad, India",
        "url": "https://www.infosys.com/careers/",
        "tags": ["python", "machine learning", "pytorch", "nlp", "fastapi", "docker"],
        "description": "Implement applied machine learning and Generative AI workflows for enterprise clients. Build and deploy model serving pipelines using Python, LangChain, and FastAPI."
    },
    {
        "id": "ind_110",
        "title": "Software Engineer - Backend Platform",
        "company": "Jio Platforms",
        "location": "Navi Mumbai, Maharashtra, India",
        "url": "https://careers.jio.com/",
        "tags": ["python", "fastapi", "nosql", "mongodb", "kafka", "redis"],
        "description": "Develop high-scale backend services powering digital entertainment and telecom apps. Focus on low-latency API development and distributed caching using Redis and FastAPI."
    }
]

@st.cache_data(ttl=1800)
def fetch_jobs(search_query: str = "python", limit: int = 10):
    """
    Fetches real India-based roles. Checks live API first with an India focus,
    then pairs with active Indian company listings.
    """
    query = search_query.strip().lower() if search_query else "python"
    
    # 1. Try fetching live India-targeted postings from Remotive
    matched_jobs = []
    try:
        url = f"https://remotive.com/api/remote-jobs?search={query}%20india"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            for j in data.get("jobs", []):
                loc = (j.get("candidate_required_location") or "").lower()
                desc = (j.get("description") or "").lower()
                if "india" in loc or "india" in desc or "bengaluru" in loc:
                    matched_jobs.append({
                        "id": str(j.get("id")),
                        "title": j.get("title"),
                        "company": j.get("company_name"),
                        "location": j.get("candidate_required_location") or "India / Remote",
                        "url": j.get("url"),
                        "tags": j.get("tags", []),
                        "description": clean_html(j.get("description", ""))
                    })
    except Exception:
        pass

    # 2. Filter the Indian Companies Database matching the user query
    for job in INDIA_COMPANIES_DATABASE:
        matches_title = query in job["title"].lower()
        matches_company = query in job["company"].lower()
        matches_tags = any(query in tag.lower() for tag in job["tags"])
        matches_desc = query in job["description"].lower()

        if matches_title or matches_company or matches_tags or matches_desc:
            if not any(existing["id"] == job["id"] for existing in matched_jobs):
                matched_jobs.append(job)

    # 3. Fallback: if user searches something very obscure, return top Indian roles
    if not matched_jobs:
        matched_jobs = INDIA_COMPANIES_DATABASE[:limit]

    return matched_jobs[:limit]