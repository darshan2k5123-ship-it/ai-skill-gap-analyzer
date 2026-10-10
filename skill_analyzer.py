import re


def detect_skills(text, skills_database):
    found_skills = []

    text_lower = text.lower()

    for skill in skills_database:

        skill_lower = skill.lower().strip()

        # Create a pattern that matches the complete skill
        pattern = r"\b" + re.escape(skill_lower) + r"\b"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills

def find_missing_skills(found_skills, required_skills):
    missing_skills = []

    for skill in required_skills:
        if skill not in found_skills:
            missing_skills.append(skill)

    return missing_skills


def calculate_scores(found_skills, missing_skills, required_skills, text):

    # ------------------------------------------------
    # 1. SKILL MATCH SCORE
    # ------------------------------------------------

    if len(required_skills) > 0:
        matched_skills = len(required_skills) - len(missing_skills)
        skill_match = (matched_skills / len(required_skills)) * 100
    else:
        skill_match = 0

    # ------------------------------------------------
    # 2. ATS SCORE
    # ------------------------------------------------
    # ATS score considers:
    # - Required skill keywords
    # - Important resume sections
    # - Certifications
    # - Projects
    # ------------------------------------------------

    text_lower = text.lower()

    # Required keyword score = 60%
    keyword_score = skill_match * 0.60

    # Resume section score = 25%
    important_sections = [
        "education",
        "experience",
        "internship",
        "projects",
        "technical skills"
    ]

    sections_found = 0

    for section in important_sections:
        if section in text_lower:
            sections_found += 1

    section_score = (sections_found / len(important_sections)) * 25

    # Extra ATS indicators = 15%
    extra_score = 0

    if "certification" in text_lower or "certifications" in text_lower:
        extra_score += 7.5

    if "github" in text_lower or "linkedin" in text_lower:
        extra_score += 7.5

    ats_score = keyword_score + section_score + extra_score

    ats_score = min(ats_score, 100)

    # ------------------------------------------------
    # 3. RESUME MATCH SCORE
    # ------------------------------------------------
    # Measures how well the resume matches the
    # selected role based on skills AND project/
    # experience evidence.
    # ------------------------------------------------

    matched_skill_evidence = 0

    for skill in required_skills:

        if skill in found_skills:

            # Count how many times the skill appears
            # in the resume.
            occurrences = text_lower.count(skill.lower())

            if occurrences >= 2:
                matched_skill_evidence += 1
            elif occurrences == 1:
                matched_skill_evidence += 0.7

    if len(required_skills) > 0:
        evidence_score = (
            matched_skill_evidence / len(required_skills)
        ) * 100
    else:
        evidence_score = 0

    # 70% skill match + 30% evidence
    resume_match = (
        (skill_match * 0.70) +
        (evidence_score * 0.30)
    )

    resume_match = min(resume_match, 100)

    return skill_match, ats_score, resume_match