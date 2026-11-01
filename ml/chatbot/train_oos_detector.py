"""
ml/chatbot/train_oos_detector.py
Trains an Out-of-Scope (OOS) detector and confidence evaluator using CLINC150 and college intents.
"""
import os
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODEL_DIR = os.path.join(BASE_DIR, 'model')

def train_oos_model():
    print("=" * 60)
    print("Training CLINC150 Out-of-Scope (OOS) & Domain Boundary Model...")
    print("=" * 60)
    
    clinc_path = os.path.join(DATASET_DIR, 'chatbot', 'clinc150', 'oos-eval-master', 'data', 'data_small.json')
    if not os.path.exists(clinc_path):
        clinc_path = os.path.join(DATASET_DIR, 'chatbot', 'clinc150', 'data', 'data_small.json')
    if not os.path.exists(clinc_path):
        clinc_path = os.path.join(DATASET_DIR, 'chatbot', 'clinc150', 'oos-eval-master', 'data', 'data_full.json')
    
    with open(clinc_path, 'r', encoding='utf-8') as f:
        clinc_data = json.load(f)
        
    intents_path = os.path.join(DATASET_DIR, 'existing', 'intents1.json')
    with open(intents_path, 'r', encoding='utf-8') as f:
        college_intents = json.load(f)
        
    # In-domain college queries: label = 1
    in_domain_texts = []
    for item in college_intents.get('intents', []):
        for pat in item.get('patterns', []):
            in_domain_texts.append(pat)
            
    # Out-of-domain queries from CLINC150 oos splits: label = 0
    oos_texts = [q[0] for q in clinc_data.get('oos_train', [])] + [q[0] for q in clinc_data.get('oos_test', [])[:500]]
    
    print(f"Dataset summary: {len(in_domain_texts)} college in-domain queries, {len(oos_texts)} out-of-scope queries.")
    
    X_texts = in_domain_texts + oos_texts
    y_labels = [1] * len(in_domain_texts) + [0] * len(oos_texts)
    
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=4000, lowercase=True)
    X_vec = vectorizer.fit_transform(X_texts)
    
    clf = LogisticRegression(C=2.0, max_iter=300, random_state=42)
    clf.fit(X_vec, y_labels)
    
    preds = clf.predict(X_vec)
    print(f"Domain Boundary Filter Accuracy: {accuracy_score(y_labels, preds)*100:.2f}%")
    
    # Validation test queries
    test_queries = [
        ("What is the fee for B.Tech Computer Science?", 1),
        ("Where is the student hostel located?", 1),
        ("Mark my attendance with facelock", 1),
        ("How to cook italian pasta carbonara at home?", 0),
        ("Who won the FIFA world cup in 2018?", 0),
        ("What is the distance between Jupiter and Saturn?", 0)
    ]
    
    print("\nSample Boundary Classification Test:")
    for query, expected in test_queries:
        vec = vectorizer.transform([query])
        prob_in_domain = clf.predict_proba(vec)[0][1]
        is_in = prob_in_domain >= 0.5
        print(f"  • '{query}' -> {'IN_DOMAIN' if is_in else 'OUT_OF_SCOPE'} (prob: {prob_in_domain:.3f})")
        
    artifacts = {
        'vectorizer': vectorizer,
        'model': clf,
        'threshold': 0.45
    }
    
    out_file = os.path.join(MODEL_DIR, 'oos_detector.pkl')
    with open(out_file, 'wb') as f:
        pickle.dump(artifacts, f)
    print(f"\n[Saved OOS Boundary Artifacts] {out_file}")

if __name__ == '__main__':
    train_oos_model()
