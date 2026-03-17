import streamlit as st
import pandas as pd
from database import conn

st.title("🗂 Saved Resume History")

user_email = st.session_state.get("user_email")

if not user_email:
    st.info("Please log in to view your saved resume history.")
else:
    df = pd.read_sql_query(
        "SELECT template_name, success_rate, improvement_rate, seniority_level, generated_resume FROM resume_history WHERE user_email = ? ORDER BY id DESC",
        conn,
        params=(user_email,)
    )

    if df.empty:
        st.warning("No saved resume history found.")
    else:
        st.dataframe(df[["template_name", "success_rate", "improvement_rate", "seniority_level"]])

        selected_index = st.selectbox("Select a saved resume", df.index.tolist())

        st.subheader("Saved Resume Preview")
        st.text_area("Resume", df.loc[selected_index, "generated_resume"], height=350)