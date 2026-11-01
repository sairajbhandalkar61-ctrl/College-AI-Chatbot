from flask import Blueprint, request, jsonify, session
from backend.models import User, StudentProfile
from backend.database import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    identifier = data.get('username') or data.get('email', '')
    password = data.get('password', '')

    if not identifier or not password:
        return jsonify({'success': False, 'message': 'Username/email and password required.'}), 400

    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid credentials. Please verify username and password.'}), 401

    session['user_id'] = user.id
    session['role'] = user.role

    # Profile info
    profile_data = {}
    if user.role == 'student' and user.student_profile:
        profile_data = user.student_profile.to_dict()
    elif user.role == 'faculty' and user.faculty_profile:
        profile_data = user.faculty_profile.to_dict()

    return jsonify({
        'success': True,
        'message': f'Logged in as {user.username}',
        'user': user.to_dict(),
        'profile': profile_data
    })

@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully.'})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            profile_data = {}
            if user.role == 'student' and user.student_profile:
                profile_data = user.student_profile.to_dict()
            elif user.role == 'faculty' and user.faculty_profile:
                profile_data = user.faculty_profile.to_dict()
            return jsonify({
                'authenticated': True,
                'user': user.to_dict(),
                'profile': profile_data
            })

    # Default demo student profile if no active session
    demo_user = User.query.filter_by(role='student').first()
    if demo_user:
        return jsonify({
            'authenticated': False,
            'is_demo': True,
            'user': demo_user.to_dict(),
            'profile': demo_user.student_profile.to_dict() if demo_user.student_profile else {}
        })

    return jsonify({'authenticated': False, 'user': None})

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    name = data.get('name', username)
    course = data.get('course', 'B.Tech Computer Science')

    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'Username, email and password are required.'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'success': False, 'message': 'Username or email already registered.'}), 409

    new_user = User(username=username, email=email, role='student')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.flush()

    new_student = StudentProfile(
        user_id=new_user.id,
        student_id=f"STU{new_user.id:04d}",
        name=name,
        course=course
    )
    db.session.add(new_student)
    db.session.commit()

    session['user_id'] = new_user.id
    session['role'] = new_user.role

    return jsonify({
        'success': True,
        'message': 'Account created successfully.',
        'user': new_user.to_dict(),
        'profile': new_student.to_dict()
    }), 201
