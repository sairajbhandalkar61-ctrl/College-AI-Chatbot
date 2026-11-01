# CORTEX 2.0 • Complete RESTful API Reference
## Enterprise Endpoints for Students, Faculty, and Administrators

---

## 1. Authentication (`/api/auth`)

| Endpoint | Method | Payload | Response | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/auth/login` | `POST` | `{"username": str, "password": str}` | User object, role, profile | Validates credentials and initiates authenticated session. |
| `/api/auth/logout` | `POST` | None | `{"success": true}` | Clears session and revokes authentication. |
| `/api/auth/me` | `GET` | None | User metadata & active profile | Returns identity of currently logged-in actor. |

---

## 2. Chatbot Dialogue & RAG (`/api/chatbot`)

| Endpoint | Method | Payload | Response | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/chatbot/message` | `POST` | `{"message": str, "student_id": str}` | `{"response": str, "source": str, "intent": str}` | Analyzes query via 78 intents, CLINC150 OOS boundary, RAG vector retrieval, and live DB lookups. |
| `/chat` (Legacy) | `POST` | `{"message": str}` | Same as above | Backwards-compatible route for legacy UI widgets. |

---

## 3. Biometric Attendance (`/api/attendance`)

| Endpoint | Method | Payload | Response | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/attendance/status/<id>` | `GET` | None | Attendance rate, sessions, logs | Retrieves attendance percentage, compliance status, and history. |
| `/api/attendance/verify-face` | `POST` | `{"student_id": str, "image_data": str}` | `{"success": true, "token": str}` | Verifies facial presence from WebRTC camera snapshot. |
| `/api/attendance/verify-fingerprint` | `POST` | `{"student_id": str, "credential_id": str}` | `{"success": true, "student_name": str}` | Validates WebAuthn biometric hardware sensor token. |
| `/api/attendance/mark` | `POST` | `{"student_id": str, "method": str, "course": str}` | Updated attendance rate & timestamp | Commits verified biometric attendance to relational database. |
| `/api/attendance/predict` | `POST` | `{"study_hours": float, "sleep_hours": float, "travel_time_minutes": float}` | Probability, risk level, recommendation | Habit-based attendance risk evaluation from 20k ML model. |

---

## 4. AI Student Success Advisor (`/api/success`)

| Endpoint | Method | Payload | Response | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/success/dashboard` | `GET` | Query param: `?student_id=SB2026` | Descriptive stats, study plan, recommendations | Comprehensive learning analytics dashboard. |
| `/api/success/tasks/<id>` | `PATCH` | `{"status": "Completed"}` | Updated task dictionary | Marks weekly action plan tasks as completed or pending. |
| `/api/success/feedback` | `POST` | `{"recommendation_id": int, "feedback_type": str}` | Success acknowledgement | Records student feedback on prescriptive suggestions. |
| `/api/success/weekly-report` | `GET` | Query param: `?student_id=SB2026` | Weekly progress, trends, intervention flags | Comprehensive weekly success report. |

---

## 5. Academic Analytics & Predictors (`/api/academic`)

| Endpoint | Method | Payload | Response | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/academic/results` | `GET` | Query param: `?student_id=SB2026` | Subject scores, grades, percentages | Semester grade report. |
| `/api/academic/predict-grade` | `POST` | `{"G1": float, "G2": float, "studytime": int, "absences": int}` | `{"predicted_score": float, "letter_grade": str, "is_pass": bool}` | Predicts final $G_3$ score via UCI regression model. |
| `/api/academic/predict-outcome`| `POST` | `{"total_vle_clicks": int, "avg_score": float, "assessments_count": int}` | `{"predicted_outcome": str, "confidence": float}` | Predicts course outcome via OULAD classification model. |

---

## 6. Career & Resume Guidance (`/api/career`)

| Endpoint | Method | Payload | Response | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/career/profile` | `GET` / `POST`| `{"skills": list, "target_role": str}` | Role matches, taxonomy status | Manages student career profile and O*NET match percentages. |
| `/api/career/analyze-resume` | `POST` | `{"resume_text": str}` | Extracted skills, target role match, missing skills | Extracts skills and computes gaps against industry standards. |

---

## 7. Operational Campus APIs

- `/api/timetable`: Weekly class schedule and upcoming examinations.
- `/api/assignments`: Active coursework listing and submission endpoint (`/api/assignments/submit`).
- `/api/notices`: Institutional notices and automated AI summary (`/api/notices/summarize`).
- `/api/grievances`: Confidential grievance submission and ticket tracking.
- `/api/notifications`: Real-time system notifications and mark-as-read endpoints.
- `/api/faculty`: Faculty dashboard, class rosters, lecture session creation, and grading.
- `/api/admin`: Institutional metrics, student directory, and system health status (`/api/admin/system`).
