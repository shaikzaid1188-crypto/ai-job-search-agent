import streamlit as st

from src.parser import extract_text_from_pdf
from src.job_api import fetch_jobs
from src.ai_matcher import (
    extract_skills_from_resume,
    calculate_job_match,
    analyze_skill_gap
)


# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="AI Job Search Agent",
    layout="wide"
)

st.title("💼 AI Job Search & Resume Assistant")

st.write(
    "Upload your resume and discover matching job opportunities using AI."
)


# ==============================
# 1. RESUME UPLOAD
# ==============================

st.sidebar.header("1. Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF Resume",
    type=["pdf"]
)

resume_text = ""
extracted_skills = []


if uploaded_file:

    with st.spinner("Extracting resume text..."):

        resume_text = extract_text_from_pdf(
            uploaded_file
        )

    if resume_text:

        st.sidebar.success(
            "Resume parsed successfully!"
        )

        with st.sidebar.expander(
            "Preview Extracted Resume"
        ):

            st.text(
                resume_text[:1000] + "..."
            )

        # Gemini is used for skill extraction
        with st.spinner(
            "AI is analyzing your resume..."
        ):

            extracted_skills = extract_skills_from_resume(
                resume_text
            )

        if extracted_skills:

            st.subheader(
                "🤖 AI Extracted Skills"
            )

            st.write(
                ", ".join(extracted_skills)
            )

        else:

            st.warning(
                "No skills could be extracted from the resume."
            )

    else:

        st.error(
            "Could not extract text from the uploaded PDF."
        )


# ==============================
# 2. JOB SEARCH
# ==============================

st.header("2. Live Job Search")

col1, col2 = st.columns([3, 1])


with col1:

    search_keyword = st.text_input(
        "Enter Job Role or Skill (e.g., Python, Data, React)",
        value=""
    )


st.caption("💡 Try: Python, React, Java, Data, AI, or FastAPI")

with col2:

    search_button = st.button(
        "Search Jobs",
        use_container_width=True
    )


# ==============================
# JOB SEARCH EXECUTION
# ==============================

if search_button or search_keyword:

    try:

        with st.spinner(
            f"Fetching {search_keyword} listings..."
        ):

            jobs = fetch_jobs(
                tag=search_keyword,
                limit=6
            )

    except Exception as e:

        st.error(
            "Something went wrong while fetching jobs. "
            "Please try again."
        )

        st.caption(
            f"Error details: {e}"
        )

        jobs = []


    # ==============================
    # DISPLAY JOB RESULTS
    # ==============================

    if jobs:

        st.subheader(
            f"Found {len(jobs)} Opportunities"
        )

        for job in jobs:

            # ==============================
            # PROFESSIONAL JOB CARD
            # ==============================

            with st.container(border=True):

                st.markdown(
                    f"## 💼 [{job['title']}]({job['url']})"
                )

                st.markdown(
                    f"**🏢 {job['company']}** | "
                    f"📍 {job['location']}"
                )

                st.markdown(
                    "**Skills:** "
                    + " • ".join(
                        f"`{tag}`"
                        for tag in job["tags"][:5]
                    )
                )

                st.write(
                    job["description"]
                )


                # ==============================
                # AI JOB MATCHING
                # ==============================

                if extracted_skills:

                    match_result = calculate_job_match(
                        extracted_skills,
                        job
                    )

                    st.metric(
                        "🎯 AI Match Score",
                        f"{match_result['score']}%"
                    )

                    st.info(
                        f"**AI Analysis:** "
                        f"{match_result['reason']}"
                    )


                    # ==============================
                    # SKILL GAP ANALYSIS
                    # ==============================

                    gap_result = analyze_skill_gap(
                        extracted_skills,
                        job
                    )

                    st.write(
                        "🧩 **Skill Gap Analysis**"
                    )


                    if gap_result["missing_skills"]:

                        st.write(
                            "**Missing Skills:** "
                            + ", ".join(
                                gap_result[
                                    "missing_skills"
                                ]
                            )
                        )

                    else:

                        st.success(
                            "No major skill gaps detected."
                        )


                    st.write(
                        f"**💡 Recommendation:** "
                        f"{gap_result['recommendation']}"
                    )


                st.markdown("---")


    else:

        st.warning(
            "No jobs found for that search. "
            "Try terms like 'python', 'react', or 'data'."
        )


# ==============================
# FOOTER
# ==============================

st.markdown("---")

st.caption(
    "🤖 AI Job Search Agent | Built with Streamlit & Gemini AI"
)