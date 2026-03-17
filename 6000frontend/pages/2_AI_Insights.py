import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("📊 Insights Dashboard")

if "user_email" not in st.session_state:
    st.markdown("""
    <div class="tip-box">
    Sign in from the <strong>Account</strong> page if you want to keep track of your resume history.
    </div>
    """, unsafe_allow_html=True)

result = st.session_state.get("latest_result")

if not result:
    st.warning("No resume analysis found yet. Please generate a resume first.")
else:
    success_rate = result.get("success_rate", 0)
    improvement_rate = result.get("improvement_rate", 0)
    detected_experience = result.get("experience_years_detected", 0)
    detected_projects = result.get("projects_detected", 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Success Rate", f"{success_rate}%")
    with col2:
        st.metric("Needs Improvement", f"{improvement_rate}%")
    with col3:
        st.metric("Career Level", result.get("seniority_level", "Unknown"))

    st.subheader("Success Overview")
    fig1, ax1 = plt.subplots()
    ax1.bar(["Success Rate", "Needs Improvement"], [success_rate, improvement_rate])
    ax1.set_ylim(0, 100)
    ax1.set_ylabel("Percentage")
    st.pyplot(fig1)

    st.subheader("Profile Strength Radar")
    categories = ["Experience", "Projects", "Resume Match", "Job Fit", "Readiness"]
    values = [
        min(detected_experience * 10, 100),
        min(detected_projects * 10, 100),
        result.get("semantic_score", 0),
        result.get("ml_score", 0),
        success_rate
    ]

    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig2, ax2 = plt.subplots(subplot_kw=dict(polar=True))
    ax2.plot(angles, values, linewidth=2)
    ax2.fill(angles, values, alpha=0.25)
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(categories)
    ax2.set_yticklabels([])
    st.pyplot(fig2)

    st.subheader("Skills to Improve")
    missing_skills = result.get("missing_skills", [])
    if missing_skills:
        heatmap_data = np.array([[1 for _ in missing_skills]])
        fig3, ax3 = plt.subplots()
        ax3.imshow(heatmap_data, aspect="auto")
        ax3.set_xticks(range(len(missing_skills)))
        ax3.set_xticklabels(missing_skills, rotation=45, ha="right")
        ax3.set_yticks([])
        ax3.set_title("Skills to Strengthen")
        st.pyplot(fig3)
    else:
        st.success("No important missing skills were detected for this role.")