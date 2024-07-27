from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    sentiment = sentiment_analyzer(text)
    return sentiment[0]
