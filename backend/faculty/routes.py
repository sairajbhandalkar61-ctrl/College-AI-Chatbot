from flask import Blueprint, jsonify, request
from backend.database import db
from backend.models import FacultyProfile, Subject, Course, AttendanceSession, AttendanceRecord, StudentProfile, Assignment, AssignmentSubmission, AcademicResult
from datetime import datetime, date

faculty_bp = Blueprint('faculty', __name__, url_prefix='/api/faculty')

@faculty_bp.route('/dashboard', methods=['GET'])
def get_faculty_dashboard():
    # Find default or requested faculty
    emp_id = request.args.get('employee_id', 'FAC101')
    faculty = FacultyProfile.query.filter_by(employee_id=emp_id).first()
    if not faculty:
        faculty = FacultyProfile.query.first()
    
    if not faculty:
        return jsonify({'error': 'No faculty profile found'}), 404

    # Get subjects taught or general college subjects
    subjects = Subject.query.all()
    sessions = AttendanceSession.query.filter_by(faculty_id=faculty.id).all()
    assignments = Assignment.query.filter_by(faculty_id=faculty.id).all()
    
    total_students = StudentProfile.query.count()
    total_sessions = len(sessions)
    total_assignments = len(assignments)

    return jsonify({
        'faculty': faculty.to_dict(),
        'overview': {
            'total_students_enrolled': total_students,
            'total_sessions_conducted': total_sessions,
            'active_assignments': total_assignments,
            'department': faculty.department
        },
        'classes': [s.to_dict() for s in subjects],
        'recent_assignments': [a.to_dict() for a in assignments[:5]]
    })

@faculty_bp.route('/classes', methods=['GET'])
def list_faculty_classes():
    subjects = Subject.query.all()
    return jsonify({
        'classes': [s.to_dict() for s in subjects]
    })

@faculty_bp.route('/attendance/sessions', methods=['GET', 'POST'])
def handle_attendance_sessions():
    if request.method == 'POST':
        data = request.get_json() or {}
        subject_id = data.get('subject_id')
        faculty_id = data.get('faculty_id', 1)
        topic = data.get('topic', 'Class Lecture')
        session_type = data.get('session_type', 'Theory')
        time_slot = data.get('session_time', '10:00 AM')

        if not subject_id:
            return jsonify({'error': 'subject_id is required'}), 400

        new_session = AttendanceSession(
            subject_id=subject_id,
            faculty_id=faculty_id,
            session_date=date.today(),
            session_time=time_slot,
            topic=topic,
            session_type=session_type
        )
        db.session.add(new_session)
        db.session.commit()

        # If student attendance list provided, record it
        students_marked = data.get('records', [])
        for rec in students_marked:
            st = StudentProfile.query.filter_by(student_id=rec.get('student_id')).first()
            if st:
                db.session.add(AttendanceRecord(
                    session_id=new_session.id,
                    student_id=st.id,
                    status=rec.get('status', 'Present'),
                    method=rec.get('method', 'Faculty Manual')
                ))
        db.session.commit()

        return jsonify({
            'message': 'Attendance session recorded successfully',
            'session_id': new_session.id
        }), 201

    # GET: return recent sessions
    sessions = AttendanceSession.query.order_by(AttendanceSession.id.desc()).limit(20).all()
    out = []
    for s in sessions:
        out.append({
            'id': s.id,
            'subject_code': s.subject.code if s.subject else 'N/A',
            'subject_name': s.subject.name if s.subject else 'N/A',
            'date': s.session_date.isoformat(),
            'time': s.session_time,
            'topic': s.topic,
            'type': s.session_type,
            'attendees': s.records.filter_by(status='Present').count()
        })
    return jsonify({'sessions': out})

@faculty_bp.route('/grades', methods=['POST'])
def submit_student_grade():
    data = request.get_json() or {}
    student_id_str = data.get('student_id')
    subject_code = data.get('subject_code')
    score = data.get('score')
    exam_type = data.get('exam_type', 'Midterm')

    if not student_id_str or not subject_code or score is None:
        return jsonify({'error': 'student_id, subject_code, and score are required'}), 400

    student = StudentProfile.query.filter_by(student_id=student_id_str).first()
    subject = Subject.query.filter_by(code=subject_code).first()

    if not student or not subject:
        return jsonify({'error': 'Invalid student or subject'}), 404

    # Determine grade
    try:
        score_val = float(score)
    except ValueError:
        return jsonify({'error': 'Invalid score value'}), 400

    grade = 'F'
    if score_val >= 90: grade = 'A+'
    elif score_val >= 80: grade = 'A'
    elif score_val >= 70: grade = 'B'
    elif score_val >= 60: grade = 'C'
    elif score_val >= 50: grade = 'D'

    result = AcademicResult(
        student_id=student.id,
        subject_id=subject.id,
        exam_type=exam_type,
        score=score_val,
        max_score=100.0,
        grade=grade
    )
    db.session.add(result)
    db.session.commit()

    return jsonify({
        'message': 'Academic grade recorded successfully',
        'result': result.to_dict()
    }), 201
