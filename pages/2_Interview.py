import streamlit as st
import io, base64
from gtts import gTTS
from utils import record_audio, generate_feedback

st.set_page_config(page_title="Interview")

st.title("Interview")

# Enable camera toggle (if available)
if "camera_enabled" not in st.session_state:
    st.session_state["camera_enabled"] = False

camera_enabled = st.checkbox("Enable Camera", value=st.session_state["camera_enabled"])
st.session_state["camera_enabled"] = camera_enabled

if camera_enabled:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.camera_input("Interview Camera Feed", key="interview_camera")

# Ensure interview questions exist
if "questions" not in st.session_state:
    st.error("No interview questions found. Please fill out the Candidate Details form first.")
else:
    current = st.session_state.get("current_question", 0)
    questions = st.session_state["questions"]
    
    if current < len(questions):
        current_question = questions[current]
        st.subheader(f"Question {current + 1}:")
        st.write(current_question)
        
        # Buttons for text-to-speech and audio recording
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
                                placeholder="You can speak or type your answer")
        if st.button("Submit Answer", key=f"submit_{current}"):
            if len(answer.split()) < 30:
                st.warning("Please answer with at least 30 words.")
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
        st.success("You have completed all the interview questions.")
        if st.button("Submit Interview for Feedback"):
            with st.spinner("Generating feedback..."):
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
                st.header("Interview Feedback")
                st.write(feedback)
