from flask import Blueprint, request, jsonify, session
from backend.services.success_advisor_service import advisor_engine
from backend.models import (
    StudentProfile, StudyRecommendation, StudyPlan, StudyPlanTask,
    RecommendationFeedback, WeeklySuccessReport
)
from backend.database import db
from datetime import date

advisor_bp = Blueprint('advisor', __name__, url_prefix='/api/success')
success_advisor_bp = advisor_bp

def _get_student_id():
    # If user logged in, use their student_id
    user_id = session.get('user_id')
    if user_id:
        student = StudentProfile.query.filter_by(user_id=user_id).first()
        if student:
            return student.student_id
    # Default active demo student
    return 'SB2026'

@advisor_bp.route('/dashboard', methods=['GET'])
def get_advisor_dashboard():
    s_id = _get_student_id()
    desc = advisor_engine.get_descriptive_analytics(s_id)
    if not desc:
        return jsonify({'error': 'Student not found'}), 404

    preds = advisor_engine.get_predictive_insights(s_id)
    recs = advisor_engine.generate_recommendations(s_id)
    
    # Active study plan
    student = StudentProfile.query.filter_by(student_id=s_id).first()
    plan = StudyPlan.query.filter_by(student_id=student.id).order_by(StudyPlan.id.desc()).first()
    plan_tasks = [t.to_dict() for t in plan.tasks.all()] if plan else []

    # Next best action
    next_action = recs[0] if recs else {
        'suggested_action': 'Maintain your current study rhythm and review daily lecture notes.',
        'priority': 'Low',
        'effort_mins': 30
    }

    return jsonify({
        'student': desc,
        'predictions': preds,
        'recommendations': recs,
        'next_best_action': next_action,
        'study_plan': {
            'goal': plan.weekly_goal if plan else 'Consistent daily revision',
            'tasks': plan_tasks
        }
    })

@advisor_bp.route('/insights', methods=['GET'])
def get_insights():
    s_id = _get_student_id()
    desc = advisor_engine.get_descriptive_analytics(s_id)
    return jsonify(desc or {})

@advisor_bp.route('/predictions', methods=['GET', 'POST'])
def get_predictions():
    s_id = _get_student_id()
    study = 4.5
    sleep = 7.0
    travel = 30.0

    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        study = float(data.get('study_hours', 4.5))
        sleep = float(data.get('sleep_hours', 7.0))
        travel = float(data.get('travel_time_minutes', 30.0))

    preds = advisor_engine.get_predictive_insights(s_id, study, sleep, travel)
    return jsonify(preds or {})

@advisor_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    s_id = _get_student_id()
    recs = advisor_engine.generate_recommendations(s_id)
    return jsonify({'recommendations': recs})

