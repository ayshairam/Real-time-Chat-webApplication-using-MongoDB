

import streamlit as st
import time
from auth import signup_user, login_user
from utils import save_message, get_messages

st.set_page_config("💬 Chat App", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None
if "receiver_email" not in st.session_state:
    st.session_state.receiver_email = ""


def login_ui():
    st.subheader("🔐 Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pw")
    if st.button("Login"):
        success, user = login_user(email, password)
        if success:
            st.session_state.user = user
            st.success("Login successful!")
            st.rerun()  # Refresh the page after login
        else:
            st.error("Invalid email or password.")


def signup_ui():
    st.subheader("📝 Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        success, msg = signup_user(username, email, password)
        st.success(msg) if success else st.error(msg)


def chat_ui():
    st.markdown(f"### 👋 Welcome, `{st.session_state.user['username']}`")

    st.session_state.receiver_email = st.text_input("🧑‍💻 Chat with (receiver's email)",
                                                    value=st.session_state.receiver_email)

    if not st.session_state.receiver_email:
        st.error("Please enter a receiver's email.")
        return  # Return early if receiver email is empty

    # Fetch chat messages from the database
    messages = get_messages(st.session_state.user["email"], st.session_state.receiver_email)

    st.markdown("---")
    st.subheader("💬 Chat")

    # Display chat messages
    chat_box = st.empty()
    with chat_box.container():
        if messages:  # Check if there are any messages
            for msg in messages:
                sender = msg["sender"]
                text = msg["message"]
                align = "➡️" if sender == st.session_state.user["email"] else "⬅️"
                st.markdown(f"{align} **{sender}**: {text}")
        else:
            st.markdown("No messages yet. Start the conversation!")

    # Input for new message
    new_msg = st.text_input("Type your message")
    if st.button("Send"):
        if new_msg.strip():
            save_message(st.session_state.user["email"], st.session_state.receiver_email, new_msg)
            st.rerun()  # Refresh the page to show the new message

    # Auto-refresh the chat every 5 seconds to check for new messages
    time.sleep(5)  # Wait for 5 seconds
    st.rerun()  # Rerun the app to update the chat messages


st.title("📱 Simple WhatsApp-style Chat")

if st.session_state.user:
    chat_ui()  # Only show chat window if the user is logged in
else:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        login_ui()
    with tab2:
        signup_ui()


