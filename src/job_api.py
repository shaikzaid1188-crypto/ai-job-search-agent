import os
import requests
import re
from dotenv import load_dotenv

load_dotenv(override=True)


def get_rapidapi_key() -> str:
    """Dynamically fetches the RapidAPI key from Streamlit secrets or env vars."""
    key = ""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "RAPIDAPI_KEY" in st.secrets:
            key = st.secrets["RAPIDAPI_KEY"]
    except Exception:
        pass

    if not key:
        key = os.getenv("RAPIDAPI_KEY", "")
    return key.strip() if key else ""


def clean_html(raw_html: str) -> str:
    """Strips HTML tags and normalizes whitespace."""
    cleanr = re.compile(r"<.*?>")
    cleaned = re.sub(cleanr, "", raw_html or "")
    return " ".join(cleaned.split())


def _call_api(query_str: str) -> tuple[list, str]:
    """Queries JSearch search-v2 endpoint on RapidAPI and returns (jobs, error_message)."""
    api_key = get_rapidapi_key()
    if not api_key:
        err = "RAPIDAPI_KEY is missing or empty. Please check your Streamlit Cloud Secrets."
        print(f"[JSearch Error] {err}")
        return [], err

    url = "https://jsearch.p.rapidapi.com/search-v2"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    querystring = {
        "query": query_str,
        "country": "in",
        "page": "1",
        "num_pages": "1"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=12)
        if response.status_code == 200:
            res_json = response.json()
            data = res_json.get("data", [])
            if isinstance(data, dict):
                data = data.get("jobs", [])

            parsed_jobs = []
            for item in data:
                tags = [t.lower() for t in (item.get("job_required_skills") or []) if t]
                if not tags:
                    tags = [w.lower() for w in re.findall(r"\b[A-Za-z]{3,}\b", item.get("job_title", ""))]

                city = item.get("job_city") or ""
                state = item.get("job_state") or ""
                loc_parts = [p for p in [city, state, "India"] if p]
                location = ", ".join(loc_parts) if loc_parts else "India (Remote/Hybrid)"

                parsed_jobs.append({
                    "id": item.get("job_id", ""),
                    "title": item.get("job_title", "Position Title Not Listed"),
                    "company_name": item.get("employer_name", "Confidential"),
                    "candidate_required_location": location,
                    "url": item.get("job_apply_link") or item.get("job_google_link") or "#",
                    "tags": tags,
                    "description": clean_html(item.get("job_description", "")[:600])
                })
            return parsed_jobs, ""
        else:
            err = f"API Error {response.status_code}: {response.text}"
            print(f"[JSearch Error] {err}")
            return [], err
    except Exception as e:
        err = f"Request failed: {e}"
        print(f"[JSearch Exception] {err}")
        return [], err


def fetch_jobs(query: str = "Python", company: str = "All Companies", *args, **kwargs) -> tuple[list, str]:
    """
    Fetches real-time Indian job postings targeting specific enterprises or broad searches.
    Returns (jobs, error_message).
    """
    clean_query = query.strip() if query else "Python Developer"

    if company and company != "All Companies":
        search_term = f'"{company}" {clean_query} jobs in India'
        jobs, err = _call_api(search_term)
        exact_matches = [j for j in jobs if company.lower() in j.get("company_name", "").lower()]
        if exact_matches:
            return exact_matches, ""

        direct_results, err = _call_api(f'jobs at {company} India')
        company_filtered = [j for j in direct_results if company.lower() in j.get("company_name", "").lower()]
        if company_filtered:
            return company_filtered, ""

        return jobs, err

    return _call_api(f"{clean_query} in India")