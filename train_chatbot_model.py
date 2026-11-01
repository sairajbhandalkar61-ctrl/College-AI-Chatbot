import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

with open('dataset/intents1.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

patterns = []
labels = []
for intent in intents['intents']:
    tag = intent['tag']
    for pattern in intent['patterns']:
        patterns.append(pattern)
        labels.append(tag)

# Using standard TfidfVectorizer without aggressive stopword removal
vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
X = vectorizer.fit_transform(patterns)

model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X, labels)

test_queries = [
    "Mark my attendance today",
    "What is my current attendance?",
    "Predict my attendance risk",
    "What courses are offered?",
    "How much is the fee?",
    "Tell me about college fees",
    "Where is the hostel?"
]

print("Test Predictions:")
for query in test_queries:
    vec = vectorizer.transform([query])
    pred = model.predict(vec)[0]
    print(f"'{query}' -> '{pred}'")

import pickle
with open('model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('model/chatbot_model.pkl', 'wb') as f:
    pickle.dump(model, f)
