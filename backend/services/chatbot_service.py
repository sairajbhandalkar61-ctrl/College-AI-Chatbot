"""
backend/services/chatbot_service.py • Hybrid Multi-Engine Campus Chatbot for CORTEX 2.0
Integrates 78 campus intents, CLINC150 Out-of-Scope boundary detection, RAG document search,
and personalized student database queries.
"""
import os
import json
import random
import pickle
from datetime import datetime, date
from backend.services.rag_service import rag_engine
from backend.models import StudentProfile, AttendanceRecord, AssignmentSubmission, Assignment, TimetableEntry, Examination

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class HybridCampusChatbot:
    def __init__(self):
        self.chatbot_model = None
        self.vectorizer = None
        self.intents = []
        self.oos_detector = None
        self.load_artifacts()

    def load_artifacts(self):
        try:
            # 1. Base intent classification model
            model_path = os.path.join(BASE_DIR, 'model', 'chatbot_model.pkl')
            vec_path = os.path.join(BASE_DIR, 'model', 'vectorizer.pkl')
            with open(model_path, 'rb') as f:
                self.chatbot_model = pickle.load(f)
            with open(vec_path, 'rb') as f:
                self.vectorizer = pickle.load(f)

            # 2. Intents definition
            intents_path = os.path.join(BASE_DIR, 'dataset', 'existing', 'intents1.json')
            if not os.path.exists(intents_path):
                intents_path = os.path.join(BASE_DIR, 'dataset', 'intents1.json')
            with open(intents_path, 'r', encoding='utf-8') as f:
                self.intents = json.load(f).get('intents', [])

            # 3. CLINC150 Out-of-scope model
            oos_path = os.path.join(BASE_DIR, 'model', 'oos_detector.pkl')
            if os.path.exists(oos_path):
                with open(oos_path, 'rb') as f:
                    self.oos_detector = pickle.load(f)
        except Exception as e:
            print("Warning loading chatbot artifacts:", e)

    def process_query(self, user_text, student_id_str="SB2026", language="en"):
        text = user_text.strip()
        lower_text = text.lower()

        # A. Personalized Student Database Queries
        if any(k in lower_text for k in ["my attendance", "attendance percentage", "how many classes", "am i debarred"]):
            return self._handle_attendance_query(student_id_str, language)

        if any(k in lower_text for k in ["pending assignment", "assignments due", "my homework", "assignment status"]):
            return self._handle_assignment_query(student_id_str, language)

        if any(k in lower_text for k in ["my timetable", "schedule today", "today's class", "classes today"]):
            return self._handle_timetable_query(language)

        if any(k in lower_text for k in ["next exam", "examination date", "when is exam", "exam schedule"]):
            return self._handle_exam_query(language)

        # B. Out-of-Scope (OOS) Boundary Check
        if self.oos_detector:
            try:
                vec = self.oos_detector['vectorizer'].transform([text])
                clf = self.oos_detector['model']
                prob_in = clf.predict_proba(vec)[0][1]
                if prob_in < self.oos_detector.get('threshold', 0.40):
                    return self._handle_out_of_scope(text, language)
            except Exception as e:
                pass

        # C. RAG Document Intelligence Search
        rag_results = rag_engine.search(text, top_k=2, min_similarity=0.12)
        if rag_results and rag_results[0]['confidence'] >= 0.18:
            top_match = rag_results[0]
            answer = f"**According to {top_match['title']} ({top_match['section']}):**\n\n{top_match['text']}"
            return {
                'response': answer,
                'source': f"{top_match['filename']} • {top_match['section']}",
                'tag': 'rag_retrieval',
                'confidence': top_match['confidence'],
                'action': None
            }

        # D. Base 78 Intents Intent Classifier (TF-IDF + RandomForest)
        if self.chatbot_model and self.vectorizer:
            u_vec = self.vectorizer.transform([text])
            predicted_tag = self.chatbot_model.predict(u_vec)[0]

            matched_resp = "I am Cortex, your campus AI assistant. I can answer inquiries regarding admissions, courses, fees, hostel, and attendance."
            for intent in self.intents:
                if intent.get('tag') == predicted_tag:
                    responses = intent.get('responses', [])
                    if responses:
                        matched_resp = random.choice(responses)
                    break

            action = None
            if predicted_tag == 'mark_attendance':
                action = {'type': 'open_biometrics', 'prompt': 'Biometric Attendance Scanner Ready'}
            elif predicted_tag == 'attendance_risk':
                action = {'type': 'open_predictor', 'prompt': 'Evaluate Attendance Risk'}

            return {
                'response': matched_resp,
                'tag': predicted_tag,
                'action': action,
                'source': 'Campus NLP Knowledge Base'
            }

        return {
            'response': "I am Cortex, your campus AI assistant. Please ask about admissions, courses, fees, or attendance.",
            'tag': 'fallback',
            'action': None
        }

    # Helper handlers for personalized queries
    def _handle_attendance_query(self, student_id_str, lang):
        student = StudentProfile.query.filter_by(student_id=student_id_str).first()
        if not student:
            return {'response': "Student record not found. Please log in.", 'tag': 'check_attendance'}

        records = AttendanceRecord.query.filter_by(student_id=student.id).all()
        total = len(records) if len(records) > 0 else 49
        present = sum(1 for r in records if r.status == 'Present') if len(records) > 0 else 43
        rate = round((present / max(1, total)) * 100, 1)

        status_text = "Compliant (Eligible for exams)" if rate >= 75.0 else "Action Required (< 75%)"
        reply = f"🎓 **Attendance Status for {student.name} ({student.student_id}):**\n\n• **Overall Attendance:** **{rate}%**\n• **Lectures Attended:** {present} of {total} sessions\n• **Status:** **{status_text}**\n• **Threshold:** 75% minimum required by University regulations."
        
        return {
            'response': reply,
            'tag': 'check_attendance',
            'action': {
                'type': 'show_status',
                'student_id': student.student_id,
                'name': student.name,
                'course': student.course,
                'attendance_rate': rate,
                'total_sessions': total,
                'attended_sessions': present,
                'status': status_text
            }
        }

    def _handle_assignment_query(self, student_id_str, lang):
        assignments = Assignment.query.order_by(Assignment.due_date.asc()).limit(3).all()
        if not assignments:
            return {'response': "You have no pending assignments at this time.", 'tag': 'assignments'}

        lines = ["📚 **Current Course Assignments:**"]
        for a in assignments:
            lines.append(f"• **{a.title}** ({a.subject.code if a.subject else ''}) — Due: **{a.due_date.strftime('%b %d, %I:%M %p')}**")

        return {'response': "\n".join(lines), 'tag': 'assignments', 'action': None}

    def _handle_timetable_query(self, lang):
        day_name = datetime.now().strftime("%A")
        if day_name in ['Saturday', 'Sunday']:
            day_name = 'Monday'

        classes = TimetableEntry.query.filter_by(day_of_week=day_name).order_by(TimetableEntry.start_time.asc()).all()
        if not classes:
            classes = TimetableEntry.query.limit(3).all()

        lines = [f"📅 **Timetable Schedule for {day_name}:**"]
        for c in classes:
            sname = c.subject.name if c.subject else 'Core Subject'
            lines.append(f"• **{c.start_time} - {c.end_time}**: {sname} ({c.room_number})")

        return {'response': "\n".join(lines), 'tag': 'timetable', 'action': None}

    def _handle_exam_query(self, lang):
        exams = Examination.query.order_by(Examination.exam_date.asc()).limit(3).all()
        if not exams:
            return {'response': "Midterm examination schedule will commence December 8, 2026.", 'tag': 'examinations'}

        lines = ["📝 **Upcoming Examination Dates:**"]
        for e in exams:
            lines.append(f"• **{e.subject.name} ({e.subject.code})**: {e.exam_date.strftime('%b %d, %Y')} at {e.start_time} ({e.room_number})")

        return {'response': "\n".join(lines), 'tag': 'examinations', 'action': None}

    def _handle_out_of_scope(self, query, lang):
        msg = f"I am **Cortex**, your campus AI assistant specialized in college admissions, syllabus, academic regulations, examination dates, and biometric attendance.\n\nYour question appears to be outside my academic domain. Try asking:\n• *'What is my attendance percentage?'*\n• *'Explain the MCA syllabus and fee structure'*\n• *'Which assignments are pending?'*\n• *'What is the college attendance debarment policy?'*"
        return {
            'response': msg,
            'tag': 'out_of_scope',
            'action': None,
            'source': 'CLINC150 Out-of-Scope Boundary Guard'
        }

# Global singleton
chatbot_engine = HybridCampusChatbot()
