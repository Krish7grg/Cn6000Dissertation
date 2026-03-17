"""
Enhanced Skill Extraction Module
--------------------------------
This module extracts both single-word and multi-word
technical skills from resume text using spaCy.
"""

import spacy
from spacy.matcher import PhraseMatcher
from typing import List

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Predefined list of technical skills (single + multi-word)
SKILL_LIST = [
    "python",
    "java",
    "c++",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "data science",
    "sql",
    "tensorflow",
    "pytorch",
    "scikit-learn"
]

# Initialize PhraseMatcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Convert skills into spaCy documents
skill_patterns = [nlp(skill) for skill in SKILL_LIST]
matcher.add("SKILLS", skill_patterns)

def extract_skills(text: str) -> List[str]:
    """
    Extracts technical skills from resume text.

    Parameters:
    ----------
    text : str
        Resume text.

    Returns:
    -------
    List[str]
        List of extracted skills.
    """

    doc = nlp(text)
    matches = matcher(doc)

    found_skills = set()

    # Extract matched phrases
    for match_id, start, end in matches:
        skill = doc[start:end].text.lower()
        found_skills.add(skill)

    return list(found_skills)

# Test the module
if __name__ == "__main__":
    sample_resume = (
        "Experienced Python developer with expertise in "
        "machine learning and artificial intelligence."
    )
    print(extract_skills(sample_resume))




