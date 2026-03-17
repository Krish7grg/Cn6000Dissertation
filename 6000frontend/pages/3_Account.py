import streamlit as st
import hashlib
from database import conn, cursor


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


st.title("👤 Account")
st.write("Create an account or sign in to save resume history and manage your activity.")

tab1, tab2 = st.tabs(["Sign Up", "Login"])

with tab1:
    st.subheader("Create Account")
    name = st.text_input("Full Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Create Account"):
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hash_password(password))
            )
            conn.commit()
            st.success("Account created successfully.")
        except Exception:
            st.error("This email may already exist.")

with tab2:
    st.subheader("Login")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (login_email, hash_password(login_password))
        )
        user = cursor.fetchone()

        if user:
            st.session_state["user_email"] = login_email
            st.success("Login successful.")
        else:
            st.error("Invalid email or password.")