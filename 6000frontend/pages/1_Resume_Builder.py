import streamlit as st
import requests
from database import conn, cursor
from util import (
    build_resume_text,
    build_resume_html,
    generate_pdf_bytes,
    generate_docx_bytes
)

API_URL = "http://127.0.0.1:8000/generate-and-analyze"

st.title("📄 Resume Builder")
st.markdown("Create a polished, downloadable, and editable resume using AI.")

st.image(
    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80",
    use_container_width=True
)

if "user_email" not in st.session_state:
    st.markdown("""
    <div class="tip-box">
    Want to save your resume history? Please visit the <strong>Account</strong> page and sign in first.
    </div>
    """, unsafe_allow_html=True)

with st.expander("Helpful tips before you begin"):
    st.write("""
    - Use clear job-relevant skills
    - Mention years of experience in your experience box
    - Mention projects if possible
    - Paste a real job description for better tailoring
    """)

template_name = st.selectbox(
    "Choose Resume Template",
    ["Modern", "Professional", "Minimal"]
)

accent_color = st.selectbox(
    "Choose Accent Color",
    ["#2563eb", "#7c3aed", "#059669", "#dc2626", "#ea580c"],
    format_func=lambda x: {
        "#2563eb": "Blue",
        "#7c3aed": "Purple",
        "#059669": "Green",
        "#dc2626": "Red",
        "#ea580c": "Orange"
    }[x]
)

with st.form("resume_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        education = st.text_input("Education", placeholder="MSc Artificial Intelligence")
        skills = st.text_area("Skills (comma separated)", placeholder="Python, Machine Learning, NLP")

    with col2:
        summary = st.text_area("Professional Summary")
        experience = st.text_area("Experience")
        job_description = st.text_area("Target Job Description")

    submit = st.form_submit_button("Generate Resume")

if submit:
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]

    payload = {
        "name": name,
        "email": email,
        "skills": skills_list,
        "experience": experience,
        "education": education,
        "summary": summary,
        "job_description": job_description
    }

    with st.spinner("Generating your resume and analysing your success potential..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=120)

            if response.status_code == 200:
                result = response.json()

                success_rate = round(result.get("success_rate", result.get("final_ai_score", 0)), 2)
                improvement_rate = round(result.get("improvement_rate", 100 - success_rate), 2)

                attractive_resume_text = build_resume_text(
                    template_name=template_name,
                    name=name,
                    email=email,
                    summary=summary,
                    skills=skills_list,
                    experience=experience,
                    education=education,
                    generated_resume=result.get("generated_resume", "")
                )

                attractive_resume_html = build_resume_html(
                    template_name=template_name,
                    accent_color=accent_color,
                    name=name,
                    email=email,
                    summary=summary,
                    skills=skills_list,
                    experience=experience,
                    education=education,
                    generated_resume=result.get("generated_resume", "")
                )

                result["attractive_resume"] = attractive_resume_text
                result["success_rate"] = success_rate
                result["improvement_rate"] = improvement_rate
                result["selected_template"] = template_name

                st.session_state["latest_result"] = result

                st.success("Your resume has been created successfully.")

                st.subheader("Styled Resume Preview")
                st.markdown(f"""
                <div class="custom-card">
                <h4 style="margin-bottom:8px;">Selected Design</h4>
                <p><strong>Template:</strong> {template_name}</p>
                <p><strong>Accent:</strong> <span style="color:{accent_color}; font-weight:700;">{accent_color}</span></p>
                <p>This preview shows how your final resume will look in a polished layout before download.</p>
                </div>
                """, unsafe_allow_html=True) 
                
                st.subheader("Editable Resume Content")
                st.text_area("Resume Text", attractive_resume_text, height=320)

                pdf_bytes = generate_pdf_bytes(attractive_resume_text, title=f"{name} Resume")
                docx_bytes = generate_docx_bytes(
                    name=name,
                    email=email,
                    summary=summary,
                    skills=skills_list,
                    experience=experience,
                    education=education,
                    generated_resume=result.get("generated_resume", "")
                )
                st.markdown("""
                <div class="custom-card">
                <h4 style="margin-bottom:8px;">Download Options</h4>
                <p>You can save your resume as a polished PDF or as an editable DOCX file for future editing.</p>
               </div>
                 """, unsafe_allow_html=True)

                d1, d2 = st.columns(2)

                with d1:
                 st.download_button(
                     label="⬇ Download PDF",
                     data=pdf_bytes,
                     file_name=f"{name.replace(' ', '_')}_resume.pdf",
                     mime="application/pdf"
              )

                with d2:
                 st.download_button(
                   label="⬇ Download DOCX (Editable)",
                   data=docx_bytes,
                   file_name=f"{name.replace(' ', '_')}_resume.docx",
                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
               )


                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Success Rate", f"{success_rate}%")
                with c2:
                    st.metric("Needs Improvement", f"{improvement_rate}%")
                with c3:
                    st.metric("Career Level", result.get("seniority_level", "Unknown"))

                st.write("Success Progress")
                st.progress(min(max(success_rate / 100, 0), 1))

                st.write("Improvement Indicator")
                st.progress(min(max(improvement_rate / 100, 0), 1))

                st.subheader("Key Suggestions")
                for rec in result.get("recommendations", []):
                    st.write(f"• {rec}")

                user_email = st.session_state.get("user_email", email if email else "guest")
                cursor.execute(
                    """
                    INSERT INTO resume_history
                    (user_email, template_name, generated_resume, success_rate, improvement_rate, seniority_level)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_email,
                        template_name,
                        attractive_resume_text,
                        success_rate,
                        improvement_rate,
                        result.get("seniority_level", "Unknown")
                    )
                )
                conn.commit()

            else:
                st.error(f"Backend returned status code {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")