import streamlit as st
from src.parser import extract_text_from_pdf
from src.job_api import fetch_jobs
from src.ai_matcher import extract_skills_from_resume, calculate_job_match, analyze_skill_gap
from src.ai_generator import generate_cover_letter, generate_resume_tips

st.set_page_config(
    page_title="AI Job Search & Resume Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Job Search & Resume Assistant")
st.write("Upload your resume to discover matching job opportunities, skill gap analysis, and tailored AI recommendations.")

# --- Sidebar: Resume Upload & Skill Extraction ---
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
    st.sidebar.info("Upload a PDF resume to enable match scores and AI generation tools.")

# --- Search & Sorting ---
col_search, col_sort = st.columns([3, 1])
with col_search:
    search_query = st.text_input("🔍 Search roles, companies, or keywords", value="python")
with col_sort:
    sort_by_match = st.selectbox("Sort By", ["Highest Match %", "Default Feed"])

# --- Fetch & Enrich Listings ---
job_listings = fetch_jobs(tag=search_query, limit=10)
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

# --- Listings Feed ---
st.subheader(f"📋 Available Opportunities ({len(enriched_jobs)})")

for job in enriched_jobs:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### [{job['title']}]({job['url']})")
            st.markdown(f"🏢 **{job['company']}** &nbsp;|&nbsp; 📍 {job['location']}")
            st.write(job['description'])
            
            tags_display = " ".join([f"`{t}`" for t in job["tags"]])
            st.markdown(f"**Required Tags:** {tags_display}")
            
            if uploaded_file and resume_skills:
                m_col, g_col = st.columns(2)
                with m_col:
                    st.markdown(f"✅ **Matching:** `{', '.join(job['matching_skills']) or 'None'}`")
                with g_col:
                    st.markdown(f"⚠️ **Skill Gaps:** `{', '.join(job['missing_skills']) or 'None'}`")

        with col2:
            if uploaded_file and resume_skills:
                st.metric("AI Fit Score", f"{job['match_score']}%")
                st.progress(job['match_score'] / 100)
            st.link_button("Apply on Portal ↗", job['url'], use_container_width=True)

        # AI Assistant Expander for each role
        if uploaded_file:
            with st.expander(f"🤖 AI Assistant for {job['title']}"):
                tab1, tab2 = st.tabs(["📝 Tailored Cover Letter", "💡 Resume Optimization Tips"])
                
                with tab1:
                    if st.button(f"Generate Cover Letter for {job['company']}", key=f"cl_{job['id']}"):
                        with st.spinner("Drafting cover letter..."):
                            letter = generate_cover_letter(resume_text, job["title"], job["company"], job["description"])
                            st.text_area("Customized Cover Letter", letter, height=220)
                            
                            # One-click download button
                            clean_filename = f"{job['company']}_{job['title']}_Cover_Letter.txt".replace(" ", "_")
                            st.download_button(
                                label="💾 Download Cover Letter (.txt)",
                                data=letter,
                                file_name=clean_filename,
                                mime="text/plain",
                                key=f"dl_{job['id']}"
                            )
                
                with tab2:
                    if st.button(f"Get Tailoring Tips for {job['company']}", key=f"tips_{job['id']}"):
                        with st.spinner("Analyzing resume against role requirements..."):
                            tips = generate_resume_tips(resume_text, job["description"], job["missing_skills"])
                            st.markdown(tips)

st.markdown("---")
st.caption("AI Job Search & Resume Matcher Assistant | Final Week 4 Build")