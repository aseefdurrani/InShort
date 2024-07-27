from flask import request, jsonify
from models.summarization_model import get_summary

def summarize():
    data = request.json
    text = data.get('text', '')
    summary = get_summary(text)
    return jsonify({"summary": summary})
