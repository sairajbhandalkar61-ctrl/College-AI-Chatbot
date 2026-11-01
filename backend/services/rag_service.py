"""
backend/services/rag_service.py • RAG Document Intelligence Engine for CORTEX 2.0
Handles document ingestion, text chunking, TF-IDF vector retrieval, and grounded citation.
"""
import os
import re
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RAG_STORAGE_DIR = os.path.join(BASE_DIR, 'dataset', 'knowledge_base')
os.makedirs(RAG_STORAGE_DIR, exist_ok=True)
INDEX_PATH = os.path.join(BASE_DIR, 'model', 'rag_index.pkl')

class RAGService:
    def __init__(self):
        self.chunks = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self.load_index()
        if not self.chunks:
            self.seed_default_knowledge()

    def chunk_text(self, text, doc_title, filename, category, chunk_size=150, overlap=30):
        words = text.split()
        chunks = []
        start = 0
        chunk_idx = 1
        
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)
            
            # Simple heuristic page / section estimation
            section_match = re.search(r'(Section\s+\d+|Chapter\s+\d+|Clause\s+[\d\.]+|###\s+[^\n]+)', chunk_text, re.IGNORECASE)
            section_ref = section_match.group(0).replace('#', '').strip() if section_match else f"Section {chunk_idx}"
            
            chunks.append({
                'id': f"{filename}_{chunk_idx}",
                'title': doc_title,
                'filename': filename,
                'category': category,
                'section': section_ref,
                'text': chunk_text,
                'word_count': len(chunk_words)
            })
            
            chunk_idx += 1
            start += (chunk_size - overlap)
            if start >= len(words):
                break
        return chunks

    def add_document(self, title, filename, category, raw_text):
        new_chunks = self.chunk_text(raw_text, title, filename, category)
        self.chunks.extend(new_chunks)
        self.rebuild_index()
        return len(new_chunks)

    def rebuild_index(self):
        if not self.chunks:
            return
        corpus = [c['text'] for c in self.chunks]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_features=8000)
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        
        with open(INDEX_PATH, 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'vectorizer': self.vectorizer,
                'matrix': self.tfidf_matrix
            }, f)

    def load_index(self):
        if os.path.exists(INDEX_PATH):
            try:
                with open(INDEX_PATH, 'rb') as f:
                    data = pickle.load(f)
                    self.chunks = data.get('chunks', [])
                    self.vectorizer = data.get('vectorizer')
                    self.tfidf_matrix = data.get('matrix')
            except Exception as e:
                print("Could not load RAG index:", e)

    def search(self, query, top_k=3, min_similarity=0.18):
        if not self.chunks or self.vectorizer is None or self.tfidf_matrix is None:
            return []
            
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
        
        top_indices = np.argsort(sims)[::-1][:top_k]
        results = []
        for idx in top_indices:
            score = float(sims[idx])
            if score >= min_similarity:
                chunk = self.chunks[idx].copy()
                chunk['confidence'] = round(score, 3)
                results.append(chunk)
        return results

    def seed_default_knowledge(self):
        """Seeds foundational verified official college policies for RAG retrieval."""
        handbook_text = """
        COLLEGE ACADEMIC POLICIES & CODE OF CONDUCT (2026-2027)
        Section 1: Attendance Requirement & Debarment Rule
        All undergraduate and postgraduate students must maintain a minimum of 75% aggregate attendance across all registered courses in each semester. Students falling below 75% without authorized medical condonation will be debarred from taking end-semester examinations. Medical condonation up to 10% requires medical board approval submitted within 7 days of absence.
        
        Section 2: Examination Evaluation & Grading System
        Assessment follows a 10-point Cumulative Grade Point Average (CGPA) system. Evaluation consists of 40% Continuous Internal Assessment (CIA: midterms, quizzes, coding lab assessments) and 60% End-Semester Final Examination. Minimum passing grade is 40% in theory and 50% in practical laboratory courses.
        
        Section 3: Fee Refund Policy
        Fee refund requests submitted before the academic orientation receive a 100% refund less processing charges of INR 1,000. Requests submitted within 15 days of session commencement receive an 80% refund. No refunds are admissible after 30 days of semester commencement.
        
        Section 4: Grievance Redressal Committee
        Students experiencing evaluation discrepancies or administrative difficulties may file a formal grievance via the student portal. The Grievance Redressal Committee investigates tickets and communicates a binding resolution within 5 working days.
        
        Section 5: Training & Placement Eligibility
        Students with zero active backlogs and a minimum CGPA of 6.5 are eligible to participate in on-campus recruitment drives. Company-specific criteria (e.g. 7.5+ CGPA for Tier-1 Product organizations) supersede generic campus eligibility.
        """
        self.add_document(
            title="Official College Academic Regulations & Handbook",
            filename="college_handbook_2026.txt",
            category="Handbook",
            raw_text=handbook_text
        )

# Global singleton
rag_engine = RAGService()
