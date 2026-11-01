import pytest
import os
import json
from backend import create_app
from backend.database import db
from backend.models import StudentProfile, User

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False
    })
    return app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

# 1. Health & Core Routes
def test_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'healthy'
    assert 'chatbot_intent' in data['models']
    assert 'academic_performance' in data['models']

def test_home_page_renders_cortex2(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'CORTEX 2.0' in res.data
    assert b'Biometric Attendance' in res.data

def test_legacy_chatbot_route(client):
    res = client.get('/chatbot')
    assert res.status_code == 200
    assert b'Cortex' in res.data

# 2. Authentication API
def test_auth_login_student(client):
    res = client.post('/api/auth/login', json={
        'username': 'sairaj',
        'password': 'password123'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data['user']['username'] == 'sairaj'
    assert data['user']['role'] == 'student'

def test_auth_login_invalid(client):
    res = client.post('/api/auth/login', json={
        'username': 'sairaj',
        'password': 'wrongpassword'
    })
    assert res.status_code == 401

# 3. Chatbot NLP & RAG Integration
def test_chatbot_campus_intent(client):
    res = client.post('/api/chatbot/message', json={
        'message': 'What is the library timing?',
        'student_id': 'SB2026'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'response' in data
    assert len(data['response']) > 0

def test_chatbot_personalized_attendance_query(client):
    res = client.post('/api/chatbot/message', json={
        'message': 'check my attendance status',
        'student_id': 'SB2026'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert '86.4%' in data['response'] or 'attendance' in data['response'].lower()

def test_chatbot_personalized_assignments_query(client):
    res = client.post('/api/chatbot/message', json={
        'message': 'what assignments are pending?',
        'student_id': 'SB2026'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'assignment' in data['response'].lower()

# 4. Biometric Attendance API
def test_attendance_status(client):
    res = client.get('/api/attendance/status/SB2026')
    assert res.status_code == 200
    data = res.get_json()
    assert data['student_id'] == 'SB2026'
    assert 'attendance_rate' in data

def test_attendance_mark_face(client):
    res = client.post('/api/attendance/verify-face', json={
        'student_id': 'SB2026',
        'image_data': 'test_frame_snapshot'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert data['student_id'] == 'SB2026'

def test_attendance_predict_ml(client):
    res = client.post('/api/attendance/predict', json={
        'study_hours': 5.0,
        'sleep_hours': 7.5,
        'travel_time_minutes': 25.0,
        'course': 'b.tech',
        'year': '3rd year'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'attendance_probability' in data
    assert 'risk_level' in data
    assert data['attendance_probability'] >= 0.0

# 5. Success Advisor API
def test_success_advisor_dashboard(client):
    res = client.get('/api/success/dashboard?student_id=SB2026')
    assert res.status_code == 200
    data = res.get_json()
    assert 'student' in data
    assert 'study_plan' in data
    assert 'recommendations' in data
    assert len(data['study_plan']) > 0

def test_study_plan_task_update(client):
    res = client.patch('/api/success/tasks/1', json={
        'status': 'Completed'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data['task']['status'] == 'Completed'

# 6. Academic Analytics & ML Models
def test_uci_grade_prediction(client):
    res = client.post('/api/academic/predict-grade', json={
        'G1': 14.0,
        'G2': 15.0,
        'studytime': 3,
        'absences': 2
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'predicted_score' in data
    assert 'letter_grade' in data
    assert data['is_pass'] is True

def test_oulad_outcome_prediction(client):
    res = client.post('/api/academic/predict-outcome', json={
        'total_vle_clicks': 1200,
        'avg_score': 82.0,
        'assessments_count': 5
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'predicted_outcome' in data
    assert 'confidence' in data

# 7. Career & Resume Intelligence
def test_career_resume_analysis(client):
    res = client.post('/api/career/analyze-resume', json={
        'resume_text': 'Experienced Python developer skilled in machine learning, flask, SQL, scikit-learn, and git.'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'extracted_skills' in data
    assert 'python' in [s.lower() for s in data['extracted_skills']]
    assert 'target_match' in data

# 8. Timetable, Assignments & Notices
def test_timetable_and_exams(client):
    res = client.get('/api/timetable')
    assert res.status_code == 200
    assert 'slots' in res.get_json()

    res_exams = client.get('/api/timetable/examinations')
    assert res_exams.status_code == 200
    assert 'examinations' in res_exams.get_json()

def test_assignments_list_and_submission(client):
    res = client.get('/api/assignments?student_id=SB2026')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data['assignments']) > 0

    # Submit assignment
    sub_res = client.post('/api/assignments/submit', json={
        'assignment_id': 1,
        'student_id': 'SB2026',
        'content': 'https://github.com/sairajbhandalkar61-ctrl/lab-submission'
    })
    assert sub_res.status_code == 201

def test_notices_and_summarize(client):
    res = client.get('/api/notices')
    assert res.status_code == 200
    assert len(res.get_json()['notices']) > 0

    sum_res = client.get('/api/notices/summarize')
    assert sum_res.status_code == 200
    assert 'summary' in sum_res.get_json()

# 9. Grievances Desk
def test_grievances_flow(client):
    post_res = client.post('/api/grievances', json={
        'student_id': 'SB2026',
        'category': 'Academic',
        'subject': 'Syllabus coverage query',
        'description': 'Requesting additional lab sessions for neural network module.'
    })
    assert post_res.status_code == 201
    assert 'ticket_number' in post_res.get_json()['grievance']

    get_res = client.get('/api/grievances?student_id=SB2026')
    assert get_res.status_code == 200
    assert len(get_res.get_json()['grievances']) > 0

# 10. Faculty & Admin Dashboards
def test_faculty_dashboard(client):
    res = client.get('/api/faculty/dashboard?employee_id=FAC101')
    assert res.status_code == 200
    data = res.get_json()
    assert data['faculty']['name'] == 'Dr. Rajesh Sharma'
    assert 'classes' in data

def test_admin_overview_and_system(client):
    res = client.get('/api/admin/overview')
    assert res.status_code == 200
    data = res.get_json()
    assert data['metrics']['total_students'] >= 1
    assert data['status'] == 'Operational'

    sys_res = client.get('/api/admin/system')
    assert sys_res.status_code == 200
    sys_data = sys_res.get_json()
    assert sys_data['system_status'] == 'Healthy'
    assert sys_data['database_status'] == 'Connected'
