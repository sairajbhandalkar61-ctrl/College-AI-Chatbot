import os
from flask import Flask, render_template, request, jsonify
from backend.config import Config
from backend.database import db

def create_app(config_class=Config):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from backend.auth.routes import auth_bp
    from backend.success_advisor.routes import success_advisor_bp
    from backend.attendance.routes import attendance_bp
    from backend.chatbot.routes import chatbot_bp
    from backend.rag.routes import rag_bp
    from backend.career.routes import career_bp
    from backend.academic.routes import academic_bp
    from backend.assignments.routes import assignments_bp
    from backend.timetable.routes import timetable_bp
    from backend.notices.routes import notices_bp
    from backend.grievances.routes import grievances_bp
    from backend.notifications.routes import notifications_bp
    from backend.students.routes import students_bp
    from backend.faculty.routes import faculty_bp
    from backend.admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(success_advisor_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(rag_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(academic_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(notices_bp)
    app.register_blueprint(grievances_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(admin_bp)

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    # Core Page Routes
    @app.route('/')
    def index():
        return render_template('cortex2.html')

    @app.route('/chatbot')
    def legacy_chatbot():
        return render_template('index.html')

    # Backwards compatibility legacy chat endpoint
    @app.route('/chat', methods=['POST'])
    def legacy_chat():
        from backend.services.chatbot_service import get_chatbot_service
        data = request.get_json() or {}
        message = data.get('message', '').strip()
        student_id = data.get('student_id', 'SB2026')
        service = get_chatbot_service()
        response = service.process_message(message, student_id=student_id)
        return jsonify(response)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            "status": "healthy",
            "service": "cortex-2.0-ecosystem",
            "platform": "CORTEX 2.0 – Intelligent Campus & Student Success Ecosystem",
            "models": {
                "chatbot_intent": "RandomForest (78 classes)",
                "attendance_risk": "RandomForest (20k records)",
                "academic_performance": "RandomForest (UCI student-mat)",
                "course_outcome": "RandomForest (OULAD)",
                "oos_detector": "LogisticRegression (CLINC150)"
            }
        }), 200

    return app
