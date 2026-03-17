import re


def extract_experience_years(resume_text: str) -> int:
    patterns = [
        r"(\d+)\+?\s+years",
        r"over\s+(\d+)\s+years",
        r"(\d+)\s+yrs"
    ]

    text = resume_text.lower()

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))

    return 0


def extract_project_count(resume_text: str) -> int:
    text = resume_text.lower()
    return len(re.findall(r"\bproject\b", text))


def estimate_seniority(experience_years: int) -> str:
    if experience_years == 0:
        return "Entry Level"
    if experience_years < 2:
        return "Junior"
    if experience_years < 5:
        return "Mid-Level"
    return "Senior"


def estimate_salary_from_seniority(seniority_level: str) -> int:
    if seniority_level == "Senior":
        return 90000
    if seniority_level == "Mid-Level":
        return 60000
    if seniority_level == "Junior":
        return 45000
    return 35000


