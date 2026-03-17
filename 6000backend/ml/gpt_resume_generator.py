"""
GPT-Based Resume Generator
---------------------------

Uses OpenAI GPT model to generate a professional resume
based on structured user input.
"""

import os
from openai import OpenAI

# Initialize OpenAI client using API key
client = OpenAI(api_key=os.getenv("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"))


def generate_resume_with_gpt(
    name: str,
    email: str,
    skills: list,
    experience: str,
    education: str,
    summary: str,
    job_description: str
) -> str:
    """
    Generates a professional resume tailored to a job description.
    """

    prompt = f"""
    Generate a professional, ATS-friendly resume.

    Candidate Name: {name}
    Email: {email}
    Skills: {', '.join(skills)}
    Experience: {experience}
    Education: {education}
    Professional Summary: {summary}

    Tailor the resume to this job description:
    {job_description}

    Format properly with sections:
    - Professional Summary
    - Technical Skills
    - Work Experience
    - Education

    Make it strong, professional, and optimized for job matching.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # cost-efficient + strong
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content