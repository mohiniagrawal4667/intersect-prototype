import streamlit as st
from matcher import match_resume
from resume_parser import extract_text_from_pdf

st.set_page_config(
    page_title="Intersect",
    page_icon="🧭",
    layout="wide"
)

# ---------------- LANDING PAGE ----------------
if "user_type" not in st.session_state:
    st.session_state.user_type = None

if st.session_state.user_type is None:
    st.title("🧭 INTERSECT")
    st.subheader("Making job-readiness visible — before the interview")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎓 I am a Student", use_container_width=True):
            st.session_state.user_type = "student"

    with col2:
        if st.button("🧑‍💼 I am a Recruiter", use_container_width=True):
            st.session_state.user_type = "recruiter"

    st.stop()

# ---------------- RECRUITER PLACEHOLDER ----------------
if st.session_state.user_type == "recruiter":
    st.title("Recruiter Dashboard (Preview)")
    st.info("Recruiter matching & JD comparison coming next.")
    st.stop()

# ---------------- STUDENT DASHBOARD ----------------
st.title("🧭 INTERSECT")
st.caption("Upload your resume to see where you stand — honestly.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    resume_text = extract_text_from_pdf("temp_resume.pdf")
    result = match_resume(resume_text)

    score = result["score"]
    matched = result["matched_skills"]
    missing = result["missing_skills"]

    st.markdown("---")

    # -------- SCORE VISUAL --------
    st.subheader("Readiness Score")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.metric("INTERSECT SCORE", f"{score}%")

    st.markdown("---")

    # -------- SKILLS SECTION --------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Skills You Already Have")
        for skill in matched:
            st.success(skill)

    with col2:
        st.subheader("🚧 Skills To Work On")
        for skill in missing:
            st.warning(skill)

    # -------- SUMMARY INSIGHT --------
    st.markdown("---")
    st.subheader("📌 Readiness Summary")

    if score >= 80:
        st.success("You're close to being job-ready. Focus on polishing depth.")
    elif score >= 60:
        st.info("You have strong fundamentals. Target missing skills strategically.")
    else:
        st.warning("Focus on core skills first. Direction matters more than speed.")

    st.markdown("### 🎯 Next Best Actions")
    for skill in missing[:3]:
        st.write(f"- Start learning **{skill}**")

