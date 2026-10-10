def career_prompt(role, found_skills, missing_skills, score):
    return f"""
You are an expert AI Career Mentor.

Role:
{role}

Skills Found:
{', '.join(found_skills)}

Missing Skills:
{', '.join(missing_skills)}

Readiness Score:
{score:.0f}%

Provide:
- Career Summary
- Missing Skills
- Best Projects
- Free Learning Resources
- 30-Day Plan
- Motivation

Keep the response under 200 words.
Use simple English.
"""

def resume_review_prompt(role, text, found_skills, missing_skills, ats_score):
    return f"""
You are an expert Resume Reviewer.

Resume:
{text}

Target Role:
{role}

Detected Skills:
{', '.join(found_skills)}

Missing Skills:
{', '.join(missing_skills)}

ATS Score:
{ats_score:.0f}%

Provide:
- Resume Rating (/10)
- Strengths
- Areas to Improve
- ATS Keywords
- Final Suggestion

Keep the response under 200 words.
"""