from flask import Blueprint, request, jsonify, session
from backend.models import Assignment, AssignmentSubmission, StudentProfile, Subject
from backend.database import db
from datetime import datetime, timedelta

assignments_bp = Blueprint('assignments', __name__, url_prefix='/api/assignments')

@assignments_bp.route('', methods=['GET', 'POST'])
def handle_assignments():
    student = StudentProfile.query.filter_by(student_id='SB2026').first()

    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        subject_id = data.get('subject_id') or Subject.query.first().id
        title = data.get('title', 'New Lab Assignment')
        desc = data.get('description', '')
        days = int(data.get('days_due', 7))

        assign = Assignment(
            subject_id=subject_id,
            title=title,
            description=desc,
            due_date=datetime.now() + timedelta(days=days),
            max_marks=float(data.get('max_marks', 50.0))
        )
        db.session.add(assign)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Assignment created.', 'id': assign.id}), 201

    # GET: return assignments with student submission status
    assignments = Assignment.query.order_by(Assignment.due_date.asc()).all()
    results = []
    for a in assignments:
        sub = AssignmentSubmission.query.filter_by(assignment_id=a.id, student_id=student.id).first() if student else None
        results.append({
            'id': a.id,
            'title': a.title,
            'subject_code': a.subject.code if a.subject else 'CS',
            'subject_name': a.subject.name if a.subject else 'General',
            'description': a.description,
            'due_date': a.due_date.strftime("%b %d, %Y (%I:%M %p)"),
            'is_overdue': datetime.now() > a.due_date,
            'status': sub.status if sub else 'Pending',
            'marks': sub.marks if sub else None,
            'max_marks': a.max_marks,
            'feedback': sub.feedback if sub else None
        })

    return jsonify({'assignments': results})

@assignments_bp.route('/submit', methods=['POST'])
@assignments_bp.route('/<int:assignment_id>/submit', methods=['POST'])
def submit_assignment(assignment_id=None):
    data = request.get_json(silent=True) or {}
    if assignment_id is None:
        assignment_id = data.get('assignment_id')
    
    student_id_str = data.get('student_id', 'SB2026')
    student = StudentProfile.query.filter_by(student_id=student_id_str).first()
    if not student:
        student = StudentProfile.query.filter_by(student_id='SB2026').first()

    assign = db.session.get(Assignment, assignment_id)
    if not assign:
        return jsonify({'error': 'Assignment not found'}), 404

    content = data.get('content') or data.get('file_url', 'submission_code.py')

    sub = AssignmentSubmission.query.filter_by(assignment_id=assign.id, student_id=student.id).first()
    if not sub:
        sub = AssignmentSubmission(assignment_id=assign.id, student_id=student.id)
        db.session.add(sub)

    sub.submitted_at = datetime.utcnow()
    sub.file_url = content
    sub.status = 'Submitted'
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Assignment "{assign.title}" submitted successfully.',
        'submission': sub.to_dict() if hasattr(sub, 'to_dict') else {'id': sub.id, 'status': 'Submitted'}
    }), 201
