from skill_list import SKILLS

def match_resume(resume_text):
    resume_text = resume_text.lower()

    matched = []
    missing = []

    for priority, skills in SKILLS.items():
        for skill in skills:
            if skill in resume_text:
                matched.append(skill)
            else:
                missing.append({
                    "skill": skill,
                    "priority": priority
                })

    total = len(matched) + len(missing)
    score = int((len(matched) / total) * 100) if total else 0

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }

