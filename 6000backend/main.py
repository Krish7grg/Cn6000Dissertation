from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib

# --- ML / NLP Imports ---
from ml.preprocessing import preprocess_text
from ml.matching import compute_similarity
from ml.skill_extraction import extract_skills
from ml.feature_extraction import (
    extract_experience_years,
    extract_project_count,
    estimate_seniority,
    estimate_salary_from_seniority
)
from ml.gpt_resume_generator import generate_resume_with_gpt


app = FastAPI()

# -----------------------------
# LOAD TRAINED ML ARTIFACTS
# -----------------------------

hiring_model = joblib.load("ml/hiring_model.pkl")
encoder_skills = joblib.load("ml/encoder_skills.pkl")
encoder_education = joblib.load("ml/encoder_education.pkl")
encoder_role = joblib.load("ml/encoder_role.pkl")

# -----------------------------
# REQUEST SCHEMA
# -----------------------------

class ResumeRequest(BaseModel):
    name: str
    email: str
    skills: List[str]
    experience: str
    education: str
    summary: str
    job_description: str


# -----------------------------
# ML PREDICTION FUNCTION
# -----------------------------
def safe_encode_education(education: str) -> int:
    try:
        return int(encoder_education.transform([education])[0])
    except Exception:
        return 0


def safe_encode_role(role: str) -> int:
    try:
        return int(encoder_role.transform([role])[0])
    except Exception:
        return 0


def predict_hiring_probability_structured(
    skill_count: int,
    experience_years: int,
    education: str,
    projects_count: int,
    salary_expectation: int
    
) -> float:
    """
    Predict hiring probability using the trained supervised ML model.
    """

    education_encoded = safe_encode_education(education)
    

    features = [[
        skill_count,
        experience_years,
        education_encoded,
        projects_count,
        salary_expectation
    
    ]]

    probability = hiring_model.predict_proba(features)[0][1]
    return float(probability)

# -----------------------------
# MAIN ENDPOINT
# -----------------------------

@app.post("/generate-and-analyze")
def generate_and_analyze(data: ResumeRequest):

    # --- 1. Generate Resume via GPT ---
    generated_resume = generate_resume_with_gpt(
        name=data.name,
        email=data.email,
        skills=data.skills,
        experience=data.experience,
        education=data.education,
        summary=data.summary,
        job_description=data.job_description

    )

    # --- 2. Clean/preprocess Text for NLP ---
    cleaned_resume = preprocess_text(generated_resume)
    cleaned_job = preprocess_text(data.job_description)

    extracted_resume_skills = extract_skills(cleaned_resume)
    job_required_skills = extract_skills(cleaned_job)

    missing_skills = sorted(list(set(job_required_skills) - set(extracted_resume_skills)))

    # --- 3. Semantic Similarity (SBERT) ---
    similarity = float(compute_similarity(cleaned_resume, cleaned_job))
    semantic_score = round(similarity * 100, 2)

    # --- 4. Structured ML Prediction ---
    # TEMPORARY heuristics (next we automate)
    experience_years = extract_experience_years(generated_resume)
    projects_count = extract_project_count(generated_resume)
    seniority_level = estimate_seniority(experience_years)

    salary_expectation = estimate_salary_from_seniority(seniority_level)

    skill_count = len(data.skills) if data.skills else len(extracted_resume_skills)

    hiring_probability = predict_hiring_probability_structured(
    skill_count=skill_count,
    experience_years=experience_years,
    education=data.education,
    projects_count=projects_count,
    salary_expectation=salary_expectation
    
)

    ml_score = round(hiring_probability * 100, 2)

    # --- 5. Final Hybrid Score ---
    final_ai_score = round((0.5 * semantic_score) + (0.5 * ml_score), 2)
    success_rate = final_ai_score
    improvement_rate = round(100 - success_rate, 2)

    # --- 6. Recommendation Logic ---

    recommendations = []

    if success_rate < 50:
     recommendations.append("Your resume currently has a low chance of matching this role well.")
     recommendations.append("Try strengthening job-specific achievements and clearer role alignment.")
    elif success_rate < 75:
     recommendations.append("Your resume has a moderate chance of success, but it can still be improved.")
     recommendations.append("Focus on making your experience and skills more specific to the target job.")
    else:
     recommendations.append("Your resume is strongly aligned with this role and shows a high chance of success.")

    if missing_skills:
     recommendations.append(
        "Consider highlighting these relevant skills if you genuinely have them: {', '.join(missing_skills)}"
    )

    if experience_years == 0:
     recommendations.append("Your resume does not clearly show years of experience.")

    if projects_count == 0:
     recommendations.append("Add project-based achievements to strengthen your resume.")
    
    
    
    # --- 7. Response --- 
    return {
          
    "generated_resume": generated_resume,

    "similarity_score": similarity,
    "semantic_score": semantic_score,
    "hiring_probability": hiring_probability,
    "ml_score": ml_score,
    "success_rate": success_rate,
    "improvement_rate": improvement_rate,

    "experience_years_detected": experience_years,
    "projects_detected": projects_count,
    "seniority_level": seniority_level,

    "extracted_resume_skills": extracted_resume_skills,
    "job_required_skills": job_required_skills,
    "missing_skills": missing_skills,

    "recommendations": recommendations
}
    