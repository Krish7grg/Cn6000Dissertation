import streamlit as st


def load_css():
    try:
        with open("static/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="🧠",
    layout="wide"
)

load_css()

st.sidebar.title("🧠 AI Resume Builder")
st.sidebar.write("Create, evaluate, improve, and download your resume.")
st.sidebar.markdown("👉 Go to **Account** to sign in or create an account.")

st.title("AI Resume Builder and Career Success Dashboard")
st.markdown("""
Build a beautiful resume, measure your job-fit success potential, and improve it with AI-driven recommendations.
""")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="custom-card">
        <h3>Build Your Resume with AI</h3>
        <p>Create a professional and attractive resume using smart templates, role-based generation, and downloadable editable formats.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="custom-card">
        <h3>Understand Your Success Potential</h3>
        <p>View success rate, improvement rate, insights, charts, and personalised recommendations in a user-friendly way.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image(
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
        use_container_width=True
    )

st.markdown("""
<div class="tip-box">
<strong>Quick start:</strong> Open the <strong>Resume Builder</strong> page, choose a template, generate your resume, then download it as PDF or DOCX.
</div>
""", unsafe_allow_html=True)

st.info("Use the sidebar to move between Resume Builder, Insights Dashboard, Resume History, Account, Feedback, and About.")