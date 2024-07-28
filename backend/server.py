from flask import Flask, jsonify, request  # Import Flask and necessary modules for handling requests and responses
from flask_cors import CORS  # Import CORS to handle Cross-Origin Resource Sharing
import subprocess  # Import subprocess for running external commands (not used in this snippet)
import json  # Import json for handling JSON data (not used in this snippet)
from scripts.query_wLangChain import get_response  # Import custom function to get response based on query

# Create a Flask app instance
app = Flask(__name__)
CORS(app)  # Enable CORS for the app

# Define a route for the API endpoint /api/chat that accepts POST requests
@app.route("/api/chat", methods=['POST'])
def return_home():
    data = request.get_json()  # Get JSON data from the request
    query = data.get('query', '')  # Extract the 'query' field from the JSON data

    print('here is our query:', query)  # Print the query for debugging purposes

    try:
        response = get_response(query)  # Get the response using the custom function
        print('Response:', response)  # Print the response for debugging purposes
        return jsonify (
            {'response': response}  # Return the response as JSON
        )
    except Exception as e:
        print('Error:', str(e))  # Print the error message for debugging purposes
        return jsonify (
            {'error': str(e)}  # Return the error message as JSON
        ), 500  # Return a 500 Internal Server Error status code

# Run the app if this script is executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
    # app.run(debug=True, port=8080)  # Run the app in debug mode on port 8080