from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='/static')
CORS(app)  # Allows all origins to avoid CORS errors

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
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
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": user_query}]
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            groq_response = response.json()['choices'][0]['message']['content']
        else:
            groq_response = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        print(f"Error: {e}")
        groq_response = "Something went wrong while fetching the answer."

    return jsonify({"response": groq_response})

if __name__ == '__main__':
    app.run(debug=True)
