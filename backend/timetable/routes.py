from flask import Blueprint, jsonify
from backend.models import TimetableEntry, Examination

timetable_bp = Blueprint('timetable', __name__, url_prefix='/api/timetable')

@timetable_bp.route('', methods=['GET'])
def get_timetable():
    entries = TimetableEntry.query.all()
    grouped = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': []
    }
    for e in entries:
        if e.day_of_week in grouped:
            grouped[e.day_of_week].append(e.to_dict())

    return jsonify({
        'schedule': grouped,
        'slots': [e.to_dict() for e in entries]
    })

@timetable_bp.route('/examinations', methods=['GET'])
def get_examinations():
    exams = Examination.query.all()
    res = []
    for e in exams:
        res.append({
            'id': e.id,
            'subject_code': e.subject.code if e.subject else '',
            'subject_name': e.subject.name if e.subject else '',
            'exam_date': e.exam_date.strftime("%B %d, %Y"),
            'time': f"{e.start_time} - {e.end_time}",
            'room': e.room_number,
            'exam_type': e.exam_type
        })
    return jsonify({'examinations': res})
