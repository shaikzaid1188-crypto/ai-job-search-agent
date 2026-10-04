# ⚡ AI Job Search & Resume Assistant

An intelligent full-stack career platform built with Python and Streamlit that streamlines tech job hunting across India. The application pairs real-time job retrieval with automated resume skill extraction, ATS compatibility scoring, and context-tailored cover letter generation.

🌐 **Live Demo:** [ai-job-search-agent](https://ai-job-search-agent-9w4yjz5yu5emjpoq6ifkpv.streamlit.app)

---

## 🚀 Key Features
- **Real-Time Job Aggregation**: Connects to the JSearch `/search-v2` API via RapidAPI to query live tech roles across Indian metro hubs.
- **Dynamic Resume Parser**: Extracts text and isolates key technical skills from both `.pdf` and `.docx` resumes.
- **ATS Match Engine**: Performs keyword intersection analysis against job specifications to deliver immediate compatibility scores.
- **Generative Cover Letters**: Leverages Google Gemini to generate role-aligned, 3-paragraph personalized application letters.

---

## 🛠️ Tech Stack
- **Frontend / Deployment**: Streamlit, Streamlit Community Cloud
- **Backend / Core**: Python 3.12, Requests, Regular Expressions
- **APIs**: RapidAPI (JSearch `/search-v2`), Google Generative AI (Gemini)
- **Document Processing**: `pypdf`, `python-docx`

---

## 💻 Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shaikzaid1188-crypto/ai-job-search-agent.git](https://github.com/shaikzaid1188-crypto/ai-job-search-agent.git)
   cd ai-job-search-agent