# Import the spaCy library for Natural Language Processing
import spacy

# Load the small English language model from spaCy
# This model provides tokenization, lemmatization, POS tagging, etc.
nlp = spacy.load("en_core_web_sm")


def preprocess_text(text: str) -> str:
    """
    This function preprocesses raw resume text and prepares it
    for further machine learning tasks such as skill extraction
    and semantic similarity matching.

    Steps performed:
    1. Convert text to lowercase (for consistency)
    2. Tokenize the text using spaCy
    3. Remove stopwords (e.g., 'the', 'and')
    4. Remove punctuation
    5. Apply lemmatization (convert words to base form)

    Parameters:
    text (str): Raw resume text input by the user

    Returns:
    str: Cleaned and preprocessed text
    """

    # Convert the input text to lowercase to ensure uniform processing
    text = text.lower()

    # Pass the text through the spaCy NLP pipeline
    doc = nlp(text)

    # Create a list of cleaned tokens
    tokens = []

    # Iterate through each token in the document
    for token in doc:
        # Ignore stopwords (common words with little semantic value)
        # Ignore punctuation symbols
        if not token.is_stop and not token.is_punct:
            # Append the lemmatized (base) form of the word
            tokens.append(token.lemma_)

    # Join the cleaned tokens back into a single string
    cleaned_text = " ".join(tokens)

    return cleaned_text


# This block ensures the code runs only when the file is executed directly
# and not when it is imported into another module
if __name__ == "__main__":
    # Example resume text for testing the preprocessing function
    sample_text = "Experienced Python developer with 5 years of experience in Artificial Intelligence."

    # Call the preprocessing function and print the result
    print(preprocess_text(sample_text))
