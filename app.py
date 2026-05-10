from flask import Flask, render_template, request, jsonify
import pickle
import random
import json

app = Flask(__name__)

# Load trained model
with open('model/chatbot_model.pkl', 'rb') as f:
    best_model = pickle.load(f)

# Load vectorizer
with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Load intents
with open('dataset/intents1.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Chat route
@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()

    user_input = data['message']

    # Convert text into vector
    user_vector = vectorizer.transform([user_input])

    # Predict intent
    predicted_tag = best_model.predict(user_vector)[0]

    # Default response
    response = "Sorry, I didn't understand."

    # Find matching response
    for intent in intents['intents']:

        if intent['tag'] == predicted_tag:

            response = random.choice(intent['responses'])

            break

    return jsonify({
        "response": response
    })

# Run application
if __name__ == '__main__':
    app.run(debug=True)