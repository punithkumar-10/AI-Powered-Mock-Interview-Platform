import streamlit as st
from firebase_config import fs_client
from firebase_admin import firestore

def show_community():
    st.title("Community Posts")
    if not st.session_state.get("user"):
        st.error("Please log in to view and post in the community.")
        return

    user_email = st.session_state.user['email']
    st.header("New Post")
    with st.form("new_post_form"):
        post_content = st.text_area("Your post")
        submitted = st.form_submit_button("Submit Post")
        if submitted and post_content:
            post_data = {
                "username": user_email,
                "content": post_content,
                "timestamp": firestore.SERVER_TIMESTAMP
            }
            fs_client.collection("community").add(post_data)
            st.success("Post submitted!")

    st.header("Recent Posts")
    posts_ref = fs_client.collection("community").order_by("timestamp", direction=firestore.Query.DESCENDING)
    posts = posts_ref.stream()
    for post in posts:
        data = post.to_dict()
        with st.container():
            st.write(f"**{data.get('username')}** at {data.get('timestamp') if data.get('timestamp') else ''}")
            st.write(data.get("content"))
            if data.get("username") == user_email:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_{post.id}"):
                        new_content = st.text_area("Edit your post", value=data.get("content"), key=f"edit_input_{post.id}")
                        if st.button("Save", key=f"save_{post.id}"):
                            fs_client.collection("community").document(post.id).update({"content": new_content})
                            st.success("Post updated!")
                with col2:
                    if st.button("Delete", key=f"delete_{post.id}"):
                        fs_client.collection("community").document(post.id).delete()
                        st.success("Post deleted!")
                        st.experimental_rerun()
