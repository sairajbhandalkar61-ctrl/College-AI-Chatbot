from flask import Flask, render_template, request, jsonify
import pickle
import random
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Base directory for robust path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained model
model_path = os.path.join(BASE_DIR, 'model', 'chatbot_model.pkl')
with open(model_path, 'rb') as f:
    best_model = pickle.load(f)

# Load vectorizer
vec_path = os.path.join(BASE_DIR, 'model', 'vectorizer.pkl')
with open(vec_path, 'rb') as f:
    vectorizer = pickle.load(f)

# Load intents
intents_path = os.path.join(BASE_DIR, 'dataset', 'intents1.json')
with open(intents_path, 'r', encoding='utf-8') as file:
    intents = json.load(file)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Chat route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    user_input = data.get('message', '').strip()

    if not user_input:
        return jsonify({
            "response": "Please enter a question or topic to discuss."
        })

    # Convert text into vector
    user_vector = vectorizer.transform([user_input])

    # Predict intent
    predicted_tag = best_model.predict(user_vector)[0]

    # Default response
    response = "Sorry, I didn't understand. Could you please rephrase or ask about admissions, courses, fees, hostels, or campus facilities?"

    # Find matching response
    for intent in intents.get('intents', []):
        if intent.get('tag') == predicted_tag:
            response = random.choice(intent['responses'])
            break

    return jsonify({
        "response": response
    })

# Health check route for production deployment monitoring
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "college-ai-chatbot"
    }), 200

# Run application (for local execution; production uses `gunicorn app:app`)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") in ("1", "true", "True")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)