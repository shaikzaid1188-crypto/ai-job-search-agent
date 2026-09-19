import streamlit as st
from src.parser import extract_text_from_pdf, extract_skills
from src.job_api import fetch_jobs
from src.ai_matcher import calculate_match
from src.ai_generator import generate_cover_letter, generate_resume_tips

st.set_page_config(
    page_title="AI Job Search & Resume Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Sleek CSS Styling
st.markdown("""
<style>
    /* Gradient Headers */
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        color: #9CA3AF;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    
    /* Job Cards */
    .job-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .job-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }
    
    /* Glowing Skill Chips */
    .skill-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 6px;
        padding: 3px 9px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 3px 3px 3px 0;
    }

    /* Streamlit Button Overrides */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        border-color: #6366F1;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.35);
    }
</style>
""", unsafe_allow_html=True)

# Main Title Section
st.markdown('<div class="hero-title">⚡ AI Job Search & Resume Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Accelerate your tech job search across India with automated ATS scoring & generative cover letters.</div>', unsafe_allow_html=True)

# Sidebar: Resume upload & Filters
st.sidebar.markdown("### 📄 1. Candidate Resume")
uploaded_file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])

resume_text = ""
resume_skills = []

if uploaded_file:
    with st.spinner("Extracting text and technical skills..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        resume_skills = extract_skills(resume_text)
    
    st.sidebar.success(f"✓ Uploaded: {uploaded_file.name}")
    
    with st.sidebar.expander("✨ Detected Resume Skills", expanded=True):
        if resume_skills:
            badges_html = "".join([f'<span class="skill-badge">{s}</span>' for s in resume_skills])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.write("No common tech keywords found.")
            
    with st.sidebar.expander("🔍 Extracted Text Preview", expanded=False):
        st.text(resume_text[:400] + "..." if len(resume_text) > 400 else resume_text)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📍 2. Preferences")
selected_location = st.sidebar.selectbox(
    "Preferred Hub / City",
    ["All Locations", "Bengaluru", "Pune", "Gurugram", "Chennai", "Hyderabad", "Remote"]
)

# Search Bar Area
search_col1, search_col2 = st.columns([3, 1])
with search_col1:
    search_keyword = st.text_input("🔍 Search Role, Skill, or Tech Stack", value="Python")
with search_col2:
    st.write("")
    refresh_button = st.button("Find Opportunities", use_container_width=True)

# Fetch jobs
jobs = fetch_jobs(query=search_keyword)

if selected_location != "All Locations":
    jobs = [
        job for job in jobs 
        if selected_location.lower() in job.get("candidate_required_location", "").lower()
    ]

st.markdown("---")

if not jobs:
    st.warning(f"No job openings found matching '{search_keyword}' in '{selected_location}'. Try another keyword or location.")
else:
    for job in jobs:
        score, matched_skills, missing_skills = calculate_match(resume_skills, job["tags"])
        
        # Color coding score
        if score >= 70:
            score_pill = f'<span style="color:#10B981; font-size: 1.4rem; font-weight:700;">🟢 {score}% Match</span>'
        elif score >= 40:
            score_pill = f'<span style="color:#FBBF24; font-size: 1.4rem; font-weight:700;">🟡 {score}% Match</span>'
        else:
            score_pill = f'<span style="color:#EF4444; font-size: 1.4rem; font-weight:700;">🔴 {score}% Match</span>'

        tags_html = "".join([f'<span class="skill-badge">{t}</span>' for t in job["tags"]])

        # Glassmorphic Job Card
        card_html = f"""
        <div class="job-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h3 style="margin: 0 0 6px 0; color: #FFFFFF;">{job['title']}</h3>
                    <p style="margin: 0 0 10px 0; color: #9CA3AF;">🏢 <b>{job['company_name']}</b> &nbsp;|&nbsp; 📍 {job['candidate_required_location']}</p>
                </div>
                <div>{score_pill}</div>
            </div>
            <p style="color: #D1D5DB; font-size: 0.95rem; margin-bottom: 12px;">{job['description'][:280]}...</p>
            <div>{tags_html}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Action Buttons
        col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 6])
        with col_btn1:
            if st.button("✨ Cover Letter", key=f"cl_{job['id']}"):
                if not resume_text:
                    st.error("Please upload your resume first!")
                else:
                    with st.spinner("Generating letter..."):
                        letter = generate_cover_letter(resume_text, job["title"], job["company_name"], job["description"])
                        st.session_state[f"cover_letter_{job['id']}"] = letter

        with col_btn2:
            if st.button("🎯 ATS Advice", key=f"tips_{job['id']}"):
                if not resume_text:
                    st.error("Please upload your resume first!")
                else:
                    with st.spinner("Analyzing keyword gaps..."):
                        tips = generate_resume_tips(resume_text, job["description"], missing_skills)
                        st.session_state[f"tips_{job['id']}"] = tips
                        
        with col_btn3:
            st.link_button("Apply on Portal ↗", job["url"])

        # Generated Output Containers
        if f"cover_letter_{job['id']}" in st.session_state:
            letter_content = st.session_state[f"cover_letter_{job['id']}"]
            st.markdown("**Tailored Cover Letter**")
            st.text_area("", value=letter_content, height=220, key=f"txt_cl_{job['id']}")
            st.download_button(
                label="💾 Download as .txt",
                data=letter_content,
                file_name=f"Cover_Letter_{job['company_name']}.txt",
                mime="text/plain",
                key=f"dl_{job['id']}"
            )
            
        if f"tips_{job['id']}" in st.session_state:
            st.info(st.session_state[f"tips_{job['id']}"])
            
        st.write("")