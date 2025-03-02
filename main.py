import streamlit as st

# Set page configuration for a sleek, industry-level design
st.set_page_config(
    page_title="AI Mock Interview Platform", 
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for a hero section inspired by Apple’s design
st.markdown("""
    <style>
    .hero {
        background-image: url('https://images.unsplash.com/photo-1504384308090-c894fdcc538d');
        background-size: cover;
        background-position: center;
        padding: 150px 20px;
        text-align: center;
        color: white;
    }
    .hero h1 {
        font-size: 3.5rem;
        margin: 0;
        font-weight: 600;
    }
    .hero p {
        font-size: 1.5rem;
        margin: 20px 0;
    }
    .btn {
        padding: 10px 20px;
        font-size: 1.2rem;
        background-color: #007aff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Create the hero section
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown("<h1>AI Mock Interview Platform</h1>", unsafe_allow_html=True)
st.markdown("<p>Empowering job seekers to ace their interviews with AI-driven mock sessions.<br>Perfect your skills and land your dream job.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### To get started, navigate to the **Candidate Details** page from the sidebar!")
