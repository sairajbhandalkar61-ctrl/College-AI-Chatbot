from flask import Blueprint, request, jsonify, session
from backend.services.career_service import career_engine
from backend.models import CareerProfile, StudentProfile
from backend.database import db
import json

career_bp = Blueprint('career', __name__, url_prefix='/api/career')

def _get_student():
    user_id = session.get('user_id')
    if user_id:
        s = StudentProfile.query.filter_by(user_id=user_id).first()
        if s:
            return s
    return StudentProfile.query.filter_by(student_id='SB2026').first()

@career_bp.route('/profile', methods=['GET', 'POST'])
def manage_career_profile():
    student = _get_student()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    profile = CareerProfile.query.filter_by(student_id=student.id).first()

    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        skills = data.get('skills', [])
        target_role = data.get('target_role', 'Machine Learning Engineer')
        interests = data.get('interests', [])

        if not profile:
            profile = CareerProfile(student_id=student.id)
            db.session.add(profile)

        profile.skills_json = json.dumps(skills)
        profile.target_role = target_role
        profile.interests_json = json.dumps(interests)
        db.session.commit()

        matches = career_engine.match_career_roles(skills)
        return jsonify({
            'success': True,
            'message': 'Career profile updated successfully.',
            'matches': matches
        })

    # GET
    skills = json.loads(profile.skills_json) if profile and profile.skills_json else ['Python', 'SQL', 'Machine Learning', 'Data Structures', 'Flask']
    target_role = profile.target_role if profile else 'Machine Learning Engineer'
    matches = career_engine.match_career_roles(skills)

    return jsonify({
        'student_name': student.name,
        'student_id': student.student_id,
        'skills': skills,
        'target_role': target_role,
        'career_matches': matches,
        'onet_taxonomy_loaded': len(career_engine.occupation_skills) > 0
    })

@career_bp.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    data = request.get_json(silent=True) or {}
    resume_text = data.get('resume_text', '')

    if not resume_text or len(resume_text.strip()) < 30:
        return jsonify({'error': 'Please provide resume text content (at least 30 characters) for NLP analysis.'}), 400

    extracted_skills = career_engine.extract_skills_from_text(resume_text)
    matches = career_engine.match_career_roles(extracted_skills)

    # Specific feedback
    top_role = matches[0] if matches else None
    suggestions = [
        "Include quantifiable project metrics (e.g. 'improved latency by 25%' or 'trained on 20,000 records').",
        f"Strengthen alignment with {top_role['role'] if top_role else 'target roles'} by adding showcase projects."
    ]
    if top_role and top_role.get('missing_skills'):
        suggestions.append(f"Acquire missing core technologies: {', '.join(top_role['missing_skills'][:3])}.")

    return jsonify({
        'extracted_skills': extracted_skills,
        'total_skills_identified': len(extracted_skills),
        'top_matching_role': top_role['role'] if top_role else 'Software Engineer',
        'match_percentage': top_role['match_percentage'] if top_role else 75.0,
        'target_match': top_role if top_role else {'role': 'Software Engineer', 'match_percentage': 75.0},
        'career_matches': matches,
        'improvement_suggestions': suggestions
    })

@career_bp.route('/occupations', methods=['GET'])
def get_occupations():
    roles = career_engine.match_career_roles(['Python', 'SQL', 'Machine Learning', 'Data Structures', 'Docker'])
    return jsonify({'roles': roles})
