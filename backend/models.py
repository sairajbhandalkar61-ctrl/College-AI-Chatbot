from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import db

# 1. User & Authentication
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student', 'faculty', 'admin'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    # Relationships
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    faculty_profile = db.relationship('FacultyProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    conversations = db.relationship('ChatbotConversation', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 2. Student Profile
class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    student_id = db.Column(db.String(40), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(100), default='B.Tech Computer Science')
    semester = db.Column(db.String(20), default='Semester 5')
    department = db.Column(db.String(100), default='Computer Science & Engineering')
    academic_year = db.Column(db.String(20), default='2026-2027')
    avatar_url = db.Column(db.String(255), default='/static/images/default_avatar.png')
    phone = db.Column(db.String(30), nullable=True)
    attendance_rate = db.Column(db.Float, default=85.0)
    cgpa = db.Column(db.Float, default=8.2)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    attendance_records = db.relationship('AttendanceRecord', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    academic_results = db.relationship('AcademicResult', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    submissions = db.relationship('AssignmentSubmission', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    grievances = db.relationship('GrievanceTicket', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    achievements = db.relationship('Achievement', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    study_recommendations = db.relationship('StudyRecommendation', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    study_plans = db.relationship('StudyPlan', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    weekly_reports = db.relationship('WeeklySuccessReport', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    career_profile = db.relationship('CareerProfile', backref='student', uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'course': self.course,
            'semester': self.semester,
            'department': self.department,
            'academic_year': self.academic_year,
            'avatar_url': self.avatar_url,
            'attendance_rate': self.attendance_rate,
            'cgpa': self.cgpa
        }

# 3. Faculty Profile
class FacultyProfile(db.Model):
    __tablename__ = 'faculty_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    employee_id = db.Column(db.String(40), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(100), default='Computer Science & Engineering')
    designation = db.Column(db.String(80), default='Assistant Professor')
    office_room = db.Column(db.String(50), default='Lab 402')
    phone = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    # Relationships
    sessions = db.relationship('AttendanceSession', backref='faculty', lazy='dynamic')
    assignments = db.relationship('Assignment', backref='faculty', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'name': self.name,
            'department': self.department,
            'designation': self.designation,
            'office_room': self.office_room
        }

# 4. Academic Structure: Departments, Courses, Subjects
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    courses = db.relationship('Course', backref='department', lazy='dynamic')

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    degree = db.Column(db.String(50), default='B.Tech')
    duration_years = db.Column(db.Integer, default=4)
    subjects = db.relationship('Subject', backref='course', lazy='dynamic')

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    semester = db.Column(db.String(20), default='Semester 5')
    credits = db.Column(db.Integer, default=4)
    enrollments = db.relationship('Enrollment', backref='subject', lazy='dynamic')
    sessions = db.relationship('AttendanceSession', backref='subject', lazy='dynamic')
    assignments = db.relationship('Assignment', backref='subject', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'semester': self.semester,
            'credits': self.credits
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    semester = db.Column(db.String(20), default='Semester 5')
    academic_year = db.Column(db.String(20), default='2026-2027')
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

# 5. Attendance Management
class AttendanceSession(db.Model):
    __tablename__ = 'attendance_sessions'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_profiles.id'), nullable=True)
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.String(20), default='09:00 AM')
    topic = db.Column(db.String(150), default='Regular Lecture')
    session_type = db.Column(db.String(30), default='Theory')  # Theory / Lab
    records = db.relationship('AttendanceRecord', backref='session', lazy='dynamic', cascade="all, delete-orphan")

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('attendance_sessions.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), default='Present')  # Present / Absent / Late
    method = db.Column(db.String(30), default='FaceLock AI')  # FaceLock AI / Fingerprint Biometric / Manual
    verified_at = db.Column(db.DateTime, default=datetime.utcnow)

# 6. Academic Results & Analytics
class AcademicResult(db.Model):
    __tablename__ = 'academic_results'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    exam_type = db.Column(db.String(50), default='Midterm Exam')  # Internal, Midterm, Final, Lab
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, default=100.0)
    grade = db.Column(db.String(10), default='A')
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship('Subject', backref='academic_results')

    def to_dict(self):
        return {
            'id': self.id,
            'subject_code': self.subject.code if self.subject else 'N/A',
            'subject_name': self.subject.name if self.subject else 'N/A',
            'exam_type': self.exam_type,
            'score': self.score,
            'max_score': self.max_score,
            'percentage': round((self.score / max(1.0, self.max_score)) * 100, 1),
            'grade': self.grade
        }

# 7. Assignments & Submissions
class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_profiles.id'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    max_marks = db.Column(db.Float, default=50.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('AssignmentSubmission', backref='assignment', lazy='dynamic', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'subject_code': self.subject.code if self.subject else 'N/A',
            'subject_name': self.subject.name if self.subject else 'N/A',
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.strftime("%Y-%m-%d %I:%M %p") if self.due_date else None,
            'max_marks': self.max_marks
        }

class AssignmentSubmission(db.Model):
    __tablename__ = 'assignment_submissions'
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(30), default='Submitted')  # Pending, Submitted, Late, Evaluated
    marks = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.Text, nullable=True)

# 8. Institutional Notices
class Notice(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='Academic')  # Academic, Examination, Placement, Events, Admin
    target_audience = db.Column(db.String(50), default='All Students')
    file_url = db.Column(db.String(255), nullable=True)
    is_pinned = db.Column(db.Boolean, default=False)
    published_by = db.Column(db.String(100), default='Campus Dean')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'target_audience': self.target_audience,
            'is_pinned': self.is_pinned,
            'published_by': self.published_by,
            'date': self.created_at.strftime("%b %d, %Y") if self.created_at else ''
        }

# 9. Timetable & Examinations
class TimetableEntry(db.Model):
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty_profiles.id'), nullable=True)
    day_of_week = db.Column(db.String(15), nullable=False)  # Monday, Tuesday, ...
    start_time = db.Column(db.String(15), nullable=False)  # 09:00 AM
    end_time = db.Column(db.String(15), nullable=False)    # 10:00 AM
    room_number = db.Column(db.String(30), default='Auditorium 2B')

    subject = db.relationship('Subject', backref='timetable_entries')
    faculty = db.relationship('FacultyProfile', backref='timetable_entries')

    def to_dict(self):
        return {
            'id': self.id,
            'subject_code': self.subject.code if self.subject else 'N/A',
            'subject_name': self.subject.name if self.subject else 'N/A',
            'day': self.day_of_week,
            'time': f"{self.start_time} - {self.end_time}",
            'room': self.room_number
        }

class Examination(db.Model):
    __tablename__ = 'examinations'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(15), default='10:00 AM')
    end_time = db.Column(db.String(15), default='01:00 PM')
    room_number = db.Column(db.String(30), default='Hall A')
    exam_type = db.Column(db.String(50), default='End Semester Final')

    subject = db.relationship('Subject', backref='examinations')

# 10. Grievance Helpdesk
class GrievanceTicket(db.Model):
    __tablename__ = 'grievance_tickets'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(30), unique=True, nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.String(50), default='Academic')  # Academic, Examination, Technical, Admin, Infrastructure
    subject = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='Medium')  # Low, Medium, High, Urgent
    status = db.Column(db.String(30), default='Open')      # Open, In Progress, Resolved, Closed
    resolution = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'category': self.category,
            'subject': self.subject,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'resolution': self.resolution,
            'date': self.created_at.strftime("%b %d, %Y") if self.created_at else ''
        }

Grievance = GrievanceTicket

# 11. Notifications
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), default='general')  # attendance, assignment, exam, notice, success
    link = db.Column(db.String(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'category': self.category,
            'link': self.link,
            'is_read': self.is_read,
            'timestamp': self.created_at.strftime("%I:%M %p, %b %d") if self.created_at else ''
        }

# 12. Chatbot Conversations & Messages
class ChatbotConversation(db.Model):
    __tablename__ = 'chatbot_conversations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    title = db.Column(db.String(120), default='New Chat')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship('ChatbotMessage', backref='conversation', lazy='dynamic', cascade="all, delete-orphan")

class ChatbotMessage(db.Model):
    __tablename__ = 'chatbot_messages'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('chatbot_conversations.id', ondelete='CASCADE'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'ai'
    message = db.Column(db.Text, nullable=False)
    intent_tag = db.Column(db.String(80), nullable=True)
    action_data = db.Column(db.Text, nullable=True)  # JSON serialized action
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 13. RAG Knowledge Documents
class KnowledgeDocument(db.Model):
    __tablename__ = 'knowledge_documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    filename = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), default='Handbook')  # Handbook, Syllabus, Policies, Guidelines
    file_path = db.Column(db.String(255), nullable=False)
    num_chunks = db.Column(db.Integer, default=0)
    uploaded_by = db.Column(db.String(80), default='Administrator')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 14. Career & O*NET Profiles
class CareerProfile(db.Model):
    __tablename__ = 'career_profiles'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), unique=True, nullable=False)
    skills_json = db.Column(db.Text, default='[]')
    interests_json = db.Column(db.Text, default='[]')
    target_role = db.Column(db.String(100), default='Machine Learning Engineer')
    resume_path = db.Column(db.String(255), nullable=True)
    resume_skills_json = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 15. AI Student Success Advisor (Descriptive, Predictive, Prescriptive)
