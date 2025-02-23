import streamlit as st
from pages.home import show_home
from pages.account import show_account
from pages.interview import show_interview
from pages.community import show_community

def main():
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    st.sidebar.title("Navigation")
    options = ["Home", "Account", "Take Mock Interview", "Community Post"]
    selection = st.sidebar.radio("Go to", options, index=options.index(st.session_state.page))
    st.session_state.page = selection

    if selection == "Home":
        show_home()
    elif selection == "Account":
        show_account()
    elif selection == "Take Mock Interview":
        show_interview()
    elif selection == "Community Post":
        show_community()

if __name__ == "__main__":
    main()
