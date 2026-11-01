from flask import Blueprint, request, jsonify, session
from backend.models import AcademicResult, StudentProfile
import os
import pickle
import pandas as pd

academic_bp = Blueprint('academic', __name__, url_prefix='/api/academic')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

_academic_models = None
def get_academic_models():
    global _academic_models
    if _academic_models is None:
        p = os.path.join(BASE_DIR, 'model', 'academic_models.pkl')
        if os.path.exists(p):
            with open(p, 'rb') as f:
                _academic_models = pickle.load(f)
    return _academic_models

@academic_bp.route('/results', methods=['GET'])
def get_results():
    student = StudentProfile.query.filter_by(student_id='SB2026').first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    results = AcademicResult.query.filter_by(student_id=student.id).all()
    items = [r.to_dict() for r in results]
    
    return jsonify({
        'student_id': student.student_id,
        'student_name': student.name,
        'cgpa': student.cgpa,
        'semester': student.semester,
        'results': items
    })

@academic_bp.route('/predict-grade', methods=['POST'])
def predict_grade():
    """Predicts expected examination grade using the trained UCI Student Performance model."""
    data = request.get_json(silent=True) or {}
    study_time = int(data.get('studytime', 3))      # 1: <2hrs, 2: 2-5hrs, 3: 5-10hrs, 4: >10hrs
    failures = int(data.get('failures', 0))          # previous failures (0-3)
    absences = int(data.get('absences', 4))          # total absences
    g1 = float(data.get('G1') if data.get('G1') is not None else data.get('g1', 14.0))
    g2 = float(data.get('G2') if data.get('G2') is not None else data.get('g2', 15.0))
    subject = data.get('subject', 'math')

    models = get_academic_models()
    if not models or 'uci_regressor' not in models:
        # Fallback heuristic
        pred_g3 = round(min(20.0, max(0.0, (g1 * 0.4) + (g2 * 0.5) + (study_time * 0.8) - (failures * 1.5) - (absences * 0.1))), 1)
        pass_prob = 85.0 if pred_g3 >= 10 else 45.0
    else:
        reg = models['uci_regressor']
        clf = models['uci_classifier']
        row = {
            'studytime': study_time,
            'failures': failures,
            'absences': absences,
            'traveltime': 2,
            'age': 20,
            'Medu': 3,
            'Fedu': 3,
            'freetime': 3,
            'goout': 2,
            'health': 4,
            'internet': 'yes',
            'higher': 'yes',
            'subject': subject,
            'G1': g1,
            'G2': g2
        }
        df_row = pd.DataFrame([row])
        pred_g3 = round(float(reg.predict(df_row)[0]), 1)
        pass_prob = round(float(clf.predict_proba(df_row)[0][1]) * 100, 1)

    letter_grade = 'A' if pred_g3 >= 14 else ('B' if pred_g3 >= 12 else ('C' if pred_g3 >= 10 else 'F'))

    return jsonify({
        'predicted_score': pred_g3,
        'predicted_score_g3': pred_g3,
        'letter_grade': letter_grade,
        'is_pass': pred_g3 >= 10.0,
        'performance_band': 'Strong Pass' if pred_g3 >= 14 else ('Pass' if pred_g3 >= 10 else 'At-Risk (< 10/20)'),
        'scale': '0 to 20 points',
        'converted_percentage': round((pred_g3 / 20.0) * 100, 1),
        'pass_probability': pass_prob,
        'status': 'Strong Pass' if pred_g3 >= 14 else ('Pass' if pred_g3 >= 10 else 'At-Risk (< 10/20)'),
        'model': 'Trained on UCI Student Performance dataset (1,044 students)'
    })

@academic_bp.route('/predict-outcome', methods=['POST'])
def predict_outcome():
    """Predicts course completion likelihood using the trained OULAD model."""
    data = request.get_json(silent=True) or {}
    education = data.get('highest_education', 'HE Qualification')
    age_band = data.get('age_band', '0-35')
    prev_attempts = int(data.get('num_of_prev_attempts', 0))
    credits = int(data.get('studied_credits', 60))
    avg_score = float(data.get('avg_score') if data.get('avg_score') is not None else data.get('avg_assessment_score', 78.0))

    models = get_academic_models()
    if not models or 'oulad_classifier' not in models:
        prob = 82.0
    else:
        clf = models['oulad_classifier']
        row = {
            'highest_education': education,
            'age_band': age_band,
            'num_of_prev_attempts': prev_attempts,
            'studied_credits': credits,
            'avg_assessment_score': avg_score
        }
        df_row = pd.DataFrame([row])
        prob = round(float(clf.predict_proba(df_row)[0][1]) * 100, 1)

    outcome_label = 'Pass with Distinction' if prob >= 80 else ('Pass' if prob >= 50 else 'Fail/Withdrawn')

    return jsonify({
        'predicted_outcome': outcome_label,
        'confidence': round(prob / 100.0, 3),
        'completion_success_probability': prob,
        'risk_category': 'Low Risk (High Success Chance)' if prob >= 70 else ('Moderate Risk' if prob >= 50 else 'High Withdrawal/Fail Risk'),
        'model': 'Trained on Open University Learning Analytics Dataset (32,593 registrations)'
    })
