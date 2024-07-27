from flask import request, jsonify
from models.trend_model import analyze_trends as trend_analysis

def analyze_trends():
    data = request.json
    texts = data.get('texts', [])
    trends = trend_analysis(texts)
    return jsonify({"trends": trends})
