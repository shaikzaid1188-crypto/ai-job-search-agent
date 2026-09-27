import streamlit as st
from src.parser import extract_text, extract_skills
from src.job_api import fetch_jobs
from src.ai_matcher import calculate_ats_match
from src.ai_generator import generate_cover_letter

st.set_page_config(
    page_title="AI Job Search & Resume Assistant",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #2e344e;
        margin-bottom: 12px;
    }
    .skill-badge {
        display: inline-block;
        background-color: #2b314e;
        color: #90caf9;
        border-radius: 6px;
        padding: 3px 8px;
        margin: 2px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR: RESUME UPLOAD & PARSING -----------------
with st.sidebar:
    st.header("📄 1. Candidate Resume")
    uploaded_file = st.file_uploader("Upload Resume (.pdf or .docx)", type=["pdf", "docx"])

    resume_text = ""
    detected_skills = []

    if uploaded_file is not None:
        try:
            resume_text = extract_text(uploaded_file)
            detected_skills = extract_skills(resume_text)
            st.success(f"✓ Uploaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error parsing resume: {e}")

    if detected_skills:
        with st.expander("✨ Detected Resume Skills", expanded=True):
            skill_html = "".join([f"<span class='skill-badge'>{skill}</span>" for skill in detected_skills])
            st.markdown(skill_html, unsafe_allow_html=True)

    if resume_text:
        with st.expander("🔍 Extracted Text Preview"):
            st.text_area("Resume Content", resume_text[:1200] + ("..." if len(resume_text) > 1200 else ""), height=180)

# ----------------- MAIN APP: SEARCH & JOB MATCHING -----------------
st.title("⚡ AI Job Search & Resume Assistant")
st.caption("Accelerate your tech job search across India with automated ATS scoring & generative cover letters.")

default_search = detected_skills[0].title() if detected_skills else "Python Developer"

col_search, col_filter, col_btn = st.columns([3, 2, 1])

with col_search:
    search_query = st.text_input("🔍 Search Role, Skill, or Tech Stack", value=default_search)

with col_filter:
    target_company = st.selectbox(
        "🏢 Target Company",
        [
            "All Companies",
            "TCS",
            "Infosys",
            "Wipro",
            "Google",
            "Microsoft",
            "Amazon",
            "Accenture",
            "Cognizant",
            "IBM",
            "Oracle",
            "HCL"
        ]
    )

with col_btn:
    st.write("")
    search_clicked = st.button("Find Opportunities", use_container_width=True)

if search_query or search_clicked:
    display_company = f"at {target_company}" if target_company != "All Companies" else "across India"
    with st.spinner(f"Fetching live openings for '{search_query}' {display_company}..."):
        jobs, error_msg = fetch_jobs(query=search_query, company=target_company)

    if error_msg:
        st.error(f"⚠️ {error_msg}")
    elif not jobs:
        st.warning(f"No job openings found matching '{search_query}' {display_company}. Try selecting 'All Companies' or a different role.")
    else:
        st.subheader(f"💼 Open Opportunities ({len(jobs)} Found)")

        for idx, job in enumerate(jobs):
            score, matching_skills, missing_skills = calculate_ats_match(
                detected_skills,
                job,
                job_description=f"{job.get('title', '')} {job.get('description', '')}"
            )

            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"### [{job.get('title')}]({job.get('url')})")
                    st.markdown(f"**🏢 {job.get('company_name')}**  |  📍 {job.get('candidate_required_location')}")
                    st.write(job.get("description", "No description provided.")[:320] + "...")

                    if matching_skills:
                        matched_html = " ".join([f"<span class='skill-badge' style='color:#a7f3d0;'>✓ {s}</span>" for s in matching_skills])
                        st.markdown(f"**Matches:** {matched_html}", unsafe_allow_html=True)

                with c2:
                    if detected_skills:
                        st.metric("ATS Match", f"{score}%")

                    st.link_button("Apply Directly ↗", job.get("url", "#"), use_container_width=True)

                    if st.button("Generate Cover Letter", key=f"btn_cov_{idx}", use_container_width=True):
                        if not resume_text:
                            st.warning("Please upload your resume in the sidebar first!")
                        else:
                            with st.spinner("Drafting targeted cover letter..."):
                                letter = generate_cover_letter(resume_text, job.get("description", ""))
                                st.session_state[f"letter_{idx}"] = letter

                if f"letter_{idx}" in st.session_state:
                    with st.expander("📝 Tailored Cover Letter", expanded=True):
                        st.text_area("Cover Letter", value=st.session_state[f"letter_{idx}"], height=240)

                st.divider()