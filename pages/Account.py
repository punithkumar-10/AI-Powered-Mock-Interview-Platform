import streamlit as st
from utils.firebase import firebase_signup, firebase_login, firebase_logout

st.title("Account Management")

option = st.selectbox("Select Action", ["Sign Up", "Login", "Logout"])

if option == "Sign Up":
    st.subheader("Create an Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        result = firebase_signup(email, password)
        st.success(f"Signed up as {email}" if result else "Sign up failed.")

elif option == "Login":
    st.subheader("Login to your Account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        result = firebase_login(email, password)
        st.success(f"Logged in as {email}" if result else "Login failed.")

elif option == "Logout":
    if st.button("Logout"):
        firebase_logout()
        st.success("Logged out successfully.")
