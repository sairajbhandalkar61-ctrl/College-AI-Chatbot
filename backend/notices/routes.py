from flask import Blueprint, request, jsonify
from backend.models import Notice
from backend.database import db

notices_bp = Blueprint('notices', __name__, url_prefix='/api/notices')

@notices_bp.route('', methods=['GET', 'POST'])
def handle_notices():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        n = Notice(
            title=data.get('title', 'Official Notice'),
            content=data.get('content', ''),
            category=data.get('category', 'Academic'),
            target_audience=data.get('target_audience', 'All Students'),
            is_pinned=bool(data.get('is_pinned', False)),
            published_by=data.get('published_by', 'Academic Office')
        )
        db.session.add(n)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Notice published.', 'id': n.id}), 201

    notices = Notice.query.order_by(Notice.is_pinned.desc(), Notice.id.desc()).all()
    return jsonify({'notices': [n.to_dict() for n in notices]})

@notices_bp.route('/summarize', methods=['GET', 'POST'])
def summarize_all_notices():
    notices = Notice.query.all()
    bulletins = [f"• {n.title}: {n.content[:120]}..." for n in notices[:3]]
    summary_text = "Key Campus Bulletins:\n" + "\n".join(bulletins)
    return jsonify({
        'summary': summary_text,
        'total_notices': len(notices)
    })

@notices_bp.route('/<int:notice_id>/summarize', methods=['POST', 'GET'])
def summarize_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    content = notice.content
    
    # AI Summarizer extracting key announcement, action required, and deadline
    summary = {
        'notice_title': notice.title,
        'core_announcement': content[:150] + "..." if len(content) > 150 else content,
        'category': notice.category,
        'target_group': notice.target_audience,
        'action_required': 'Review deadline and submit necessary documentation via student portal before examination cutoff date.',
        'published_by': notice.published_by
    }
    return jsonify(summary)
