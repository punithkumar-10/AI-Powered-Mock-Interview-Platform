import requests
import streamlit as st

def call_gemini_api(interview_details):
    """Send interview details to Gemini API to generate interview questions."""
    api_url = "https://gemini.api.endpoint/your_endpoint"  # Replace with your endpoint
    try:
        response = requests.post(api_url, json=interview_details)
        if response.status_code == 200:
            return response.json().get("questions", [])
        else:
            st.error("Error calling Gemini API")
            return []
    except Exception as e:
        st.error(f"Gemini API call error: {e}")
        return []

def call_gemini_feedback_api(answers_payload):
    """Send collected answers to Gemini API to retrieve feedback."""
    api_url = "https://gemini.api.endpoint/feedback"  # Replace with your endpoint
    try:
        response = requests.post(api_url, json=answers_payload)
        if response.status_code == 200:
            return response.json()  # Expected to include overall_score and detailed_feedback
        else:
            st.error("Error retrieving feedback from Gemini API")
            return {}
    except Exception as e:
        st.error(f"Feedback API error: {e}")
        return {}
