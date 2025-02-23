import streamlit as st
from gemini_api import call_gemini_api, call_gemini_feedback_api
from firebase_config import fs_client
from firebase_admin import firestore

def show_interview():
    st.title("Mock Interview")
    if not st.session_state.get("user"):
        st.error("Please log in to access mock interviews.")
        return

    tab1, tab2 = st.tabs(["New Interview", "Interview History"])

    with tab1:
        st.header("Start a New Mock Interview")
        with st.form("interview_form"):
            job_role = st.text_input("Job Role")
            interview_type = st.selectbox("Type of Interview", ["Technical", "Behavioural"])
            job_description = st.text_area("Job Description")
            additional_details = st.text_area("Additional Details")
            years_experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
            submitted = st.form_submit_button("Submit")
            if submitted:
                interview_details = {
                    "job_role": job_role,
                    "interview_type": interview_type,
                    "job_description": job_description,
                    "additional_details": additional_details,
                    "years_experience": years_experience
                }
                st.info("Generating interview questions...")
                questions = call_gemini_api(interview_details)
                if questions:
                    st.session_state.questions = questions
                    st.session_state.current_q = 0
                    st.session_state.answers = []
                    st.session_state.interview_details = interview_details
                    st.experimental_rerun()

        if "questions" in st.session_state:
            st.subheader("Interview in Progress")
            questions = st.session_state.questions
            current_q = st.session_state.current_q
            if current_q < len(questions):
                st.write(f"**Question {current_q+1}:** {questions[current_q]}")
                answer = st.text_area("Your Answer:", key=f"answer_{current_q}")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("Start"):
                        st.info("Starting recording... [Integration required]")
                with col2:
                    if st.button("Pause"):
                        st.info("Paused recording... [Integration required]")
                with col3:
                    if st.button("Restart"):
                        st.info("Restarting recording... [Integration required]")
                with col4:
                    if st.button("Save Answer"):
                        st.session_state.answers.append(answer)
                        st.success("Answer saved!")
                if st.button("Next Question"):
                    if len(st.session_state.answers) <= current_q:
                        st.session_state.answers.append(answer)
                    st.session_state.current_q += 1
                    st.experimental_rerun()
            else:
                st.success("Interview completed!")
                if st.button("Submit Interview"):
                    payload = {
                        "interview_details": st.session_state.interview_details,
                        "answers": st.session_state.answers
                    }
                    feedback = call_gemini_feedback_api(payload)
                    overall_score = feedback.get("overall_score", 0)
                    st.markdown(f"### Overall Score: {overall_score}/10")
                    st.write("Detailed Feedback:")
                    detailed_feedback = feedback.get("detailed_feedback", {})
                    for idx, fb in detailed_feedback.items():
                        st.write(f"**Question {int(idx)+1}:** {fb}")
                    user_email = st.session_state.user['email']
                    doc_ref = fs_client.collection("interviews").document(user_email).collection("records").document()
                    doc_ref.set({
                        "interview_details": st.session_state.interview_details,
                        "questions": st.session_state.questions,
                        "answers": st.session_state.answers,
                        "feedback": feedback,
                        "timestamp": firestore.SERVER_TIMESTAMP
                    })
                    st.success("Interview submitted and saved!")
                    for key in ["questions", "current_q", "answers", "interview_details"]:
                        st.session_state.pop(key, None)

    with tab2:
        st.header("Your Interview History")
        user_email = st.session_state.user['email']
        interviews_ref = fs_client.collection("interviews").document(user_email).collection("records")
        docs = interviews_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            data = doc.to_dict()
            with st.expander(f"Interview on {data.get('timestamp').strftime('%Y-%m-%d %H:%M:%S') if data.get('timestamp') else 'Unknown Date'}"):
                st.write("**Interview Details:**", data.get("interview_details", {}))
                st.write("**Questions:**", data.get("questions", []))
                st.write("**Your Answers:**", data.get("answers", []))
                feedback = data.get("feedback", {})
                st.write("**Overall Score:**", feedback.get("overall_score", "N/A"))
                st.write("**Detailed Feedback:**", feedback.get("detailed_feedback", {}))
