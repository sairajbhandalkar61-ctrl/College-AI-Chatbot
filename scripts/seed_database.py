import os
import sys
from datetime import datetime, date, timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from flask import Flask
from backend.config import Config
from backend.database import db
from backend.models import (
    User, StudentProfile, FacultyProfile, Department, Course, Subject,
    Enrollment, AttendanceSession, AttendanceRecord, AcademicResult,
    Assignment, AssignmentSubmission, Notice, TimetableEntry, Examination,
    GrievanceTicket, Notification, ChatbotConversation, ChatbotMessage,
    KnowledgeDocument, CareerProfile, StudyRecommendation, StudyPlan,
    StudyPlanTask, Achievement, WeeklySuccessReport
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def seed():
    app = create_app()
    with app.app_context():
        print("Dropping and recreating database tables...")
        db.drop_all()
        db.create_all()
        print("Tables created cleanly.")

        # 1. Seed Users
        student_user = User(username='student', email='student@cortex.edu', role='student')
        student_user.set_password('Student@123')

        sairaj_user = User(username='sairaj', email='sairaj@cortex.edu', role='student')
        sairaj_user.set_password('password123')

        faculty_user = User(username='faculty', email='faculty@cortex.edu', role='faculty')
        faculty_user.set_password('Faculty@123')

        admin_user = User(username='admin', email='admin@cortex.edu', role='admin')
        admin_user.set_password('Admin@123')

        db.session.add_all([student_user, sairaj_user, faculty_user, admin_user])
        db.session.commit()

        # 2. Profiles
        student_prof = StudentProfile(
            user_id=sairaj_user.id,
            student_id='SB2026',
            name='Sairaj Bhandalkar',
            course='B.Tech Computer Science',
            semester='Semester 5',
            department='Computer Science & Engineering',
            academic_year='2026-2027',
            attendance_rate=87.8,
            cgpa=8.45,
            phone='+91 9876543210'
        )

        faculty_prof = FacultyProfile(
            user_id=faculty_user.id,
            employee_id='FAC101',
            name='Dr. Rajesh Sharma',
            department='Computer Science & Engineering',
            designation='Associate Professor',
            office_room='Cabin 304, Turing Block',
            phone='+91 9123456780'
        )

        db.session.add_all([student_prof, faculty_prof])
        db.session.commit()

        # 3. Department, Course, Subjects
        dept = Department(code='CSE', name='Computer Science & Engineering')
        db.session.add(dept)
        db.session.commit()

        course = Course(department_id=dept.id, code='CS_BTECH', title='B.Tech Computer Science', degree='B.Tech', duration_years=4)
        db.session.add(course)
        db.session.commit()

        subjects_data = [
            ('CS501', 'Data Structures & Algorithms', 4),
            ('CS502', 'Machine Learning & Neural Networks', 4),
            ('CS503', 'Cloud Architecture & Distributed Systems', 4),
            ('CS504', 'Database Management Systems', 3),
            ('CS505', 'Software Engineering & Agile Methodologies', 3)
        ]
        created_subjects = []
        for code, name, credits in subjects_data:
            subj = Subject(course_id=course.id, code=code, name=name, semester='Semester 5', credits=credits)
            db.session.add(subj)
            created_subjects.append(subj)
        db.session.commit()

        # Enroll student in all 5 subjects
        for subj in created_subjects:
            enr = Enrollment(student_id=student_prof.id, subject_id=subj.id, semester='Semester 5', academic_year='2026-2027')
            db.session.add(enr)
        db.session.commit()

        # 4. Academic Results
        scores = [
            (created_subjects[0].id, 'Midterm Exam', 68.0, 100.0, 'B'),  # CS501 weaker
            (created_subjects[1].id, 'Midterm Exam', 92.5, 100.0, 'A+'),
            (created_subjects[2].id, 'Midterm Exam', 84.0, 100.0, 'A'),
            (created_subjects[3].id, 'Midterm Exam', 88.0, 100.0, 'A'),
            (created_subjects[4].id, 'Midterm Exam', 79.0, 100.0, 'B+')
        ]
        for s_id, etype, score, max_s, grade in scores:
            res = AcademicResult(student_id=student_prof.id, subject_id=s_id, exam_type=etype, score=score, max_score=max_s, grade=grade)
            db.session.add(res)
        db.session.commit()

        # 5. Attendance Sessions & Records
        today = date.today()
        # Seed 10 sessions over past 2 weeks
        for i in range(10):
            sess_date = today - timedelta(days=(9 - i))
            subj = created_subjects[i % len(created_subjects)]
            session = AttendanceSession(
                subject_id=subj.id,
                faculty_id=faculty_prof.id,
                session_date=sess_date,
                session_time="09:00 AM" if i % 2 == 0 else "11:30 AM",
                topic=f"Lecture Unit { (i % 4) + 1 } Discussion",
                session_type="Theory" if i % 3 != 0 else "Lab"
            )
            db.session.add(session)
            db.session.flush()

            # Record for Sairaj
            rec = AttendanceRecord(
                session_id=session.id,
                student_id=student_prof.id,
                status="Present" if i != 3 else "Absent",
                method="FaceLock AI" if i % 2 == 0 else "Fingerprint Biometric",
                verified_at=datetime.combine(sess_date, datetime.min.time()) + timedelta(hours=9, minutes=4)
            )
            db.session.add(rec)
        db.session.commit()

        # 6. Assignments & Submissions
        a1 = Assignment(
            subject_id=created_subjects[0].id,
            faculty_id=faculty_prof.id,
            title="Assignment 3: Dynamic Programming Memoization & DAGs",
            description="Implement top-down and bottom-up DP solutions for 0/1 Knapsack and Longest Common Subsequence.",
            due_date=datetime.now() + timedelta(days=3, hours=4),
            max_marks=50.0
        )
        a2 = Assignment(
            subject_id=created_subjects[1].id,
            faculty_id=faculty_prof.id,
            title="Lab Project: Random Forest Classification Pipeline",
            description="Train and evaluate a multi-class random forest model on tabular callsets with Scikit-Learn.",
            due_date=datetime.now() - timedelta(days=2),
            max_marks=50.0
        )
        a3 = Assignment(
            subject_id=created_subjects[2].id,
            faculty_id=faculty_prof.id,
            title="Case Study: Microservices Architecture & Containerization",
            description="Submit architecture blueprint and Dockerfile for distributed campus ticketing system.",
            due_date=datetime.now() + timedelta(days=7),
            max_marks=40.0
        )
        db.session.add_all([a1, a2, a3])
        db.session.flush()

        # Submissions
        sub2 = AssignmentSubmission(
            assignment_id=a2.id,
            student_id=student_prof.id,
            status="Evaluated",
            marks=48.0,
            feedback="Excellent precision-recall tradeoff and modular preprocessing pipeline."
        )
        db.session.add(sub2)
        db.session.commit()

        # 7. Institutional Notices
        notices = [
            Notice(
                title="Midterm Examination Schedule (Winter 2026)",
                content="The semester 5 midterm examinations commence from December 8, 2026. Hall tickets available in student portal.",
                category="Examination",
                target_audience="All Students",
                is_pinned=True,
                published_by="Controller of Examinations"
            ),
            Notice(
                title="Google Cloud & AI Campus Hackathon 2026",
                content="Annual 36-hour hackathon for building autonomous campus intelligence workflows. Registrations close Nov 15.",
                category="Events",
                target_audience="B.Tech & MCA",
                is_pinned=True,
                published_by="Dean of Innovation"
            ),
            Notice(
                title="Campus Placement Drive: Top Tier Product Engineering Cohort",
                content="Leading engineering organizations visiting for SDE and Data Scientist interviews. Ensure resume profile is updated.",
                category="Placement",
                target_audience="Final & Pre-Final Year",
                is_pinned=False,
                published_by="Training & Placement Cell"
            )
        ]
        db.session.add_all(notices)

        # 8. Timetable
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for idx, day in enumerate(days):
            t1 = TimetableEntry(subject_id=created_subjects[idx % 5].id, faculty_id=faculty_prof.id, day_of_week=day, start_time="09:00 AM", end_time="10:30 AM", room_number="Turing Hall 401")
            t2 = TimetableEntry(subject_id=created_subjects[(idx + 1) % 5].id, faculty_id=faculty_prof.id, day_of_week=day, start_time="11:00 AM", end_time="12:30 PM", room_number="Compute Lab 3")
            db.session.add_all([t1, t2])
        db.session.commit()

        # 9. AI Student Success Advisor Seed (Descriptive, Predictive, Prescriptive)
        rec1 = StudyRecommendation(
            student_id=student_prof.id,
            issue="Data Structures & Algorithms (CS501) performance is 68%, lagging behind peer cohort (82%).",
            reason="Analysis of midterm assessment scores indicates difficulty in Graph Algorithms and Dynamic Programming.",
            suggested_action="Allocate 45 minutes daily to graph traversal problems and review the lecture notes on Dijkstra and BFS.",
            priority="High",
            estimated_effort_mins=45,
            category="Revision",
            status="In Progress"
        )
        rec2 = StudyRecommendation(
            student_id=student_prof.id,
            issue="Pending submission for Dynamic Programming Memoization assignment due in 3 days.",
            reason="Completing this assignment reinforces the conceptual gap identified in the recent test.",
            suggested_action="Review top-down memoization code template and submit implementation.",
            priority="High",
            estimated_effort_mins=60,
            category="Assignment",
            status="Pending"
        )
        rec3 = StudyRecommendation(
            student_id=student_prof.id,
            issue="Morning travel commute (35 mins) risk factor detected by ML Attendance Predictor.",
            reason="Students with >30 min commute experience an 8% higher absenteeism probability in first-period lectures.",
            suggested_action="Adjust sleep schedule to achieve 7.5 hours rest; target departing 15 minutes earlier to safeguard attendance.",
            priority="Medium",
            estimated_effort_mins=15,
            category="Habits",
            status="Pending"
        )
        db.session.add_all([rec1, rec2, rec3])
        db.session.commit()

        # 10. Study Plan
        plan = StudyPlan(student_id=student_prof.id, week_start=today, weekly_goal="Master Dynamic Programming & achieve 90% attendance across all labs")
        db.session.add(plan)
        db.session.flush()

        tasks = [
            StudyPlanTask(plan_id=plan.id, day_of_week="Monday", task_title="Revise 0/1 Knapsack Top-Down vs Bottom-Up", subject_code="CS501", duration_mins=45, is_completed=True),
            StudyPlanTask(plan_id=plan.id, day_of_week="Tuesday", task_title="Solve 3 LeetCode Medium DP problems", subject_code="CS501", duration_mins=60, is_completed=True),
            StudyPlanTask(plan_id=plan.id, day_of_week="Wednesday", task_title="Complete Cloud Containerization Lab Dockerfile", subject_code="CS503", duration_mins=40, is_completed=False),
            StudyPlanTask(plan_id=plan.id, day_of_week="Thursday", task_title="Review Random Forest feature importances & tuning", subject_code="CS502", duration_mins=30, is_completed=False),
            StudyPlanTask(plan_id=plan.id, day_of_week="Friday", task_title="Practice SQL Window Functions & Subqueries", subject_code="CS504", duration_mins=45, is_completed=False)
        ]
        db.session.add_all(tasks)

        # 11. Achievements
        badges = [
            Achievement(student_id=student_prof.id, badge_name="Attendance Champion", badge_category="Attendance", description="Maintained above 85% attendance across all core subjects.", icon="shield-check"),
            Achievement(student_id=student_prof.id, badge_name="Biometric Pioneer", badge_category="Technology", description="Successfully authenticated attendance via FaceLock AI & WebAuthn.", icon="fingerprint"),
            Achievement(student_id=student_prof.id, badge_name="Consistent Learner", badge_category="Academic", description="Completed 5 consecutive daily study plan sessions.", icon="zap")
        ]
        db.session.add_all(badges)

        # 12. Notifications
        notifs = [
            Notification(user_id=student_user.id, title="Assignment Reminder", message="Dynamic Programming assignment due in 3 days.", category="assignment", link="/assignments"),
            Notification(user_id=student_user.id, title="Attendance Verified", message="Your attendance for Cloud Architecture was recorded via FaceLock AI.", category="attendance", link="/attendance"),
            Notification(user_id=student_user.id, title="Success Advisor Insight", message="New personalized study recommendation ready for review.", category="success", link="/advisor")
        ]
        db.session.add_all(notifs)

        # 13. Career Profile
        cprofile = CareerProfile(
            student_id=student_prof.id,
            skills_json='["Python", "Machine Learning", "SQL", "Flask", "Scikit-Learn", "Data Structures", "Docker"]',
            interests_json='["Artificial Intelligence", "Data Science", "Backend Development"]',
            target_role="Machine Learning Engineer"
        )
        db.session.add(cprofile)

        # 14. Grievance Ticket Example
        ticket = GrievanceTicket(
            ticket_id="GRV-2026-8812",
            student_id=student_prof.id,
            category="Academic",
            subject="Clarification regarding CS501 Midterm Question 4 Grading",
            description="Requested re-verification of question 4 (AVL tree rotation analysis) as partial marks were omitted.",
            priority="Medium",
            status="In Progress",
            resolution="Assigned to Dr. Rajesh Sharma for evaluation re-check."
        )
        db.session.add(ticket)

        db.session.commit()
        print("Database seeded with comprehensive production campus data successfully.")

if __name__ == '__main__':
    seed()
