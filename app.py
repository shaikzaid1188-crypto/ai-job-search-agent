import streamlit as st
from src.parser import extract_text_from_pdf
from src.job_api import fetch_jobs

st.set_page_config(page_title="AI Job Search Agent", layout="wide")

st.title("💼 AI Job Search & Resume Assistant")
st.write("Upload your resume and discover matching live job opportunities.")

# Sidebar - Resume Upload
st.sidebar.header("1. Upload Resume")
uploaded_file = st.sidebar.file_uploader("Choose a PDF Resume", type=["pdf"])

resume_text = ""
if uploaded_file:
    with st.spinner("Extracting resume text..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        st.sidebar.success("Resume parsed successfully!")
        with st.sidebar.expander("Preview Extracted Resume"):
            st.text(resume_text[:400] + "...")

# Main Panel - Job Search
st.header("2. Live Job Search")
col1, col2 = st.columns([3, 1])

with col1:
    search_keyword = st.text_input("Enter Job Role or Skill (e.g., Python, Data, React)", value="python")
with col2:
    search_button = st.button("Search Jobs", use_container_width=True)

if search_button or search_keyword:
    with st.spinner(f"Fetching {search_keyword} listings..."):
        jobs = fetch_jobs(tag=search_keyword, limit=6)

        if jobs:
            st.subheader(f"Found {len(jobs)} Opportunities")
            for job in jobs:
                with st.container():
                    st.markdown(f"### [{job['title']}]({job['url']})")
                    st.write(f"**Company:** {job['company']} | **Location:** {job['location']}")
                    st.write(f"**Tags:** `{', '.join(job['tags'][:5])}`")
                    st.write(job['description'])
                    st.markdown("---")
        else:
            st.warning("No jobs found for that tag. Try terms like 'python', 'react', or 'data'.")