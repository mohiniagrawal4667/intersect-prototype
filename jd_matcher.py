def extract_skills_from_jd(jd_text, skill_list):
    jd_text = jd_text.lower()
    required_skills = []

    for skill in skill_list:
        if skill in jd_text:
            required_skills.append(skill)

    return required_skills
