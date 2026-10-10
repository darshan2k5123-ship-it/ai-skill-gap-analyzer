import os
import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt
import google.generativeai as genai
from dotenv import load_dotenv

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from skill_analyzer import (
    detect_skills,
    find_missing_skills,
    calculate_scores
)
from pdf_generator import generate_pdf
from data import skills_database, roles
load_dotenv()

GEMINI_API_KEY = (
    st.secrets.get("GEMINI_API_KEY")
    if "GEMINI_API_KEY" in st.secrets
    else os.getenv("GEMINI_API_KEY")
)


genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# Session State
if "career_advice" not in st.session_state:
    st.session_state.career_advice = ""

if "resume_review" not in st.session_state:
    st.session_state.resume_review = ""

if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = ""

if "ats_keywords" not in st.session_state:
    st.session_state.ats_keywords = ""

if "project_suggestions" not in st.session_state:
    st.session_state.project_suggestions = ""

if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = ""
st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🤖",
    layout="wide"
)
with st.sidebar:

    st.header("📌 Navigation")

    st.write("📄 Upload Resume")
    st.write("✅ Skill Analysis")
    st.write("📊 ATS Score")
    st.write("🎯 Resume Match")
    st.write("🤖 AI Career Mentor")
    st.write("📝 Resume Review")
    st.write("📥 Download Report")

    st.divider()

    st.subheader("🎯 Project Goal")

    st.info(
        "Analyze resumes, identify skill gaps, improve ATS score, and provide AI-powered career guidance."
    )
    st.divider()

    theme = st.selectbox(
        "🎨 Choose Theme",
        ["Light", "Dark"]
    )
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }

        div[data-testid="stMetric"] {
            background-color: #1E1E1E;
            border-radius: 10px;
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>
        div[data-testid="stMetric"] {
            border-radius: 10px;
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
# Title
st.title("🤖 AI Skill Gap Analyzer")
st.caption("Upload your resume and analyze your readiness for your dream job.")
st.divider()



# Dropdown Menu
role = st.selectbox(
    "Select Target Job Role",
    list(roles.keys())
)

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type=["pdf"]
)
st.subheader("📋 Paste Job Description (Optional)")

job_description = st.text_area(
    "Paste the Job Description here",
    height=200
)
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎯 Target Role", role)

with col2:
    if uploaded_file:
        st.metric("📄 Resume", "Uploaded")
    else:
        st.metric("📄 Resume", "Not Uploaded")

with col3:
    st.metric("📚 Skills Database", len(skills_database))

st.divider()

# Only run if resume is uploaded
if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            if page.extract_text():
                text += page.extract_text()

    # Skill Detection
    found_skills = detect_skills(text, skills_database)

    

    required_skills = roles[role]

    missing_skills = find_missing_skills(
        found_skills,
        required_skills
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Skills Found")

        for skill in found_skills:

            if skill == "Python":
                st.success("🟢 Python - Advanced")

            elif skill == "Java":
                st.success("🟡 Java - Intermediate")

            elif skill == "HTML":
                st.success("🟡 HTML - Intermediate")

            elif skill == "SQL":
                st.success("🟢 SQL - Advanced")

            else:
                st.success(f"🔵 {skill}")

    with col2:
        st.subheader("🚀 Skills to Learn")

        for skill in missing_skills:

            st.warning(f"📘 {skill}")
        
    score, ats_score, resume_match = calculate_scores(
        found_skills,
        missing_skills,
        required_skills,
        text
    )

    st.subheader("📊 Placement Readiness Score")

    st.progress(score / 100)

    st.metric("Overall Readiness", f"{score:.0f}%")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Skill Match", f"{score:.0f}%")

    with col2:
        st.metric("📄 ATS Score", f"{ats_score:.0f}%")

    with col3:
        st.metric("❌ Missing Skills", len(missing_skills))
    
    with col4:
        st.metric("📈 Resume Match", f"{resume_match:.0f}%")

    if score >= 80:
        st.success("🏆 Excellent Readiness")
    elif score >= 60:
        st.info("👍 Good Readiness")
    elif score >= 40:
        st.warning("📚 Moderate Readiness")
    else:
        st.error("⚠️ Needs Improvement")
    st.subheader("📈 Skills Analysis")
    st.subheader("📄 ATS Resume Score")

    

    if ats_score > 100:
        ats_score = 100

    st.progress(ats_score / 100)

    st.metric("ATS Score", f"{ats_score:.0f}%")

    if ats_score >= 85:
        st.success("✅ Excellent! Your resume is ATS-friendly.")

    elif ats_score >= 70:
        st.warning("⚠️ Good resume. Improve missing skills and add more projects.")

    else:
        st.error("❌ Resume needs improvement for ATS screening.")

    st.subheader("🎯 Resume Match")

    st.progress(resume_match / 100)

    st.write(
        f"Your resume matches **{resume_match:.0f}%** of the required skills for the **{role}** role."
    )
    
    st.subheader("💪 Resume Strengths")

    if len(found_skills) > 0:

        for skill in found_skills:
            st.success(f"Strong in {skill}")

    else:

        st.warning("No technical skills detected.")
    
    st.subheader("📌 Areas to Improve")

    for skill in missing_skills:
        st.warning(f"Learn {skill}")

    labels = ["Skills Found", "Missing Skills"]

    sizes = [len(found_skills), len(missing_skills)]

    fig, ax = plt.subplots()

    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)
    st.subheader("📚 Personalized Learning Roadmap")

    for i, skill in enumerate(missing_skills):
        st.write(f"Week {i+1}: Learn {skill}")

    st.subheader("📌 Quick Readiness Advice")

    if score >= 80:
        st.success(
            "You are highly ready for placements. Start applying for jobs."
        )

    elif score >= 60:
        st.warning(
            "You are close to being placement-ready. Focus on the missing skills."
        )

    else:
        st.error(
            "You need more preparation. Follow the roadmap and build projects."
        )
    if uploaded_file:

        # ---------- Analyze Resume ----------
        if st.button("🚀 Analyze Resume with AI"):

            with st.spinner("🤖 AI is analyzing your resume..."):

                try:

                    

                    ai_prompt = f"""
                    You are an expert career coach, resume reviewer, and professional
                    career advisor.

                    Analyze the candidate's resume for the target job role.

                    Target Role:
                    {role}

                    Resume:
                    {text}

                    Detected Skills:
                    {', '.join(found_skills)}

                    Missing Skills:
                    {', '.join(missing_skills)}

                    Placement Readiness:
                    {score:.0f}%

                    Return EXACTLY these three sections:

                    ## Career Advice

                    Give practical career advice based on the candidate's current skills,
                    missing skills, target role, and placement readiness.

                    ## Resume Review

                    Review the resume and give specific suggestions for:
                    - Technical skills
                    - Projects
                    - Resume content
                    - ATS compatibility
                    - Professional presentation

                    ## Professional Cover Letter

                    Write a concise and professional cover letter for the candidate
                    applying for the target role.

                    IMPORTANT:
                    1. Keep the three sections completely separate.
                    2. Do not repeat Career Advice inside Resume Review.
                    3. Do not repeat Resume Review inside Career Advice.
                    4. Do not repeat the Cover Letter in the other sections.
                    5. Use the exact section headings shown above.
                    6. Do not add any other major headings.
                    """

                    response = model.generate_content(ai_prompt)

                    full_response = response.text.strip()

                    # ----------------------------------------
                    # Extract separate AI sections
                    # ----------------------------------------

                    import re

                    career_advice = ""
                    resume_review = ""
                    cover_letter = ""

                    # Find Career Advice section
                    career_match = re.search(
                        r"(?:#{1,6}\s*)?(?:\*\*)?Career Advice(?:\*\*)?\s*:?\s*(.*?)(?=(?:#{1,6}\s*)?(?:\*\*)?Resume Review|$)",
                        full_response,
                        re.IGNORECASE | re.DOTALL
                    )

                    # Find Resume Review section
                    review_match = re.search(
                        r"(?:#{1,6}\s*)?(?:\*\*)?Resume Review(?:\*\*)?\s*:?\s*(.*?)(?=(?:#{1,6}\s*)?(?:\*\*)?(?:Professional )?Cover Letter|$)",
                        full_response,
                        re.IGNORECASE | re.DOTALL
                    )

                    # Find Cover Letter section
                    cover_match = re.search(
                        r"(?:#{1,6}\s*)?(?:\*\*)?(?:Professional )?Cover Letter(?:\*\*)?\s*:?\s*(.*)$",
                        full_response,
                        re.IGNORECASE | re.DOTALL
                    )

                    if career_match:
                        career_advice = career_match.group(1).strip()

                    if review_match:
                        resume_review = review_match.group(1).strip()

                    if cover_match:
                        cover_letter = cover_match.group(1).strip()

                    # Fallback messages
                    if not career_advice:
                        career_advice = "Career advice was not generated separately."

                    if not resume_review:
                        resume_review = "Resume review was not generated separately."

                    if not cover_letter:
                        cover_letter = "Cover letter was not generated separately."

                    # Store each section separately
                    st.session_state.career_advice = career_advice
                    st.session_state.resume_review = resume_review
                    st.session_state.cover_letter = cover_letter

                    st.session_state.analysis_done = True

                except Exception as e:
                    st.error(e)

        # ---------- Show AI Results ----------
        if st.session_state.analysis_done:

            st.subheader("🤖 AI Career Mentor")
            st.write(st.session_state.career_advice)

            st.subheader("📝 Resume Review")
            st.write(st.session_state.resume_review)

            st.subheader("📄 AI Cover Letter")
            st.write(st.session_state.cover_letter)
            st.subheader("⭐ Resume Rating")

            if score >= 90:
                st.success("9.5 / 10")
            elif score >= 80:
                st.success("8.5 / 10")
            elif score >= 70:
                st.info("7.5 / 10")
            elif score >= 60:
                st.warning("6.5 / 10")
            else:
                st.error("5 / 10")

            st.download_button(
                "📄 Download Cover Letter",
                st.session_state.cover_letter,
                file_name="Cover_Letter.txt"
            )

            # Interview Questions
            if st.button("🎤 Generate Interview Questions"):

                interview_prompt = f"""
    Generate:
    - 5 Technical Questions
    - 3 HR Questions
    - 2 Coding Questions

    Role: {role}
    Skills: {', '.join(found_skills)}
    """

                if not st.session_state.interview_questions:
                    interview = model.generate_content(interview_prompt)
                    st.session_state.interview_questions = interview.text

                st.subheader("🎤 AI Interview Questions")
                st.write(st.session_state.interview_questions)

            # ATS Keywords
            if st.button("🔑 Generate ATS Keywords"):

                keyword_prompt = f"""
    Give 30 ATS keywords for {role}.
    Return only bullet points.
    """

                if not st.session_state.ats_keywords:
                    keywords = model.generate_content(keyword_prompt)
                    st.session_state.ats_keywords = keywords.text

                st.subheader("🔑 ATS Keywords")
                st.write(st.session_state.ats_keywords)

            # Project Ideas
            if st.button("💻 Recommend Projects"):

                project_prompt = f"""
    Suggest 5 portfolio projects for {role}.
    Mention project name, difficulty and skills learned.
    """

                if not st.session_state.project_suggestions:
                    projects = model.generate_content(project_prompt)
                    st.session_state.project_suggestions = projects.text

                st.subheader("💻 AI Project Suggestions")
                st.write(st.session_state.project_suggestions)

            # Job Description Analysis
            if job_description.strip():

                if st.button("📋 Analyze Job Description"):

                    jd_prompt = f"""
    Compare this resume with the job description.

    Resume:
    {text}

    Job Description:
    {job_description}
    """

                    if not st.session_state.jd_analysis:
                        jd = model.generate_content(jd_prompt)
                        st.session_state.jd_analysis = jd.text

                    st.subheader("📋 Resume vs Job Description")
                    st.write(st.session_state.jd_analysis)

            generate_pdf(
                role,
                score,
                ats_score,
                resume_match,
                found_skills,
                missing_skills,
                st.session_state.career_advice,
                st.session_state.resume_review,
                st.session_state.cover_letter
            )

            with open("AI_Skill_Report.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download AI Report",
                    pdf_file,
                    file_name="AI_Skill_Report.pdf",
                    mime="application/pdf"
                )