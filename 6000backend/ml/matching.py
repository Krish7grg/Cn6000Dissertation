"""
Semantic Resume–Job Matching Module
----------------------------------
This module computes semantic similarity between
a resume and a job description using Sentence-BERT.
"""

# Import required libraries
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load pre-trained Sentence-BERT model
# This model converts text into semantic embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(resume_text: str, job_text: str) -> float:
    """
    Computes semantic similarity between resume and job description.

    Parameters:
    ----------
    resume_text : str
        Preprocessed resume text.
    job_text : str
        Job description text.

    Returns:
    -------
    float
        Similarity score between 0 and 1.
    """

    # Convert both texts into vector embeddings
    embeddings = model.encode([resume_text, job_text])

    # Extract individual embeddings
    resume_embedding = embeddings[0].reshape(1, -1)
    job_embedding = embeddings[1].reshape(1, -1)

    # Compute cosine similarity between embeddings
    similarity_score = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    return similarity_score

# Test the module
if __name__ == "__main__":
    resume = (
        "Experienced Python developer with background in "
        "machine learning and artificial intelligence."
    )

    job_description = (
        "Looking for a software engineer skilled in Python, "
        "AI, and machine learning techniques."
    )

    score = compute_similarity(resume, job_description)
    print(f"Resume–Job Similarity Score: {score:.2f}")
