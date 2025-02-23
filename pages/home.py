import streamlit as st

def show_home():
    st.title("AI-Powered Mock Interview Platform")
    st.write("Welcome to our next-generation interview preparation tool powered by AI.")
    st.write("""
        This platform allows you to:
        - Create and take mock interviews tailored to your job role.
        - Receive real-time feedback from an AI interview panel.
        - Connect with a community of peers.
    """)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up / Login"):
            st.session_state.page = "Account"
    with col2:
        if st.button("Take a Mock Interview"):
            st.session_state.page = "Take Mock Interview"
