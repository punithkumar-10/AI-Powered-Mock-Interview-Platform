import os
import io
import base64
import streamlit as st
from gtts import gTTS
import speech_recognition as sr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Set your API key securely (you can retrieve this from st.secrets in production)
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Initialize session state variables for camera
if "camera_enabled" not in st.session_state:
    st.session_state["camera_enabled"] = False

st.title("AI Mock Interview Platform")

# --- Candidate Details Form ---
with st.form("candidate_details_form"):
    st.header("Candidate Details")
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
        with st.spinner("Submitted! We are generating questions for you..."):
            st.session_state["name"] = name
            st.session_state["job_role"] = job_role
            st.session_state["job_description"] = job_description
            st.session_state["interview_type"] = interview_type
            st.session_state["years_experience"] = years_experience

            prompt_template = """
You are an expert interviewer. Based on the following job role, job description, and interview type, generate 5 tailored interview questions that assess a candidate's fit for the role.

Job Role: {job_role}
Job Description: {job_description}
Interview Type: {interview_type}

Provide the questions as a numbered list.
"""
            prompt = PromptTemplate(
                input_variables=["job_role", "job_description", "interview_type"],
                template=prompt_template
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            questions_output = chain.run(
                job_role=job_role,
                job_description=job_description,
                interview_type=interview_type
            )
            questions = [line.strip() for line in questions_output.split("\n")
                         if line.strip() and line.strip()[0].isdigit()]
            if not questions:
                st.error("Failed to generate interview questions. Please try again.")
            else:
                st.session_state["questions"] = questions
                st.session_state["current_question"] = 0
                st.session_state["responses"] = []
                st.session_state["camera_enabled"] = True
                st.success("Interview questions generated. Please proceed to the interview section.")

# --- Audio Recording Function ---
def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Recording... Please speak now.")
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    try:
        text = r.recognize_google(audio)
        st.success("Audio recognized successfully!")
        return text
    except Exception as e:
        st.error(f"Error recognizing speech: {e}")
        return ""

# --- Interview Section ---
if "questions" in st.session_state:
    st.header("Interview")
    
    camera_enabled = st.checkbox("Enable Camera", value=st.session_state["camera_enabled"])
    st.session_state["camera_enabled"] = camera_enabled
    
    if st.session_state["camera_enabled"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.camera_input("Interview Camera Feed", key="interview_camera")
    
    current = st.session_state["current_question"]
    if current < len(st.session_state["questions"]):
        current_question = st.session_state["questions"][current]
        st.subheader(f"Question {current + 1}:")
        st.write(current_question)
        
        cols = st.columns(2)
        if cols[0].button("🔊", key=f"read_{current}"):
            tts = gTTS(text=current_question, lang="en")
            audio_file = io.BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
            st.markdown(
                f"""
                <audio controls autoplay>
                  <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                Your browser does not support the audio element.
                </audio>
                """,
                unsafe_allow_html=True
            )
        if cols[1].button("🎙️", key=f"record_{current}"):
            rec_text = record_audio()
            existing_text = st.session_state.get(f"q_{current}_recorded", "")
            st.session_state[f"q_{current}_recorded"] = existing_text + " " + rec_text
        
        default_answer = st.session_state.get(f"q_{current}_recorded", "")
        answer = st.text_area("Your answer:", key=f"q_{current}",
                                value=default_answer,
                                placeholder="You can speak to answer or type")
        if st.button("Submit Answer", key=f"submit_{current}"):
            if len(answer.split()) < 30:
                st.warning("Please answer with at least 30 words.")
            else:
                st.session_state["responses"].append({
                    "question": current_question,
                    "answer": answer
                })
                st.session_state["current_question"] += 1
                if hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
    else:
        st.session_state["camera_enabled"] = False
        st.success("You have completed all the interview questions.")
        if st.button("Submit Interview for Feedback"):
            with st.spinner("Please wait for feedback..."):
                transcript = (
                    f"Candidate Name: {st.session_state['name']}\n"
                    f"Job Role: {st.session_state['job_role']}\n"
                    f"Job Description: {st.session_state['job_description']}\n"
                    f"Interview Type: {st.session_state['interview_type']}\n"
                    f"Years of Experience: {st.session_state['years_experience']}\n\n"
                    "Interview Transcript:\n"
                )
                for qa in st.session_state["responses"]:
                    transcript += f"Q: {qa['question']}\nA: {qa['answer']}\n\n"
                
                feedback_prompt = """
You are an expert interviewer. Please review the following interview transcript and provide detailed feedback including:
- Strengths in the candidate's responses,
- Areas for improvement,
- Overall suggestions for interview improvement,
- An overall score out of 10.

Interview Transcript:
{transcript}

Provide your response in a clear, structured format.
"""
                feedback_template = PromptTemplate(
                    input_variables=["transcript"],
                    template=feedback_prompt
                )
                feedback_chain = LLMChain(llm=llm, prompt=feedback_template)
                try:
                    feedback = feedback_chain.run(transcript=transcript)
                    st.header("Interview Feedback")
                    st.write(feedback)
                except Exception as e:
                    st.error("An error occurred while generating feedback: " + str(e))
