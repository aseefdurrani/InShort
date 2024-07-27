import re

def clean_text(text):
    """
    Clean and preprocess text data by removing unwanted characters
    and normalizing spaces.

    Args:
        text (str): The input text to clean.

    Returns:
        str: The cleaned and preprocessed text.
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\W', ' ', text)
    return text.lower()
