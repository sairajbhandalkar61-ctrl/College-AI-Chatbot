from flask import Blueprint, jsonify
from backend.models import Notification, User
from backend.database import db

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notifications_bp.route('', methods=['GET'])
def get_notifications():
    user = User.query.filter_by(role='student').first()
    if not user:
        return jsonify({'notifications': []})

    notifs = Notification.query.filter_by(user_id=user.id).order_by(Notification.id.desc()).all()
    unread_count = sum(1 for n in notifs if not n.is_read)

    return jsonify({
        'unread_count': unread_count,
        'notifications': [n.to_dict() for n in notifs]
    })

@notifications_bp.route('/<int:notification_id>/read', methods=['POST', 'PATCH'])
def mark_read(notification_id):
    notif = Notification.query.get_or_404(notification_id)
    notif.is_read = True
    db.session.commit()
    return jsonify({'success': True, 'id': notif.id, 'is_read': True})

@notifications_bp.route('/mark-all-read', methods=['POST'])
def mark_all_read():
    user = User.query.filter_by(role='student').first()
    if user:
        Notification.query.filter_by(user_id=user.id).update({'is_read': True})
        db.session.commit()
    return jsonify({'success': True, 'message': 'All notifications marked as read.'})
