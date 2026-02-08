import streamlit as st
from db import create_user_table, register_user, login_user

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Redirect if already logged in
if st.session_state['logged_in']:
    st.switch_page("pages/home.py")

def login_register_page():
    st.title("🔐 Login or Register")

    menu = ["Login", "Register"]
    choice = st.selectbox("Choose Option", menu)

    create_user_table()

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"Welcome back, {username}!")
                st.switch_page("pages/home.py")
            else:
                st.error("Incorrect username or password.")

    else:
        st.subheader("Create New Account")
        username = st.text_input("Username", key="reg_user")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            if register_user(username, email, password):
                st.success("Registration successful. Please login now.")
            else:
                st.error("Username already taken.")

login_register_page()