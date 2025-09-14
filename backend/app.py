from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='frontend')
CORS(app)

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = "https://api.groq.ai/v1/query"

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get('query')

    if not user_query:
        return jsonify({"response": "Please provide a valid query."})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"query": user_query}

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        groq_response = response.json().get('response_text', 'No response from Groq API.')
    except Exception as e:
        print(f"Error: {e}")
        groq_response = "Error fetching response."

    return jsonify({"response": groq_response})

# Serve static assets (like style.css, script.js)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)
