import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

def count_skills(skills_text: str) -> int:
    """
    Count skills in comma-separated skill field.
    """
    if pd.isna(skills_text):
        return 0
    return len([s.strip() for s in str(skills_text).split(",") if s.strip()])


# Load dataset
df = pd.read_csv("data/resume_dataset.csv")

print("✅ Dataset Loaded")
print("Rows:", len(df))

# Normalize decision column
df["Recruiter Decision"] = (
    df["Recruiter Decision"]
    .astype(str)
    .str.lower()
    .str.strip()
)

print("Unique decisions:", df["Recruiter Decision"].unique())

# Correct mapping for THIS dataset
df["label"] = df["Recruiter Decision"].map({
    "hire": 1,
    "reject": 0
})

df = df.dropna(subset=["label"])

print("Rows after mapping:", len(df))

# Create robust numeric feature
df["skill_count"] = df["Skills"].apply(count_skills)


# Encode categorical columns
le_skills = LabelEncoder()
le_education = LabelEncoder()
le_role = LabelEncoder()

df["Skills"] = le_skills.fit_transform(df["Skills"].astype(str))
df["Education"] = le_education.fit_transform(df["Education"].astype(str))
df["Job Role"] = le_role.fit_transform(df["Job Role"].astype(str))

# Feature selection (numerical + encoded)
features = [
    "Skills",
    "Experience (Years)",
    "Education",
    "Projects Count",
    "Salary Expectation ($)"
]

X = df[features]
y = df["label"]

# Train simple classifier
model = LogisticRegression(max_iter=2000)
model.fit(X, y)

# Save artifacts
joblib.dump(model, "ml/hiring_model.pkl")
joblib.dump(le_skills, "ml/encoder_skills.pkl")
joblib.dump(le_education, "ml/encoder_education.pkl")
joblib.dump(le_role, "ml/encoder_role.pkl")

print("✅ Model trained & saved successfully")