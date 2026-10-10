from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from xml.sax.saxutils import escape
import re


def clean_ai_text(text):
    """
    Clean Gemini's Markdown-style response
    so it displays properly in a ReportLab PDF.
    """

    if not text:
        return "No information available."

    text = str(text)

    # Remove Markdown heading symbols
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)

    # Convert bold Markdown to normal text
    text = text.replace("**", "")

    # Escape HTML/XML special characters
    text = escape(text)

    # Convert bullet points
    text = text.replace("•", "&#8226;")

    # Convert new lines to PDF line breaks
    text = text.replace("\n", "<br/>")

    return text


def generate_pdf(
    role,
    score,
    ats_score,
    resume_match,
    found_skills,
    missing_skills,
    career_advice,
    resume_review,
    cover_letter
):

    doc = SimpleDocTemplate(
        "AI_Skill_Report.pdf",
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=28,
        textColor=colors.darkblue,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        textColor=colors.darkblue,
        spaceBefore=15,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=10.5,
        leading=16,
        spaceAfter=5
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.grey
    )

    story = []

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    story.append(
        Paragraph(
            "AI Skill Gap Analyzer Report",
            title_style
        )
    )

    story.append(Spacer(1, 10))

    # --------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------

    story.append(
        Paragraph(
            f"<b>Target Role:</b> {escape(str(role))}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Placement Readiness:</b> {score:.0f}%",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {ats_score:.0f}%",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Resume Match:</b> {resume_match:.0f}%",
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # --------------------------------------------------
    # SKILLS FOUND
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Skills Found",
            section_style
        )
    )

    if found_skills:

        for skill in found_skills:
            story.append(
                Paragraph(
                    f"&#8226; {escape(str(skill))}",
                    normal_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No technical skills detected.",
                normal_style
            )
        )

    story.append(Spacer(1, 10))

    # --------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Missing Skills",
            section_style
        )
    )

    if missing_skills:

        for skill in missing_skills:
            story.append(
                Paragraph(
                    f"&#8226; {escape(str(skill))}",
                    normal_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No major missing skills detected.",
                normal_style
            )
        )

    story.append(Spacer(1, 10))

    # --------------------------------------------------
    # REPORT SUMMARY
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Report Summary",
            section_style
        )
    )

    if score >= 80:

        summary = (
            "Excellent placement readiness. "
            "Continue strengthening your skills and prepare for interviews."
        )

    elif score >= 60:

        summary = (
            "Good progress. Focus on the missing skills, "
            "projects and interview preparation."
        )

    else:

        summary = (
            "Focus on learning the missing skills, "
            "building projects and improving your technical preparation."
        )

    story.append(
        Paragraph(
            summary,
            normal_style
        )
    )

    # --------------------------------------------------
    # AI CAREER ADVICE
    # --------------------------------------------------

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "AI Career Advice",
            section_style
        )
    )

    story.append(
        Paragraph(
            clean_ai_text(career_advice),
            normal_style
        )
    )

    # --------------------------------------------------
    # RESUME REVIEW
    # --------------------------------------------------

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Resume Review",
            section_style
        )
    )

    story.append(
        Paragraph(
            clean_ai_text(resume_review),
            normal_style
        )
    )

    # --------------------------------------------------
    # COVER LETTER
    # --------------------------------------------------

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Professional Cover Letter",
            section_style
        )
    )

    story.append(
        Paragraph(
            clean_ai_text(cover_letter),
            normal_style
        )
    )

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "Generated by AI Skill Gap Analyzer | "
            "Built using Python, Streamlit & Gemini AI",
            small_style
        )
    )

    # Build PDF
    doc.build(story)