import streamlit as st
from utils import generate_interview_questions

st.set_page_config(
    page_title="Candidate Details | AI Mock Interview", 
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
    body {
        background: linear-gradient(135deg, #2C3E50, #4CA1AF);
        font-family: 'Roboto', sans-serif;
        color: #fefefe;
    }
    .form-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .stButton button {
        background: linear-gradient(90deg, #ffcb05, #ff9d00);
        color: #2C3E50;
        font-weight: bold;
        border: none;
        padding: 10px 25px;
        border-radius: 8px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 203, 5, 0.3);
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 7px 20px rgba(255, 203, 5, 0.4);
    }
    h1 {
        text-align: center;
        margin-bottom: 30px;
        background: linear-gradient(90deg, #ffcb05, #ff9d00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .description {
        text-align: center;
        margin-bottom: 30px;
        font-size: 1.2rem;
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation links at the top
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🏠 Home", key="home_nav"):
        st.switch_page("main.py")
with col2:
    if st.button("📋 Candidate Details", key="details_nav"):
        st.rerun()
with col3:
    if st.button("🎙️ Interview", key="interview_nav"):
        st.switch_page("pages/2_Interview.py")

# Center the title and description
st.markdown("<h1>Candidate Details</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Please fill in your details to begin your personalized mock interview.</p>", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "job_role" not in st.session_state:
    st.session_state["job_role"] = ""
if "job_description" not in st.session_state:
    st.session_state["job_description"] = ""
if "interview_type" not in st.session_state:
    st.session_state["interview_type"] = "Technical"
if "years_experience" not in st.session_state:
    st.session_state["years_experience"] = 2

with st.form("candidate_details_form"):
    name = st.text_input("Enter your name:", 
                         placeholder="e.g., John Smith",
                         value=st.session_state["name"])
    
    job_role = st.text_input("Enter the job role you are interviewing for:", 
                             placeholder="e.g., Software Engineer, Product Manager",
                             value=st.session_state["job_role"])
    
    job_description = st.text_area("Enter the job description for this role:",
                                 placeholder="Paste the job description here...",
                                 value=st.session_state["job_description"])
    
    col1, col2 = st.columns(2)
    with col1:
        interview_type = st.selectbox("Select the interview type:", 
                                     ["Technical", "Behavioural", "System Design", "Leadership", "Problem Solving"],
                                     index=["Technical", "Behavioural", "System Design", "Leadership", "Problem Solving"].index(st.session_state["interview_type"]))
    with col2:
        years_experience = st.number_input("Years of experience:", 
                                          min_value=0, value=st.session_state["years_experience"], step=1)
    
    st.markdown("<br>", unsafe_allow_html=True)
    candidate_submit = st.form_submit_button("Generate Interview Questions")

if candidate_submit:
    if not job_role or not job_description:
        st.error("Please enter both the job role and job description.")
    else:
        with st.spinner("Generating personalized interview questions..."):
            # Save candidate details in session state
            st.session_state["name"] = name
            st.session_state["job_role"] = job_role
            st.session_state["job_description"] = job_description
            st.session_state["interview_type"] = interview_type
            st.session_state["years_experience"] = years_experience
            
            # Generate interview questions using the LLM helper function
            questions = generate_interview_questions(job_role, job_description, interview_type)
            if questions:
                st.session_state["questions"] = questions
                st.session_state["current_question"] = 0
                st.session_state["responses"] = []
                
                # Success message with animated checkmark
                st.markdown("""
                <div style="text-align:center; margin-top:30px;">
                    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M5 13L9 17L19 7" stroke="#4CAF50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <animate attributeName="stroke-dasharray" from="0,100" to="100,100" dur="1s" fill="freeze" />
                        </path>
                    </svg>
                    <h3 style="color:#4CAF50;">Interview questions generated successfully!</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Proceed to interview button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Proceed to Interview", use_container_width=True):
                        st.switch_page("pages/2_Interview.py")
            else:
                st.error("Failed to generate interview questions. Please try again.")