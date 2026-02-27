import streamlit as st
import pdfplumber

from matcher import match_resume
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile

def generate_premium_pdf(score, matched, missing):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=A4)

    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, 800, "INTERSECT – Career Readiness Report")

    c.setFont("Helvetica", 14)
    c.drawString(50, 760, f"Overall Readiness Score: {score}%")

    y = 720
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Skills You Already Have")
    y -= 25

    c.setFont("Helvetica", 12)
    for skill in matched:
        c.drawString(60, y, f"✔ {skill.title()}")
        y -= 18

    y -= 20
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Skills To Focus On (Recruiter Priority)")
    y -= 25

    c.setFont("Helvetica", 12)
    for item in missing:
        c.drawString(
            60,
            y,
            f"- {item['skill'].title()} ({item['priority']})"
        )
        y -= 18

    c.save()
    return tmp.name


# ---------- PAGE SETUP ----------
st.set_page_config(page_title="INTERSECT", layout="wide")

st.title("🧭 INTERSECT – Career Readiness Analyzer")
st.caption("Not motivation. Not guessing. Real skill alignment.")

# ---------- INIT SAFE DEFAULTS ----------
score = None
matched = []
missing = []
summary = []

# ---------- UPLOAD ----------
uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

if uploaded_file:
   resume_text = ""

if uploaded_file is not None:
    import pdfplumber

    resume_text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text.lower()

    # 🔥 THIS LINE WAS MISSING / MISPLACED
    result = match_resume(resume_text)

    # ✅ NOW result EXISTS
    score = result["score"]
    matched = result["matched"]
    missing = result["missing"]

# ---------- CIRCULAR SCORE ----------
st.divider()
st.subheader("Your INTERSECT Readiness")

if score is not None:
    progress = int(score * 5.65)

    st.markdown(
        f"""
        <div style="display:flex;justify-content:center;">
        <svg width="240" height="240">
            <circle cx="120" cy="120" r="95"
                stroke="#1f2937"
                stroke-width="18"
                fill="none"/>
            <circle cx="120" cy="120" r="95"
                stroke="#22c55e"
                stroke-width="18"
                fill="none"
                stroke-dasharray="{progress} 565"
                stroke-linecap="round"
                transform="rotate(-90 120 120)"/>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
                font-size="40" fill="white">{score}%</text>
            <text x="50%" y="65%" dominant-baseline="middle" text-anchor="middle"
                font-size="14" fill="#9ca3af">Readiness</text>
        </svg>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("Upload a resume to see your readiness score")
    st.divider()
st.subheader("📊 Skill Readiness Summary (What Actually Matters)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✅ Skills You Already Have")
    for skill in matched:
        st.markdown(
            f"""
            <div style="
                padding:12px;
                margin-bottom:10px;
                background:#123b2a;
                border-left:6px solid #2ecc71;
                border-radius:8px;
                font-size:20px;
                font-weight:600;">
                {skill.title()}
            </div>
            """,
            unsafe_allow_html=True
        )

with col2:
    st.markdown("### 🚧 Skills You Need To Work On")
    for item in missing:
        priority = item["priority"]
        skill = item["skill"]

        size = "24px" if priority in ["Critical", "High"] else "18px"
        color = "#e74c3c" if priority == "Critical" else "#f1c40f"

        st.markdown(
            f"""
            <div style="
                padding:14px;
                margin-bottom:12px;
                background:#3b2a12;
                border-left:6px solid {color};
                border-radius:8px;
                font-size:{size};
                font-weight:700;">
                {skill.title()}
                <span style="float:right; font-size:14px;">{priority}</span>
            </div>
            """,
            unsafe_allow_html=True
        )



# ---------- SUMMARY TABLE ----------
if score is not None:
    st.divider()
    st.subheader("📊 Skill Readiness Summary (What Actually Matters)")

    st.markdown("""
    <style>
    .critical {color:#ef4444;font-size:26px;font-weight:700}
    .high {color:#f97316;font-size:22px;font-weight:600}
    .medium {color:#eab308;font-size:18px}
    .low {color:#9ca3af;font-size:16px}
    </style>
    """, unsafe_allow_html=True)

    for item in summary:
        cls = item["priority"].lower()
        st.markdown(
            f"<div class='{cls}'>• {item['skill'].title()} ({item['priority']} Priority)</div>",
            unsafe_allow_html=True
        )

# ---------- PDF REPORT ----------
def generate_pdf(score, summary):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=A4)

    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, 800, "INTERSECT – Readiness Report")

    c.setFont("Helvetica", 14)
    c.drawString(50, 760, f"Overall Readiness Score: {score}%")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 720, "Skills To Improve (Recruiter View)")

    y = 690
    c.setFont("Helvetica", 12)

    for item in summary:
        c.drawString(60, y, f"- {item['skill'].title()} [{item['priority']}]")
        y -= 18
        if y < 50:
            c.showPage()
            y = 750

    c.save()
    return tmp.name

if st.button("📄 Download Detailed Readiness Report"):
    pdf_path = generate_premium_pdf(score, matched, missing)
    with open(pdf_path, "rb") as f:
        st.download_button(
            "⬇ Download PDF",
            f,
            file_name="Intersect_Readiness_Report.pdf"
        )