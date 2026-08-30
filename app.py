import streamlit as st
from src.parser import extract_text_from_pdf
from src.job_api import fetch_jobs
from src.ai_matcher import extract_skills_from_resume, calculate_job_match, analyze_skill_gap

st.set_page_config(
    page_title="AI Job Search & Resume Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Job Search & Resume Matcher Assistant")
st.write("Upload your resume to discover matching job opportunities, skill gap analysis, and tailored recommendations.")

# --- Sidebar: Resume Upload & Skill Discovery ---
st.sidebar.header("📄 1. Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])

resume_text = ""
resume_skills = []

if uploaded_file:
    with st.sidebar.status("Processing Resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        resume_skills = extract_skills_from_resume(resume_text)
    
    st.sidebar.success(f"Extracted {len(resume_skills)} Skills!")
    
    if resume_skills:
        st.sidebar.subheader("Detected Skills:")
        st.sidebar.write(", ".join(resume_skills))
    else:
        st.sidebar.warning("No standard tech skills detected. Consider expanding your resume content.")

# --- Search & Filter Controls ---
col_search, col_sort = st.columns([3, 1])

with col_search:
    search_query = st.text_input("🔍 Search roles, companies, or keywords (e.g., Python, AI, AWS, Google)", value="python")

with col_sort:
    sort_by_match = st.selectbox("Sort By", ["Highest Match %", "Default Feed"])

# --- Fetch & Match Jobs ---
job_listings = fetch_jobs(tag=search_query, limit=10)

# Process scores for each job
enriched_jobs = []
for job in job_listings:
    score = calculate_job_match(resume_skills, job["tags"], job["description"]) if resume_skills else 0
    gap = analyze_skill_gap(resume_skills, job["tags"])
    
    enriched_jobs.append({
        **job,
        "match_score": score,
        "matching_skills": gap["matching"],
        "missing_skills": gap["missing"]
    })

if sort_by_match == "Highest Match %" and resume_skills:
    enriched_jobs.sort(key=lambda x: x["match_score"], reverse=True)

# --- Main Job Feed Display ---
st.subheader(f"📋 Available Opportunities ({len(enriched_jobs)})")

if not uploaded_file:
    st.info("💡 Upload your resume on the left sidebar to unlock personalized AI Match Scores and Skill Gap recommendations.")

for job in enriched_jobs:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### [{job['title']}]({job['url']})")
            st.markdown(f"🏢 **{job['company']}** &nbsp;|&nbsp; 📍 {job['location']}")
            st.write(job['description'])
            
            # Render Tags
            tags_display = " ".join([f"`{t}`" for t in job["tags"]])
            st.markdown(f"**Required Tags:** {tags_display}")
            
            # Skill Gap Analysis Display (When resume is provided)
            if uploaded_file and resume_skills:
                match_col, miss_col = st.columns(2)
                with match_col:
                    matching_str = ", ".join(job["matching_skills"]) if job["matching_skills"] else "None"
                    st.markdown(f"✅ **Matching Skills:** `{matching_str}`")
                with miss_col:
                    missing_str = ", ".join(job["missing_skills"]) if job["missing_skills"] else "None"
                    st.markdown(f"⚠️ **Missing Skills:** `{missing_str}`")

        with col2:
            if uploaded_file and resume_skills:
                st.metric(label="AI Fit Score", value=f"{job['match_score']}%")
                st.progress(job['match_score'] / 100)
                
                if job['match_score'] >= 70:
                    st.success("High Fit")
                elif job['match_score'] >= 40:
                    st.warning("Moderate Fit")
                else:
                    st.error("Skill Gap")
            else:
                st.write("")
                st.caption("Upload resume to calculate match score.")
                
            st.link_button("Apply on Company Portal ↗", job['url'], use_container_width=True)

st.markdown("---")
st.caption("AI Job Search & Resume Matcher Assistant | Week 3 Project Build")