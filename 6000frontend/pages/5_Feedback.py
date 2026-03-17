import streamlit as st
from database import conn, cursor

st.title("⭐ Feedback")

st.write("Please share your experience using this resume builder.")

rating = st.slider("Rate the application", 1, 5, 4)
comments = st.text_area("Comments")

if st.button("Submit Feedback"):
    user_email = st.session_state.get("user_email", "anonymous")
    cursor.execute(
        "INSERT INTO feedback (user_email, rating, comments) VALUES (?, ?, ?)",
        (user_email, rating, comments)
    )
    conn.commit()
    st.success("Thank you for your feedback.")