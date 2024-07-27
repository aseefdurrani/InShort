from flask import request, jsonify
from models.sentiment_model import analyze_sentiment as sentiment_analysis

def analyze_sentiment():
    data = request.json
    text = data.get('text', '')
    sentiment = sentiment_analysis(text)
    return jsonify({"sentiment": sentiment})
