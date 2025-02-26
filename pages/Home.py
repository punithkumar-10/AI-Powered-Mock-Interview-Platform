import streamlit as st

st.set_page_config(page_title="AI Mock Interview Platform", layout="wide")
st.title("Welcome to the AI Mock Interview Platform")
st.write("""
Our platform helps you practice and improve your interview skills using AI-generated questions and detailed feedback.
""")

col1, col2 = st.columns(2)
with col1:
    if st.button("Sign Up / Login"):
        st.experimental_set_query_params(page="Account")
with col2:
    if st.button("Take a Mock Interview"):
        st.experimental_set_query_params(page="Interview")
        
st.info("Use the sidebar or buttons above to navigate through the app.")
