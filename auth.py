import streamlit as st
from firebase_config import pb_auth

def signup_user(email, password):
    try:
        pb_auth.create_user_with_email_and_password(email, password)
        st.success("Sign up successful! Please log in.")
    except Exception as e:
        st.error(f"Sign up error: {e}")

def login_user(email, password):
    try:
        user = pb_auth.sign_in_with_email_and_password(email, password)
        st.session_state.user = user  # Store the user in session state
        st.success("Login successful!")
    except Exception as e:
        st.error(f"Login error: {e}")

def logout_user():
    st.session_state.pop("user", None)
    st.success("Logged out successfully!")
