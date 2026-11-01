from flask import Blueprint, jsonify, session
from backend.models import StudentProfile, Achievement, Notice, TimetableEntry, Assignment, AssignmentSubmission
from backend.services.success_advisor_service import advisor_engine
from datetime import datetime

students_bp = Blueprint('students', __name__, url_prefix='/api/students')

@students_bp.route('/dashboard', methods=['GET'])
def student_dashboard():
    student = StudentProfile.query.filter_by(student_id='SB2026').first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    # Analytics
    desc = advisor_engine.get_descriptive_analytics(student.student_id)
    preds = advisor_engine.get_predictive_insights(student.student_id)
    recs = advisor_engine.generate_recommendations(student.student_id)

    # Next class
    day_name = datetime.now().strftime("%A")
    if day_name in ['Saturday', 'Sunday']:
        day_name = 'Monday'
    today_classes = TimetableEntry.query.filter_by(day_of_week=day_name).all()

    # Pending assignments
    assignments = Assignment.query.order_by(Assignment.due_date.asc()).limit(3).all()
    pending_assignments = []
    for a in assignments:
        sub = AssignmentSubmission.query.filter_by(assignment_id=a.id, student_id=student.id).first()
        if not sub or sub.status == 'Pending':
            pending_assignments.append({
                'title': a.title,
                'subject': a.subject.name if a.subject else '',
                'due': a.due_date.strftime("%b %d, %I:%M %p")
            })

    # Latest notices
    notices = Notice.query.order_by(Notice.id.desc()).limit(3).all()

    # Achievements
    achievements = Achievement.query.filter_by(student_id=student.id).all()

    return jsonify({
        'student': student.to_dict(),
        'analytics': desc,
        'predictions': preds,
        'next_best_action': recs[0] if recs else None,
        'recommendations': recs,
        'today_classes': [c.to_dict() for c in today_classes],
        'pending_assignments': pending_assignments,
        'latest_notices': [n.to_dict() for n in notices],
        'achievements': [a.to_dict() for a in achievements]
    })