class StudyRecommendation(db.Model):
    __tablename__ = 'study_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    issue = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    suggested_action = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='High')  # High, Medium, Low
    estimated_effort_mins = db.Column(db.Integer, default=45)
    category = db.Column(db.String(50), default='Revision')
    status = db.Column(db.String(30), default='Pending')  # Pending, In Progress, Completed, Dismissed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'issue': self.issue,
            'reason': self.reason,
            'suggested_action': self.suggested_action,
            'priority': self.priority,
            'effort_mins': self.estimated_effort_mins,
            'category': self.category,
            'status': self.status,
            'created_at': self.created_at.strftime("%b %d") if self.created_at else ''
        }

class StudyPlan(db.Model):
    __tablename__ = 'study_plans'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    weekly_goal = db.Column(db.String(255), default='Master Graph Algorithms & complete Cloud Lab')
    tasks = db.relationship('StudyPlanTask', backref='plan', lazy='dynamic', cascade="all, delete-orphan")

class StudyPlanTask(db.Model):
    __tablename__ = 'study_plan_tasks'
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('study_plans.id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(db.String(15), default='Monday')
    task_title = db.Column(db.String(200), nullable=False)
    subject_code = db.Column(db.String(30), default='CS501')
    duration_mins = db.Column(db.Integer, default=45)
    is_completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day_of_week,
            'title': self.task_title,
            'subject_code': self.subject_code,
            'duration_mins': self.duration_mins,
            'is_completed': self.is_completed,
            'status': 'Completed' if self.is_completed else 'Pending'
        }

class RecommendationFeedback(db.Model):
    __tablename__ = 'recommendation_feedback'
    id = db.Column(db.Integer, primary_key=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('study_recommendations.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    feedback_type = db.Column(db.String(30), nullable=False)  # Helpful, Completed, Irrelevant
    comments = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    badge_name = db.Column(db.String(100), nullable=False)
    badge_category = db.Column(db.String(50), default='Attendance')
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50), default='award')
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'badge_name': self.badge_name,
            'badge_category': self.badge_category,
            'description': self.description,
            'icon': self.icon,
            'awarded_date': self.awarded_at.strftime("%b %d, %Y") if self.awarded_at else ''
        }

class WeeklySuccessReport(db.Model):
    __tablename__ = 'weekly_success_reports'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    attendance_summary = db.Column(db.String(255), nullable=False)
    subjects_improved = db.Column(db.String(255), nullable=True)
    subjects_needing_attention = db.Column(db.String(255), nullable=True)
    report_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'week_number': self.week_number,
            'attendance_summary': self.attendance_summary,
            'subjects_improved': self.subjects_improved,
            'subjects_needing_attention': self.subjects_needing_attention,
            'created_at': self.created_at.strftime("%b %d, %Y") if self.created_at else ''
        }
