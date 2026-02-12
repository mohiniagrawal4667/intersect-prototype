from skill_list import CORE_SKILLS, OPTIONAL_SKILLS

def match_resume(resume_text):
    matched_core = []
    matched_optional = []

    for skill in CORE_SKILLS:
        if skill in resume_text:
            matched_core.append(skill)

    for skill in OPTIONAL_SKILLS:
        if skill in resume_text:
            matched_optional.append(skill)

    core_score = (len(matched_core) / len(CORE_SKILLS)) * 70
    optional_score = (len(matched_optional) / len(OPTIONAL_SKILLS)) * 30

    total_score = int(core_score + optional_score)

    return {
        "score": total_score,
        "matched_skills": matched_core + matched_optional,
        "missing_skills": list(
            set(CORE_SKILLS + OPTIONAL_SKILLS)
            - set(matched_core + matched_optional)
        )
    }
