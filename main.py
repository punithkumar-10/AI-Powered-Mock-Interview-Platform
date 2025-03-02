import streamlit as st

# Set page configuration for a modern layout
st.set_page_config(
    page_title="AI Mock Interview Platform", 
    page_icon="🤖",
    layout="wide"
)

# Advanced CSS with an eye-pleasing gradient background and custom fonts
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
    body {
        background: linear-gradient(135deg, #2C3E50, #4CA1AF);
        font-family: 'Roboto', sans-serif;
        color: #fefefe;
        margin: 0;
        padding: 0;
    }
    /* Card container styling */
    .card-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-top: 50px;
    }
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 25px;
        width: 280px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
    }
    .card h3 {
        font-size: 1.5rem;
        margin-bottom: 15px;
        color: #ffffff;
    }
    .card p {
        font-size: 1rem;
        color: #e0e0e0;
        margin-bottom: 25px;
    }
    .card-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        color: #ffcb05;
    }
    /* Header section styling */
    .header {
        text-align: center;
        padding: 80px 20px 40px;
    }
    .header h1 {
        font-size: 4rem;
        margin-bottom: 20px;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #ffcb05, #ff9d00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .header p {
        font-size: 1.5rem;
        color: #e0e0e0;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }
    /* Call-to-action button styling */
    .cta-button {
        display: inline-block;
        margin-top: 40px;
        padding: 15px 30px;
        background: linear-gradient(90deg, #ffcb05, #ff9d00);
        color: #2C3E50;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        text-decoration: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 203, 5, 0.3);
    }
    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 7px 20px rgba(255, 203, 5, 0.4);
    }
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 40px 0;
        color: #a0a0a0;
        font-size: 0.9rem;
        margin-top: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation links at the top
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🏠 Home", key="home_nav"):
        st.rerun()
with col2:
    if st.button("📋 Candidate Details", key="details_nav"):
        st.switch_page("pages/1_Candidate_Details.py")
with col3:
    if st.button("🎙️ Interview", key="interview_nav"):
        st.switch_page("pages/2_Interview.py")

# Main header (hero) section with Get Started button
st.markdown("""
<div class="header">
    <h1>AI Mock Interview Platform</h1>
    <p>Elevate your interview skills with our AI-powered mock interview experience. Prepare, practice, and perfect your performance for your dream job.</p>
</div>
""", unsafe_allow_html=True)

# Center the Get Started button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Get Started", use_container_width=True):
        st.switch_page("pages/1_Candidate_Details.py")

# Feature cards
st.markdown("""
<div class="card-container">
    <div class="card">
        <div class="card-icon">🤖</div>
        <h3>AI-Powered Questions</h3>
        <p>Get tailored interview questions based on your job role and experience level.</p>
    </div>
    <div class="card">
        <div class="card-icon">🎙️</div>
        <h3>Speech Recognition</h3>
        <p>Practice your verbal responses with our advanced speech-to-text technology.</p>
    </div>
    <div class="card">
        <div class="card-icon">📊</div>
        <h3>Detailed Feedback</h3>
        <p>Receive comprehensive feedback on your answers to improve your interview skills.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Reset session state button
# if st.button("Reset All Data (Debug)"):
#     for key in list(st.session_state.keys()):
#         del st.session_state[key]
#     st.success("Session state has been reset!")

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 AI Mock Interview Platform | Made with ❤️ by Punith Kumar</p>
</div>
""", unsafe_allow_html=True)