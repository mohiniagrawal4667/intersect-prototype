from resume_parser import extract_text_from_pdf
from matcher import match_resume

def main():
    resume_text = extract_text_from_pdf("demo_resume.pdf")
    result = match_resume(resume_text)

    print("\n===== INTERSECT ANALYSIS =====")
    print(f"INTERSECT SCORE: {result['score']}%")

    print("\nMatched skills:")
    for skill in result["matched_skills"]:
        print("✓", skill)

    print("\nMissing skills:")
    for skill in result["missing_skills"]:
        print("-", skill)

if __name__ == "__main__":
    main()