@advisor_bp.route('/study-plan', methods=['GET', 'POST'])
def handle_study_plan():
    s_id = _get_student_id()
    student = StudentProfile.query.filter_by(student_id=s_id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        goal = data.get('goal', 'Achieve 85% score in midterm revisions')
        tasks = data.get('tasks', [])

        new_plan = StudyPlan(student_id=student.id, week_start=date.today(), weekly_goal=goal)
        db.session.add(new_plan)
        db.session.flush()

        for t in tasks:
            task = StudyPlanTask(
                plan_id=new_plan.id,
                day_of_week=t.get('day', 'Monday'),
                task_title=t.get('title', 'Study Session'),
                subject_code=t.get('subject_code', 'CS501'),
                duration_mins=t.get('duration_mins', 45),
                is_completed=False
            )
            db.session.add(task)
        db.session.commit()

        return jsonify({'success': True, 'message': 'New study plan activated.', 'plan_id': new_plan.id})

    # GET
    plan = StudyPlan.query.filter_by(student_id=student.id).order_by(StudyPlan.id.desc()).first()
    if not plan:
        return jsonify({'goal': 'No active study plan', 'tasks': []})

    return jsonify({
        'id': plan.id,
        'goal': plan.weekly_goal,
        'week_start': plan.week_start.isoformat(),
        'tasks': [t.to_dict() for t in plan.tasks.all()]
    })

@advisor_bp.route('/tasks/<int:task_id>', methods=['PATCH', 'POST'])
def toggle_task(task_id):
    task = db.session.get(StudyPlanTask, task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json(silent=True) or {}
    if 'status' in data:
        task.is_completed = (data.get('status') == 'Completed')
    elif 'is_completed' in data:
        task.is_completed = bool(data.get('is_completed'))
    else:
        task.is_completed = not task.is_completed
    db.session.commit()
    return jsonify({
        'success': True,
        'task': task.to_dict(),
        'task_id': task.id,
        'is_completed': task.is_completed
    })

@advisor_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json(silent=True) or {}
    rec_id = data.get('recommendation_id')
    ftype = data.get('feedback_type', 'Helpful')
    comments = data.get('comments', '')

    s_id = _get_student_id()
    student = StudentProfile.query.filter_by(student_id=s_id).first()

    if rec_id and student:
        fb = RecommendationFeedback(
            recommendation_id=rec_id,
            student_id=student.id,
            feedback_type=ftype,
            comments=comments
        )
        db.session.add(fb)
        
        # If user marked completed, update recommendation status
        if ftype == 'Completed':
            rec = StudyRecommendation.query.get(rec_id)
            if rec:
                rec.status = 'Completed'
        db.session.commit()

    return jsonify({'success': True, 'message': 'Thank you! Your feedback helps optimize future study recommendations.'})

@advisor_bp.route('/weekly-report', methods=['GET'])
def get_weekly_report():
    s_id = _get_student_id()
    desc = advisor_engine.get_descriptive_analytics(s_id)
    preds = advisor_engine.get_predictive_insights(s_id)

    report = {
        'student_name': desc['name'],
        'student_id': desc['student_id'],
        'date_generated': date.today().strftime("%B %d, %Y"),
        'attendance_rate': f"{desc['attendance_rate']}%",
        'attendance_status': 'Compliant' if desc['is_attendance_compliant'] else 'At Risk',
        'subjects_improved': 'Machine Learning & Neural Networks (92.5%)',
        'subjects_needing_attention': 'Data Structures & Algorithms (68.0%)',
        'overall_learning_health': desc['academic_health'],
        'forecasted_sgpa': preds['forecasted_sgpa'],
        'recommended_priorities': [
            'Dedicate 45 minutes daily to graph algorithms and tree rotations in CS501.',
            'Submit pending Dynamic Programming assignment on time.',
            'Target departing 15 minutes earlier to prevent commute fatigue in morning lectures.'
        ]
    }
    return jsonify(report)

@advisor_bp.route('/resources', methods=['GET'])
def get_recommended_resources():
    resources = [
        {
            'subject': 'Data Structures & Algorithms (CS501)',
            'title': 'Lecture Notes: Graph Traversal & Dijkstra Algorithm',
            'type': 'PDF Document',
            'duration': '25 min read',
            'url': '/static/docs/CS501_Graph_Algorithms.pdf'
        },
        {
            'subject': 'Data Structures & Algorithms (CS501)',
            'title': 'Interactive Practice: Dynamic Programming Knapsack Visualizer',
            'type': 'Coding Lab',
            'duration': '40 min exercise',
            'url': 'https://leetcode.com/problemset/all/'
        },
        {
            'subject': 'Machine Learning & Neural Networks (CS502)',
            'title': 'Slide Deck: Ensemble Methods & Random Forest Hyperparameter Tuning',
            'type': 'Presentation',
            'duration': '30 min review',
            'url': '/static/docs/CS502_Ensemble_Methods.pdf'
        },
        {
            'subject': 'Cloud Architecture & Distributed Systems (CS503)',
            'title': 'Laboratory Blueprint: Dockerfile & Microservices Containerization',
            'type': 'Lab Guide',
            'duration': '45 min lab',
            'url': '/static/docs/CS503_Docker_Lab.pdf'
        }
    ]
    return jsonify({'resources': resources})
