from flask import Blueprint, request, jsonify, session
from backend.models import GrievanceTicket, StudentProfile
from backend.database import db
import uuid
import re

grievances_bp = Blueprint('grievances', __name__, url_prefix='/api/grievances')

def _categorize_complaint(text):
    text_l = text.lower()
    if any(k in text_l for k in ['mark', 'grade', 'score', 'evaluat', 'exam', 'paper']):
        return 'Academic / Examination'
    if any(k in text_l for k in ['portal', 'login', 'wifi', 'password', 'server', 'system']):
        return 'Technical'
    if any(k in text_l for k in ['hostel', 'water', 'canteen', 'lab', 'room', 'bus']):
        return 'Infrastructure'
    if any(k in text_l for k in ['fee', 'receipt', 'refund', 'scholarship', 'certificate']):
        return 'Administration'
    return 'General Inquiry'

@grievances_bp.route('', methods=['GET', 'POST'])
def handle_grievances():
    student = StudentProfile.query.filter_by(student_id='SB2026').first()

    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        subject = data.get('subject', '').strip()
        desc = data.get('description', '').strip()
        cat = data.get('category') or _categorize_complaint(subject + " " + desc)

        if not subject or not desc:
            return jsonify({'error': 'Subject and description are required.'}), 400

        ticket_code = f"GRV-2026-{uuid.uuid4().hex[:4].upper()}"
        ticket = GrievanceTicket(
            ticket_id=ticket_code,
            student_id=student.id,
            category=cat,
            subject=subject,
            description=desc,
            priority=data.get('priority', 'Medium'),
            status='Open',
            resolution='Assigned to Student Welfare & Dean Office for initial review.'
        )
        db.session.add(ticket)
        db.session.commit()

        dict_rep = ticket.to_dict()
        dict_rep['ticket_number'] = ticket.ticket_id
        return jsonify({
            'success': True,
            'message': f'Grievance ticket {ticket_code} generated successfully.',
            'ticket': dict_rep,
            'grievance': dict_rep
        }), 201

    tickets = GrievanceTicket.query.filter_by(student_id=student.id).order_by(GrievanceTicket.id.desc()).all()
    ticket_list = []
    for t in tickets:
        d = t.to_dict()
        d['ticket_number'] = t.ticket_id
        ticket_list.append(d)
    return jsonify({'tickets': ticket_list, 'grievances': ticket_list})
