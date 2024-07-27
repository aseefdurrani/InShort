from flask import Blueprint
from .summarizer import summarize
from .sentiment_analyzer import analyze_sentiment
from .trend_analyzer import analyze_trends

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/summarize', methods=['POST'])
def summarize_endpoint():
    return summarize()

@api_blueprint.route('/sentiment', methods=['POST'])
def sentiment_endpoint():
    return analyze_sentiment()

@api_blueprint.route('/trends', methods=['POST'])
def trends_endpoint():
    return analyze_trends()
