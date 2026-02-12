from skill_list import SKILLS

def match_resume(resume_text):
    matched = []
    missing = []

    for skill in SKILLS:
        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(SKILLS)) * 100)

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }
