import streamlit as st
from pypdf import PdfReader
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Matcher PRO",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS for Premium Look ---
def inject_custom_css():
    st.markdown("""
    <style>
    /* Main Background & Gradient */
    .stApp {
        background: radial-gradient(circle at top left, #1e1e2f, #0f0f1a);
        color: #e0e0e0;
    }

    /* Glassmorphism Containers */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        # border-radius: 15px;
        # background: rgba(255, 255, 255, 0.05);
        # backdrop-filter: blur(10px);
        # border: 1px solid rgba(255, 255, 255, 0.1);
        # padding: 20px;
        # margin-bottom: 20px;
    }

    /* Target specific blocks for styling */
    .css-1r6p783 {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
    }

    /* Title Styling */
    h1 {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -1px;
        text-align: center;
        margin-bottom: 1.5rem !important;
    }

    h3 {
        color: #2575fc;
        font-weight: 600 !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.6rem 2.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(37, 117, 252, 0.3) !important;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 117, 252, 0.5) !important;
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #2575fc !important;
    }

    /* Divider */
    hr {
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0));
        margin: 2rem 0 !important;
    }

    /* Input area labels */
    .stTextArea label, .stFileUploader label {
        color: #b0b0b0 !important;
        font-weight: 500 !important;
    }

    /* Custom Cards for Advice */
    .advice-card {
        background: rgba(37, 117, 252, 0.1);
        border-left: 5px solid #2575fc;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.8s ease-out forwards;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Helper Functions ---
def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF resume."""
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def analyze_match(resume_text, job_description):
    """
    Enhanced Placeholder for AI analysis.
    In a real app, this would call an LLM API.
    """
    # Logic to simulate different results based on input length or keywords
    desc_keywords = set(job_description.lower().split())
    resume_keywords = set(resume_text.lower().split())
    
    # Very basic intersection simulation
    common = desc_keywords.intersection(resume_keywords)
    percentage = min(95, max(45, len(common) * 2)) 
    
    return {
        "match_percentage": f"{percentage}%",
        "matched_skills": list(common)[:5] if common else ["Communication", "Problem Solving", "Adaptability"],
        "missing_skills": ["Cloud Infrastructure", "CI/CD Pipelines", "System Architecture"],
        "advice": "Your resume highlights strong technical foundations. To stand out, try to include specific metrics like 'improved performance by 30%' or 'reduced latency by 200ms' in your experience section."
    }

def render_circular_gauge(percentage_str):
    percentage = int(percentage_str.replace('%', ''))
    color = "#2575fc" if percentage > 70 else "#f87171"
    
    gauge_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; padding: 20px;">
        <div style="position: relative; width: 200px; height: 200px;">
            <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="#2e2e48" stroke-width="2" />
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="{percentage}, 100" />
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: {color}; font-size: 2.5rem; font-weight: 800;">
                {percentage}%
            </div>
        </div>
    </div>
    """
    st.markdown(gauge_html, unsafe_allow_html=True)

# --- App Layout ---
inject_custom_css()

# Header Section
st.markdown("<h1 class='fade-in'>🎯 AI Resume Matcher PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #b0b0b0;'>Optimize your application with precision AI-driven insights.</p>", unsafe_allow_html=True)

st.divider()

# Inputs Section
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📄 Your Resume")
    uploaded_resume = st.file_uploader("Upload PDF Resume", type=["pdf"], label_visibility="collapsed")
    if uploaded_resume:
        st.success(f"File uploaded: {uploaded_resume.name}")

with col2:
    st.subheader("💼 Job Description")
    job_desc = st.text_area("Paste here", height=150, placeholder="Paste the full job description...", label_visibility="collapsed")

# Action Area
st.write("")
analyze_btn = st.button("🚀 Analyze Alignment")

if analyze_btn:
    if uploaded_resume and job_desc.strip():
        with st.spinner("🧠 Deep Neural Analysis in Progress..."):
            # 1. Read PDF
            resume_text = extract_text_from_pdf(uploaded_resume)
            
            # 2. Analyze
            results = analyze_match(resume_text, job_desc)
            
            st.divider()
            
            # Results Section
            st.markdown("<h2 style='text-align: center;'>Analysis Results</h2>", unsafe_allow_html=True)
            
            # Gauge and Summary
            render_circular_gauge(results["match_percentage"])
            
            res_col1, res_col2 = st.columns(2, gap="medium")
            
            with res_col1:
                st.markdown("### ✅ Key Matches")
                for skill in results["matched_skills"]:
                    st.markdown(f"<div style='background: rgba(37, 252, 117, 0.1); padding: 8px 15px; border-radius: 5px; margin-bottom: 5px; border-left: 3px solid #4ade80;'>{skill}</div>", unsafe_allow_html=True)

            with res_col2:
                st.markdown("### ❌ Missing Gaps")
                for skill in results["missing_skills"]:
                    st.markdown(f"<div style='background: rgba(252, 37, 37, 0.1); padding: 8px 15px; border-radius: 5px; margin-bottom: 5px; border-left: 3px solid #f87171;'>{skill}</div>", unsafe_allow_html=True)

            # Advice Card
            st.markdown(f"""
            <div class='advice-card'>
                <h4 style='margin-top:0; color:#2575fc;'>💡 Strategic Advice</h4>
                <p style='margin-bottom:0;'>{results['advice']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ Please provide both a resume and a job description.")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #555;'>Elevate your career with AI-powered matching.</p>", unsafe_allow_html=True)
