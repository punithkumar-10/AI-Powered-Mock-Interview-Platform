import streamlit as st
from auth import signup_user, login_user, logout_user

def show_account():
    st.title("Account")
    tab1, tab2 = st.tabs(["Sign Up", "Login"])
    
    with tab1:
        st.header("Create an Account")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            signup_user(email, password)
    
    with tab2:
        st.header("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            login_user(email, password)
    
    if st.session_state.get("user"):
        st.write("Logged in as:", st.session_state.user['email'])
        if st.button("Logout"):
            logout_user()
