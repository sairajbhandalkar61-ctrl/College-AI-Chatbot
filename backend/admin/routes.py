from flask import Blueprint, jsonify, request
from backend.database import db
from backend.models import User, StudentProfile, FacultyProfile, Department, Course, Subject, Grievance, Notice, AttendanceSession, AcademicResult
import sys
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/overview', methods=['GET'])
def get_admin_overview():
    total_students = StudentProfile.query.count()
    total_faculty = FacultyProfile.query.count()
    total_courses = Course.query.count()
    total_departments = Department.query.count()
    pending_grievances = Grievance.query.filter_by(status='Pending').count()
    active_notices = Notice.query.filter_by(is_active=True).count()

    # Calculate average attendance across students
    students = StudentProfile.query.all()
    avg_attendance = 0.0
    if students:
        avg_attendance = round(sum(s.attendance_rate for s in students) / len(students), 1)

    return jsonify({
        'metrics': {
            'total_students': total_students,
            'total_faculty': total_faculty,
            'total_courses': total_courses,
            'total_departments': total_departments,
            'average_attendance_rate': avg_attendance,
            'pending_grievances': pending_grievances,
            'active_notices': active_notices
        },
        'status': 'Operational',
        'platform_version': 'CORTEX 2.0 Enterprise'
    })

@admin_bp.route('/students', methods=['GET'])
def list_students():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    query = request.args.get('q', '').strip()

    st_query = StudentProfile.query
    if query:
        st_query = st_query.filter(
            (StudentProfile.name.ilike(f'%{query}%')) | 
            (StudentProfile.student_id.ilike(f'%{query}%')) |
            (StudentProfile.course.ilike(f'%{query}%'))
        )

    students = st_query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        'total': students.total,
        'page': page,
        'pages': students.pages,
        'students': [s.to_dict() for s in students.items]
    })

@admin_bp.route('/faculty', methods=['GET'])
def list_faculty():
    faculty = FacultyProfile.query.all()
    return jsonify({
        'faculty': [f.to_dict() for f in faculty]
    })

@admin_bp.route('/system', methods=['GET'])
def get_system_health():
    from dataset_registry import DATASETS

    # Check model artifacts
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    models_dir = os.path.join(base_dir, 'model')
    
    models_status = {
        'chatbot_model.pkl': os.path.exists(os.path.join(models_dir, 'chatbot_model.pkl')),
        'vectorizer.pkl': os.path.exists(os.path.join(models_dir, 'vectorizer.pkl')),
        'attendance_model.pkl': os.path.exists(os.path.join(models_dir, 'attendance_model.pkl')),
        'academic_models.pkl': os.path.exists(os.path.join(models_dir, 'academic_models.pkl')),
        'oos_detector.pkl': os.path.exists(os.path.join(models_dir, 'oos_detector.pkl'))
    }

    return jsonify({
        'system_status': 'Healthy',
        'python_version': sys.version.split()[0],
        'models_available': models_status,
        'datasets_configured': len(DATASETS),
        'database_status': 'Connected'
    })
