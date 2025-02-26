import streamlit as st

# You can use st.experimental_set_query_params or rely on Streamlit's native multipage if you put pages in the pages/ folder.
# For this example, we'll use a simple radio on the sidebar to select the page.

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Account", "Take Mock Interview", "Community"])

if page == "Home":
    st.experimental_set_query_params(page="Home")
elif page == "Account":
    st.experimental_set_query_params(page="Account")
elif page == "Take Mock Interview":
    st.experimental_set_query_params(page="Interview")
elif page == "Community":
    st.experimental_set_query_params(page="Community")

# Automatically load the corresponding page.
# In Streamlit Sharing you can also use the multipage structure by putting files in the pages/ folder.
st.write("Please navigate using the sidebar. (For multipage apps, each file in pages/ is automatically detected.)")
