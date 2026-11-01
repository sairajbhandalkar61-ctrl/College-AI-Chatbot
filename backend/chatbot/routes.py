from flask import Blueprint, request, jsonify, session
from backend.services.chatbot_service import chatbot_engine
from backend.models import ChatbotConversation, ChatbotMessage, StudentProfile
from backend.database import db
import json

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

@chatbot_bp.route('/message', methods=['POST'])
def send_message():
    data = request.get_json(silent=True) or {}
    message_text = data.get('message', '').strip()
    language = data.get('language', 'en')
    conversation_id = data.get('conversation_id')

    if not message_text:
        return jsonify({'response': 'Please enter a message or question.'}), 400

    # Determine student ID
    user_id = session.get('user_id')
    student_id_str = 'SB2026'
    if user_id:
        student = StudentProfile.query.filter_by(user_id=user_id).first()
        if student:
            student_id_str = student.student_id

    # Process query
    result = chatbot_engine.process_query(message_text, student_id_str=student_id_str, language=language)

    # Persist message history if conversation_id is provided
    if conversation_id:
        conv = ChatbotConversation.query.get(conversation_id)
        if conv:
            msg_user = ChatbotMessage(conversation_id=conv.id, sender='user', message=message_text)
            msg_ai = ChatbotMessage(
                conversation_id=conv.id,
                sender='ai',
                message=result['response'],
                intent_tag=result.get('tag'),
                action_data=json.dumps(result.get('action')) if result.get('action') else None
            )
            db.session.add_all([msg_user, msg_ai])
            db.session.commit()

    return jsonify(result)

@chatbot_bp.route('/conversations', methods=['GET', 'POST'])
def manage_conversations():
    user_id = session.get('user_id')
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        title = data.get('title', 'New Chat')
        conv = ChatbotConversation(user_id=user_id, title=title)
        db.session.add(conv)
        db.session.commit()
        return jsonify({'id': conv.id, 'title': conv.title, 'created_at': conv.created_at.isoformat()}), 201

    # GET
    if user_id:
        convs = ChatbotConversation.query.filter_by(user_id=user_id).order_by(ChatbotConversation.id.desc()).all()
    else:
        convs = ChatbotConversation.query.order_by(ChatbotConversation.id.desc()).limit(10).all()

    return jsonify([{'id': c.id, 'title': c.title, 'created_at': c.created_at.strftime("%b %d, %I:%M %p")} for c in convs])
