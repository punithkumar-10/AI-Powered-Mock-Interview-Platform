import requests
import streamlit as st

# Endpoints for your FastAPI Gemini service (update if deployed differently)
GENERATE_ENDPOINT = "http://localhost:8000/generate"
FEEDBACK_ENDPOINT = "http://localhost:8000/feedback"

# Your provided API key for securing the endpoints
API_KEY = "AIzaSyBgHX0SOzFsv6O4p-gxeoM-FCGTpcuTHmY"
HEADERS = {"X-API-Key": API_KEY}

def call_gemini_api(interview_details):
    """
    Send interview details to Gemini API to generate interview questions.
    """
    try:
        response = requests.post(GENERATE_ENDPOINT, json=interview_details, headers=HEADERS)
        if response.status_code == 200:
            # Expecting JSON with a 'questions' field.
            return response.json().get("questions", [])
        else:
            st.error("Error calling Gemini API: " + response.text)
            return []
    except Exception as e:
        st.error(f"Gemini API call error: {e}")
        return []

def call_gemini_feedback_api(answers_payload):
    """
    Send candidate's answers to Gemini API to retrieve feedback.
    """
    try:
        response = requests.post(FEEDBACK_ENDPOINT, json=answers_payload, headers=HEADERS)
        if response.status_code == 200:
            # Expected to have 'overall_score' and 'detailed_feedback' in the response
            return response.json()
        else:
            st.error("Error retrieving feedback from Gemini API: " + response.text)
            return {}
    except Exception as e:
        st.error(f"Feedback API error: {e}")
        return {}
