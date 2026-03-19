import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
import json
from PIL import Image

# --- Helper Functions ---
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def suggest_job_roles(resume_content, api_key, is_image=False):
    """
    Acts as a career advisor. Analyzes the resume and suggests suitable job titles.
    """
    genai.configure(api_key=api_key)
    # Using gemini-2.5-flash for speed and multimodal capabilities
    model = genai.GenerativeModel('gemini-2.5-flash') 

    # --- UPDATED PROMPT: The Career Advisor Instruction ---
    prompt_instructions = """
    You are a Senior Career Advisor and IT Recruiter with 20 years of experience.
    Analyze the provided resume (it could be text or an image).

    Based STRICTLY on the skills, experience, and education found in the resume, 
    perform the following tasks:
    1. Identify the candidate's core technical and soft skills.
    2. Suggest the top 3-4 professional job titles this candidate is qualified to apply for right now.
    3. For each suggested title, provide a brief 'Reason Why' based on their resume.

    Respond ONLY with a valid JSON object in the exact format below. Do not include markdown formatting like ```json.
    {
        "candidate_summary": "A short, 2-sentence summary of the candidate's professional profile.",
        "top_skills_found": ["skill 1", "skill 2", "skill 3"],
        "recommended_roles": [
            {
                "job_title": "Example Job Title 1",
                "reason_why": "Brief explanation connecting resume experience to this role."
            },
            {
                "job_title": "Example Job Title 2",
                "reason_why": "Brief explanation connecting resume experience to this role."
            }
        ]
    }
    """

    try:
        if is_image:
            response = model.generate_content([prompt_instructions, resume_content])
        else:
            full_prompt = prompt_instructions + f"\n\nResume Text:\n{resume_content}"
            response = model.generate_content(full_prompt)
        
        # Clean up potential AI formatting errors
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        elif response_text.startswith("```"):
            response_text = response_text[3:-3]
            
        return json.loads(response_text)
    
    except Exception as e:
        return {"error": f"AI Analysis failed. Error: {str(e)}"}

# --- UI Setup ---
st.set_page_config(page_title="AI Career Navigator", page_icon="🚀", layout="centered")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("Get your free key from [Google AI Studio](https://aistudio.google.com/).")

st.title("🚀 AI Career Navigator")
st.markdown("Not sure what jobs to apply for? Upload or take a picture of your resume, and our AI advisor will suggest the best-fitting job roles for you.")
st.divider()

# --- Inputs ---
st.subheader("1. Provide Your Resume")

resume_data = None
is_image_format = False

# Layout for input methods
input_method = st.radio("Choose input method:", ["📁 Upload File (PDF/JPG/PNG)", "📷 Use Camera"], horizontal=True)

if input_method == "📁 Upload File (PDF/JPG/PNG)":
    uploaded_file = st.file_uploader("Upload resume", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            resume_data = extract_text_from_pdf(uploaded_file)
            is_image_format = False
            st.info("✅ PDF loaded successfully.")
        else:
            resume_data = Image.open(uploaded_file)
            is_image_format = True
            st.image(resume_data, caption="Uploaded Resume", use_container_width=True)

elif input_method == "📷 Use Camera":
    camera_photo = st.camera_input("Snap a photo of your printed resume")
    if camera_photo:
        resume_data = Image.open(camera_photo)
        is_image_format = True
        st.success("📸 Photo captured successfully.")

# --- Action Button ---
st.write("") # Spacer
if st.button("Get Career Advice", type="primary", use_container_width=True):
    
    # 1. Validate Inputs
    if not api_key_input:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar.")
    elif not resume_data:
        st.error("⚠️ Please provide your resume (upload a file or take a photo).")
    else:
        # 2. Show a loading spinner during API Call
        with st.spinner("Analyzing your profile and finding the perfect roles..."):
            
            result = suggest_job_roles(
                resume_content=resume_data, 
                api_key=api_key_input, 
                is_image=is_image_format
            )
            
            # 3. Handle and Display the Results
            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Analysis Complete!")
                st.divider()
                
                # --- Display Profile Summary ---
                st.subheader("👤 Professional Profile")
                st.info(result.get("candidate_summary", "No summary provided."))
                
                # --- Display Top Skills ---
                st.subheader("💡 Top Skills Identified")
                skills = result.get("top_skills_found", [])
                if skills:
                    # Creating a horizontal flow of skills using columns or generic text
                    st.write(" • ".join(skills))
                else:
                    st.write("No specific skills identified.")
                
                st.divider()
                
                # --- Display Recommended Roles ---
                st.subheader("🎯 Recommended Job Titles")
                roles = result.get("recommended_roles", [])
                
                if roles:
                    for idx, role in enumerate(roles):
                        # Use an expander for a clean accordion-style UI
                        with st.expander(f"**{idx + 1}. {role.get('job_title', 'Unknown Role')}**", expanded=True):
                            st.write(f"**Why you are a fit:** {role.get('reason_why', 'No reason provided.')}")
                else:
                    st.warning("Could not determine specific job roles for this resume.")
