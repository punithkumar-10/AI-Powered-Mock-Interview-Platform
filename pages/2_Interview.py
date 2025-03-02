import streamlit as st
import io, base64
from gtts import gTTS
from utils import record_audio, generate_feedback

st.set_page_config(
    page_title="Interview Session | AI Mock Interview", 
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
    .interview-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .question-box {
        background: rgba(44, 62, 80, 0.6);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #ffcb05;
    }
    .audio-controls {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
    }
    .audio-button {
        background: rgba(255, 255, 255, 0.15);
        border: none;
        color: white;
        padding: 8px 15px;
        border-radius: 6px;
        cursor: pointer;
        transition: background 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    .audio-button:hover {
        background: rgba(255, 255, 255, 0.25);
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
        width: 100%;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 7px 20px rgba(255, 203, 5, 0.4);
    }
    h1, h2 {
        text-align: center;
        margin-bottom: 30px;
        background: linear-gradient(90deg, #ffcb05, #ff9d00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .feedback-container {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 25px;
        margin-top: 30px;
    }
    .progress-bar-container {
        width: 100%;
        height: 10px;
        background-color: rgba(255,255,255,0.1);
        border-radius: 5px;
        margin: 20px 0;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #ffcb05, #ff9d00);
        border-radius: 5px;
        transition: width 0.5s ease;
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
        st.switch_page("pages/1_Candidate_Details.py")
with col3:
    if st.button("🎙️ Interview", key="interview_nav"):
        st.rerun()

# Center the title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1>AI Interview Session</h1>", unsafe_allow_html=True)

# Enable camera toggle (if available)
if "camera_enabled" not in st.session_state:
    st.session_state["camera_enabled"] = False

# Initialize questions list if not in session state (for testing/debugging)
if "questions" not in st.session_state:
    st.session_state["questions"] = []
if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0
if "responses" not in st.session_state:
    st.session_state["responses"] = []

st.markdown("<div class='interview-container'>", unsafe_allow_html=True)

camera_col, _, controls_col = st.columns([1, 0.1, 2])

with camera_col:
    camera_enabled = st.toggle("Enable Camera", value=st.session_state["camera_enabled"])
    st.session_state["camera_enabled"] = camera_enabled

    if camera_enabled:
        st.camera_input("Camera Feed", key="interview_camera")

with controls_col:
    # Ensure interview questions exist
    if not st.session_state["questions"]:
        st.error("No interview questions found. Please fill out the Candidate Details form first.")
        if st.button("Go to Candidate Details", use_container_width=True):
            st.switch_page("pages/1_Candidate_Details.py")
    else:
        current = st.session_state.get("current_question", 0)
        questions = st.session_state["questions"]
        total_questions = len(questions)
        
        # Progress bar
        progress_percentage = (current / total_questions) * 100 if total_questions > 0 else 0
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span>Progress</span>
            <span>{current}/{total_questions} Questions</span>
        </div>
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: {progress_percentage}%;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        if current < len(questions):
            current_question = questions[current]
            st.markdown(f"""
            <div class="question-box">
                <h4>Question {current + 1}:</h4>
                <p>{current_question}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Buttons for text-to-speech and audio recording
            cols = st.columns(2)
            if cols[0].button("🔊 Text to Speech", key=f"read_{current}"):
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
            if cols[1].button("🎙️ Record Answer", key=f"record_{current}"):
                with st.spinner("Recording your answer..."):
                    rec_text = record_audio()
                    existing_text = st.session_state.get(f"q_{current}_recorded", "")
                    st.session_state[f"q_{current}_recorded"] = existing_text + " " + rec_text
            
            default_answer = st.session_state.get(f"q_{current}_recorded", "")
            answer = st.text_area("Your answer:", key=f"q_{current}",
                                    value=default_answer,
                                    placeholder="Type your answer or use the Record button above...",
                                    height=150)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Submit Answer", key=f"submit_{current}"):
                if len(answer.split()) < 5:  # Changed from 30 to 5 for easier testing
                    st.warning("Please provide a more detailed answer (at least 5 words).")
                else:
                    if "responses" not in st.session_state:
                        st.session_state["responses"] = []
                    st.session_state["responses"].append({
                        "question": current_question,
                        "answer": answer
                    })
                    st.session_state["current_question"] = current + 1
                    st.experimental_rerun()
        else:
            st.success("🎉 Congratulations! You have completed all the interview questions.")
            
            # Generate interview feedback button
            if st.button("Generate Interview Feedback", key="gen_feedback", use_container_width=True):
                with st.spinner("Analyzing your responses and generating feedback..."):
                    # Construct transcript
                    transcript = (
                        f"Candidate Name: {st.session_state.get('name', 'N/A')}\n"
                        f"Job Role: {st.session_state.get('job_role', 'N/A')}\n"
                        f"Job Description: {st.session_state.get('job_description', 'N/A')}\n"
                        f"Interview Type: {st.session_state.get('interview_type', 'N/A')}\n"
                        f"Years of Experience: {st.session_state.get('years_experience', 'N/A')}\n\n"
                        "Interview Transcript:\n"
                    )
                    for qa in st.session_state.get("responses", []):
                        transcript += f"Q: {qa['question']}\nA: {qa['answer']}\n\n"
                    
                    # Generate feedback using the helper function
                    feedback = generate_feedback(transcript)
                    
                    st.markdown("<div class='feedback-container'>", unsafe_allow_html=True)
                    st.markdown("<h2>Interview Feedback</h2>", unsafe_allow_html=True)
                    st.markdown(feedback, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Option to start over - placed outside the feedback generation to avoid nesting
            st.markdown("<br>", unsafe_allow_html=True)
            
            button_cols = st.columns(2)
            with button_cols[0]:
                if st.button("Try Another Interview", key="try_another", use_container_width=True):
                    st.switch_page("pages/1_Candidate_Details.py")
            with button_cols[1]:
                if st.button("Return to Home", key="return_home", use_container_width=True):
                    st.switch_page("main.py")

st.markdown("</div>", unsafe_allow_html=True)