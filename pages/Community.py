import streamlit as st
from utils.firebase import add_post, get_all_posts, delete_post

st.title("Community Posts")

st.subheader("Create a Post")
username = st.text_input("Username")
post_details = st.text_area("Your Post")
if st.button("Submit Post"):
    if username and post_details:
        add_post(username, post_details)
        st.success("Post submitted!")
    else:
        st.error("Please enter both username and post content.")

st.divider()
st.subheader("Recent Posts")
posts = get_all_posts()
for post in posts:
    st.markdown(f"**{post['username']}** at {post['timestamp']}")
    st.write(post["post_details"])
    if st.button("Delete", key=post["id"]):
        delete_post(post["id"])
        st.experimental_rerun()
