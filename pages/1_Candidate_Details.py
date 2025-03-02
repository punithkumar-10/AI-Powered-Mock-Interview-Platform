import streamlit as st
from utils import generate_interview_questions

st.set_page_config(page_title="Candidate Details")

st.title("Candidate Details")
st.markdown("Please fill in your details to begin your personalized mock interview.")

with st.form("candidate_details_form"):
    name = st.text_input("Enter your name:")
    job_role = st.text_input("Enter the job role you are interviewing for:")
    job_description = st.text_area("Enter the job description for this role:")
    interview_type = st.selectbox("Select the interview type:", ["Technical", "Behavioural", "Other"])
    years_experience = st.number_input("Enter your years of experience:", min_value=0, value=0, step=1)
    candidate_submit = st.form_submit_button("Submit")

if candidate_submit:
    if not job_role or not job_description:
        st.error("Please enter both the job role and job description.")
    else:
        with st.spinner("Generating interview questions..."):
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
                st.success("Interview questions generated successfully!")
                st.markdown("Now, navigate to the **Interview** page from the sidebar to start your mock interview.")
            else:
                st.error("Failed to generate interview questions. Please try again.")
