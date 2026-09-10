import streamlit as st

# Custom module imports
from src.parser import extract_text_from_pdf
from src.job_api import fetch_jobs
from src.ai_matcher import extract_skills_from_resume, calculate_job_match, analyze_skill_gap
from src.ai_generator import generate_cover_letter, generate_resume_tips

st.set_page_config(
    page_title="AI Job Search & Resume Assistant",
    page_icon="💼",
    layout="wide"
)

# --- SIDEBAR: Resume Upload ---
with st.sidebar:
    st.header("📄 1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    
    resume_text = ""
    resume_skills = []
    
    if uploaded_file is not None:
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
            st.success(f"Uploaded: {uploaded_file.name}")
            
            # Extract skills using the matcher module
            resume_skills = extract_skills_from_resume(resume_text)
            
            with st.expander("Detected Skills"):
                if resume_skills:
                    st.write(", ".join(resume_skills))
                else:
                    st.caption("No standard skills parsed.")
                    
            with st.expander("Preview Extracted Text"):
                st.caption(resume_text[:400] + "...")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    else:
        st.info("Upload a PDF resume to enable match scores and AI generation tools.")

# --- MAIN CONTENT ---
st.title("💼 AI Job Search & Resume Assistant")
st.write("Upload your resume to discover matching job opportunities, skill gap analysis, and tailored AI recommendations.")

col1, col2 = st.columns([3, 1])
with col1:
    search_query = st.text_input("🔍 Search roles, companies, or keywords", value="python")
with col2:
    sort_option = st.selectbox("Sort By", ["Highest Match %", "Newest"])

# Fetch live jobs from the Remotive API
with st.spinner("Fetching live remote jobs..."):
    jobs = fetch_jobs(search_query=search_query, limit=15)

# Calculate match metrics using ai_matcher
for job in jobs:
    if resume_text:
        job["match_score"] = calculate_job_match(resume_text, job.get("tags", []), job.get("description", ""))
        job["missing_skills"] = analyze_skill_gap(resume_skills, job.get("tags", []))
    else:
        job["match_score"] = 0
        job["missing_skills"] = []

# Sort listings
if sort_option == "Highest Match %" and resume_text:
    jobs = sorted(jobs, key=lambda x: x.get("match_score", 0), reverse=True)

st.subheader(f"📋 Available Opportunities ({len(jobs)})")

if not jobs:
    st.warning("No live jobs found matching your criteria. Try searching for terms like 'python', 'react', 'data', or 'engineer'.")

# Render Job Listings
for i, job in enumerate(jobs):
    with st.container():
        st.markdown("---")
        title_col, btn_col = st.columns([4, 1])
        
        with title_col:
            st.markdown(f"### [{job.get('title', 'Role')}]({job.get('url', '#')})")
            st.write(f"🏢 **{job.get('company', 'Company')}** | 📍 {job.get('location', 'Remote')}")
        
        with btn_col:
            if job.get("url"):
                st.link_button("Apply on Portal ↗", job["url"])
            if resume_text:
                st.metric("Match Score", f"{job['match_score']}%")

        # Description Preview
        desc = job.get("description", "")
        preview_desc = desc[:300] + "..." if len(desc) > 300 else desc
        st.write(preview_desc)

        # Tags
        if job.get("tags"):
            tags_html = " ".join([f"`{t}`" for t in job["tags"][:8]])
            st.markdown(f"**Required Tags:** {tags_html}")

        # AI Tools
        if resume_text:
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("✨ Generate Cover Letter", key=f"cl_{job.get('id', i)}_{i}"):
                    with st.spinner("Drafting cover letter with Gemini..."):
                        letter = generate_cover_letter(
                            resume_text=resume_text,
                            job_title=job.get("title", ""),
                            company=job.get("company", ""),
                            job_desc=job.get("description", "")
                        )
                        st.text_area("Tailored Cover Letter", letter, height=250)
            
            with col_b:
                if st.button("🎯 Resume Improvement Tips", key=f"tips_{job.get('id', i)}_{i}"):
                    with st.spinner("Analyzing skill gaps with Gemini..."):
                        tips = generate_resume_tips(
                            resume_text=resume_text,
                            job_desc=job.get("description", ""),
                            missing_skills=job.get("missing_skills", [])
                        )
                        st.info(tips)