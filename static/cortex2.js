
/* ==========================================================================
   OFFLINE / STATIC CDN HYDRATION FALLBACKS (For GitHub Pages & Static Hosts)
   ========================================================================== */
const OFFLINE_DATA = {
    overview: {
        attendance: '86.4%',
        cgpa: '8.45',
        pending_assignments: 2,
        risk: 'Low Risk'
    },
    study_plan: [
        { id: 1, title: 'Complete Neural Network Backpropagation Lab Notebook', subject_code: 'MCA-301', estimated_minutes: 45, status: 'Pending' },
        { id: 2, title: 'Review Distributed Database Partitioning & Sharding', subject_code: 'MCA-302', estimated_minutes: 60, status: 'Pending' },
        { id: 3, title: 'Containerize Flask Application with Docker & Compose', subject_code: 'MCA-303', estimated_minutes: 30, status: 'Completed' },
        { id: 4, title: 'Practice Graph BFS/DFS Technical Interview Problems', subject_code: 'CAREER', estimated_minutes: 50, status: 'Completed' }
    ],
    recommendations: [
        { type: 'Academic', priority: 'High', title: 'Deepen Neural Network Optimization', description: 'Review Chapter 4 on Adam and RMSprop learning rate schedulers before Friday\'s lab evaluation.' },
        { type: 'Attendance', priority: 'Medium', title: 'Maintain >75% in Cloud Computing', description: 'Attending the next 2 lectures will raise your subject attendance to 89%.' },
        { type: 'Career', priority: 'High', title: 'Add Docker & Kafka Competencies', description: 'Aligning these two skills increases your target AI Engineer role match from 82% to 94% on O*NET.' }
    ],
    attendance_logs: [
        { date: 'Nov 01, 2026', subject: 'Machine Learning Lab', method: 'FaceLock AI', status: 'Present' },
        { date: 'Oct 31, 2026', subject: 'Cloud Computing & DevOps', method: 'Fingerprint Sensor', status: 'Present' },
        { date: 'Oct 30, 2026', subject: 'Advanced Database Systems', method: 'FaceLock AI', status: 'Present' },
        { date: 'Oct 29, 2026', subject: 'Cyber Security & Forensics', method: 'FaceLock AI', status: 'Present' },
        { date: 'Oct 28, 2026', subject: 'Machine Learning Theory', method: 'Fingerprint Sensor', status: 'Present' }
    ],
    timetable: [
        { day: 'Monday', time_slot: '09:00 AM - 10:30 AM', subject_code: 'MCA-301', subject_name: 'Machine Learning', room: 'Turing Hall 401', faculty_name: 'Dr. Rajesh Sharma' },
        { day: 'Monday', time_slot: '11:00 AM - 12:30 PM', subject_code: 'MCA-302', subject_name: 'Cloud Computing', room: 'Room 204', faculty_name: 'Prof. Priya Patil' },
        { day: 'Tuesday', time_slot: '10:00 AM - 11:30 AM', subject_code: 'MCA-303', subject_name: 'Advanced Databases', room: 'Lab 101', faculty_name: 'Dr. Amit Kulkarni' },
        { day: 'Wednesday', time_slot: '09:00 AM - 10:30 AM', subject_code: 'MCA-301', subject_name: 'Machine Learning Lab', room: 'Lab 402', faculty_name: 'Dr. Rajesh Sharma' },
        { day: 'Thursday', time_slot: '01:30 PM - 03:00 PM', subject_code: 'MCA-304', subject_name: 'Software Architecture', room: 'Hall B', faculty_name: 'Dr. S. Joshi' },
        { day: 'Friday', time_slot: '11:00 AM - 12:30 PM', subject_code: 'MCA-302', subject_name: 'DevOps & CI/CD', room: 'Compute Lab 3', faculty_name: 'Prof. Priya Patil' }
    ],
    examinations: [
        { exam_name: 'Midterm 1: Machine Learning', subject_code: 'MCA-301', subject_name: 'Machine Learning', exam_date: 'December 08, 2026', time_slot: '10:00 AM - 01:00 PM', room: 'Turing Hall 401' },
        { exam_name: 'Midterm 2: Cloud Computing', subject_code: 'MCA-302', subject_name: 'Cloud Computing', exam_date: 'December 10, 2026', time_slot: '10:00 AM - 01:00 PM', room: 'Hall 204' },
        { exam_name: 'Midterm 3: Advanced Databases', subject_code: 'MCA-303', subject_name: 'Advanced Databases', exam_date: 'December 12, 2026', time_slot: '02:00 PM - 05:00 PM', room: 'Lab 101' }
    ],
    assignments: [
        { id: 1, title: 'Machine Learning Neural Network Lab Notebook', subject_code: 'MCA-301', subject_name: 'Machine Learning', due_date: 'Dec 05, 2026 (11:59 PM)', max_marks: 50, status: 'Pending' },
        { id: 2, title: 'Cloud Infrastructure Terraform Script', subject_code: 'MCA-302', subject_name: 'Cloud Computing', due_date: 'Dec 08, 2026 (11:59 PM)', max_marks: 50, status: 'Submitted' },
        { id: 3, title: 'SQL Query Optimization & Indexing', subject_code: 'MCA-303', subject_name: 'Advanced Databases', due_date: 'Dec 12, 2026 (11:59 PM)', max_marks: 50, status: 'Pending' }
    ],
    notices: [
        { title: 'Midterm Examination Schedule (Winter 2026)', category: 'Examination', published_at: '2 days ago', content: 'The semester 5 midterm examinations commence from December 8, 2026. Hall tickets available in student portal.' },
        { title: 'Google & Microsoft Campus Internship Registration Open', category: 'Placement', published_at: '3 days ago', content: 'Leading technology organizations visiting for SDE and Data Scientist interviews. Ensure resume profile is updated.' },
        { title: 'Campus AI & Cloud Hackathon 2026', category: 'Events', published_at: '5 days ago', content: 'Annual 36-hour hackathon for building autonomous campus intelligence workflows. Registrations close Nov 15.' }
    ],
    results: [
        { subject_code: 'MCA-301', subject_name: 'Machine Learning', exam_type: 'Midterm Exam', score: 92, max_score: 100, percentage: 92.0, grade: 'A+' },
        { subject_code: 'MCA-302', subject_name: 'Cloud Computing', exam_type: 'Midterm Exam', score: 88, max_score: 100, percentage: 88.0, grade: 'A' },
        { subject_code: 'MCA-303', subject_name: 'Advanced Databases', exam_type: 'Midterm Exam', score: 85, max_score: 100, percentage: 85.0, grade: 'A' },
        { subject_code: 'MCA-304', subject_name: 'Software Architecture', exam_type: 'Midterm Exam', score: 82, max_score: 100, percentage: 82.0, grade: 'B+' }
    ],
    grievances: [
        { ticket_number: 'GRV-2026-9F12', category: 'Academic', subject: 'Syllabus coverage query for Neural Networks', status: 'Resolved' },
        { ticket_number: 'GRV-2026-4A88', category: 'Infrastructure', subject: 'Lab 402 GPU compute environment access', status: 'In Progress' }
    ]
};

/* ==========================================================================
   CORTEX 2.0 • Client Controller & Reactive API Integration
   Connects all 15 Campus Intelligence Modules
   ========================================================================== */

let currentStudentId = 'SB2026';
let currentRole = 'student';
let mediaStream = null;

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initTheme();
    initRoleSelector();
    initChatbot();
    initNotifications();

    // Initial data hydration
    loadOverviewData();
    loadAttendanceData();
    loadTimetableData();
    loadAssignmentsData();
    loadNoticesData();
    loadGrievancesData();
    loadAdvisorData();
    loadAcademicData();
});

/* 1. NAVIGATION & TAB SWITCHING */
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item[data-tab]');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = item.getAttribute('data-tab');
            switchTab(tabId);
        });
    });

    // Mobile sidebar toggle
    const openBtn = document.getElementById('mobileSidebarOpen');
    const closeBtn = document.getElementById('mobileSidebarClose');
    const sidebar = document.getElementById('sidebar');

    if (openBtn && sidebar) {
        openBtn.addEventListener('click', () => sidebar.classList.add('open'));
    }
    if (closeBtn && sidebar) {
        closeBtn.addEventListener('click', () => sidebar.classList.remove('open'));
    }
}

function switchTab(tabId) {
    // Update nav items
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    const targetNav = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
    if (targetNav) targetNav.classList.add('active');

    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
    const targetPane = document.getElementById(`tab-${tabId}`);
    if (targetPane) targetPane.classList.add('active');

    // Update header titles
    const titles = {
        'overview': { title: 'Campus Overview', sub: 'Real-time student intelligence & predictive academic metrics' },
        'assistant': { title: 'AI Campus Assistant', sub: 'Ground truth RAG intelligence & NLP dialogue' },
        'advisor': { title: 'AI Student Success Advisor', sub: 'Prescriptive recommendations & study planning' },
        'attendance': { title: 'Biometric Attendance & ML Predictor', sub: 'FaceLock AI, WebAuthn sensor & habit risk model' },
        'academics': { title: 'Academic Analytics & Outcomes', sub: 'UCI performance model & OULAD predictions' },
        'career': { title: 'Career Guidance & Resume Intelligence', sub: 'O*NET taxonomy matching & skill gap analysis' },
        'timetable': { title: 'Class Timetable & Examination Schedule', sub: 'Weekly lectures & upcoming semester exams' },
        'assignments': { title: 'Coursework & Submissions', sub: 'Continuous evaluation & lab assignment tracking' },
        'notices': { title: 'Campus Notice Board', sub: 'Official bulletins & AI summaries' },
        'grievances': { title: 'Confidential Grievance Redressal', sub: 'Direct portal to student welfare committee' }
    };

    if (titles[tabId]) {
        document.getElementById('pageTitle').textContent = titles[tabId].title;
        document.getElementById('pageSubtitle').textContent = titles[tabId].sub;
    }

    // Close mobile drawer if open
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.remove('open');
}

/* 2. THEME SWITCHER */
function initTheme() {
    const toggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const savedTheme = localStorage.getItem('cortex_theme') || 'dark';

    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme, themeIcon);

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('cortex_theme', next);
            updateThemeIcon(next, themeIcon);
        });
    }
}

function updateThemeIcon(theme, iconEl) {
    if (!iconEl) return;
    if (theme === 'dark') {
        iconEl.className = 'fa-solid fa-moon';
    } else {
        iconEl.className = 'fa-solid fa-sun';
    }
}

/* 3. ROLE SELECTOR */
function initRoleSelector() {
    const selector = document.getElementById('roleSelector');
    if (!selector) return;

    selector.addEventListener('change', (e) => {
        currentRole = e.target.value;
        const nameEl = document.getElementById('userName');
        const subEl = document.getElementById('userSub');
        const badgeEl = document.getElementById('roleBadge');
        const heroName = document.getElementById('heroUserName');

        if (currentRole === 'student') {
            currentStudentId = 'SB2026';
            if (nameEl) nameEl.textContent = 'Sairaj Bhandalkar';
            if (subEl) subEl.textContent = 'SB2026 • MCA Data Science';
            if (badgeEl) badgeEl.textContent = 'Student';
            if (heroName) heroName.textContent = 'Sairaj';
            loadOverviewData();
        } else if (currentRole === 'faculty') {
            if (nameEl) nameEl.textContent = 'Dr. Rajesh Sharma';
            if (subEl) subEl.textContent = 'FAC101 • Computer Science';
            if (badgeEl) badgeEl.textContent = 'Faculty';
            if (heroName) heroName.textContent = 'Dr. Sharma';
            loadFacultyOverview();
        } else if (currentRole === 'admin') {
            if (nameEl) nameEl.textContent = 'Campus Administrator';
            if (subEl) subEl.textContent = 'SYSADMIN • Academic Affairs';
            if (badgeEl) badgeEl.textContent = 'Admin';
            if (heroName) heroName.textContent = 'Administrator';
            loadAdminOverview();
        }
    });
}

/* 4. OVERVIEW DATA HYDRATION */
async function loadOverviewData() {
    try {
        const res = await fetch(`/api/students/dashboard?student_id=${currentStudentId}`);
        if (!res.ok) return;
        const data = await res.json();

        if (data.student) {
            document.getElementById('overviewAttendance').textContent = `${data.student.attendance_rate}%`;
            document.getElementById('overviewCgpa').textContent = data.student.cgpa || '8.45';
        }
        if (data.metrics) {
            document.getElementById('overviewAssignments').textContent = data.metrics.pending_assignments_count || '3';
        }
    } catch (err) {
        console.warn('Overview data fetch error:', err);
    }
}

async function loadFacultyOverview() {
    try {
        const res = await fetch('/api/faculty/dashboard?employee_id=FAC101');
        if (!res.ok) return;
        const data = await res.json();
        if (data.overview) {
            document.getElementById('overviewAttendance').textContent = '91.2%';
            document.getElementById('overviewCgpa').textContent = `${data.overview.total_sessions_conducted} Sessions`;
            document.getElementById('overviewAssignments').textContent = data.overview.active_assignments;
        }
    } catch (err) {
        console.warn(err);
    }
}

async function loadAdminOverview() {
    try {
        const res = await fetch('/api/admin/overview');
        if (!res.ok) return;
        const data = await res.json();
        if (data.metrics) {
            document.getElementById('overviewAttendance').textContent = `${data.metrics.average_attendance_rate}%`;
            document.getElementById('overviewCgpa').textContent = `${data.metrics.total_students} Students`;
            document.getElementById('overviewAssignments').textContent = `${data.metrics.total_faculty} Faculty`;
        }
    } catch (err) {
        console.warn(err);
    }
}

/* 5. AI CHATBOT (STT/TTS + RAG + Intent Engine) */
function initChatbot() {
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSendBtn');
    const voiceBtn = document.getElementById('voiceDictationBtn');
    const clearBtn = document.getElementById('clearChatBtn');

    if (sendBtn && input) {
        sendBtn.addEventListener('click', () => sendChatMessage());
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') sendChatMessage();
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            const box = document.getElementById('chatMessages');
            box.innerHTML = `
                <div class="chat-msg bot">
                    <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
                    <div class="msg-bubble">
                        <p>Conversation cleared. How can I assist you today?</p>
                    </div>
                </div>
            `;
        });
    }

    // Voice Dictation (Speech Recognition)
    if (voiceBtn && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRec();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => voiceBtn.classList.add('recording');
        recognition.onend = () => voiceBtn.classList.remove('recording');
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            input.value = transcript;
            sendChatMessage();
        };

        voiceBtn.addEventListener('click', () => {
            try {
                recognition.start();
            } catch (e) {
                recognition.stop();
            }
        });
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    appendMessage('user', text);

    // Typing indicator
    const typingId = appendTypingIndicator();

    try {
        const res = await fetch('/api/chatbot/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, student_id: currentStudentId })
        });
        const data = await res.json();
        removeTypingIndicator(typingId);

        let botReply = data.response || "I have received your request.";
        let metadataHtml = '';
        if (data.source) {
            metadataHtml = `<div class="msg-meta-source"><i class="fa-solid fa-book-bookmark"></i> Source: ${data.source}</div>`;
        }

        appendMessage('bot', botReply + metadataHtml);

        // Optional speech synthesis playback
        if (data.audio_response && 'speechSynthesis' in window) {
            const utter = new SpeechSynthesisUtterance(botReply.replace(/<[^>]*>?/gm, ''));
            window.speechSynthesis.speak(utter);
        }
    } catch (err) {
        removeTypingIndicator(typingId);
        // Offline client-side campus conversational engine
        const lower = text.toLowerCase();
        let reply = "";
        let src = "Cortex Client-Side Neural Fallback";

        if (lower.includes('attendance')) {
            reply = "Your verified cumulative attendance is <strong>86.4%</strong> across 42 sessions. You are safely compliant (>75% mandatory threshold).";
        } else if (lower.includes('exam') || lower.includes('midterm') || lower.includes('schedule')) {
            reply = "Your upcoming examinations start December 8, 2026. Next exam: <strong>MCA-301: Machine Learning</strong> at 10:00 AM in Turing Hall 401.";
        } else if (lower.includes('assignment') || lower.includes('pending') || lower.includes('homework')) {
            reply = "You have 2 pending assignments: <strong>Machine Learning Neural Network Lab Notebook</strong> (due Friday, 50 pts) and <strong>SQL Query Optimization</strong> (due Dec 12).";
        } else if (lower.includes('grade') || lower.includes('predict') || lower.includes('gpa')) {
            reply = "Based on the trained UCI regression model, your predicted semester performance is <strong>14.8 / 20 (Grade A)</strong> with a 94.2% completion confidence.";
        } else if (lower.includes('career') || lower.includes('resume') || lower.includes('skill')) {
            reply = "Your current profile has an <strong>82% match</strong> for AI & Data Engineer roles. Adding Docker and Apache Kafka competencies will raise your alignment to 94%.";
        } else {
            reply = "Hello! I am your CORTEX 2.0 Campus Assistant. You can check your attendance, predict final examination grades, view class timetables, and submit assignments directly from this portal.";
        }
        appendMessage('bot', reply + `<div class="msg-meta-source"><i class="fa-solid fa-cloud-bolt"></i> Source: ${src}</div>`);
    }
}

function sendQuickMessage(text) {
    switchTab('assistant');
    const input = document.getElementById('chatInput');
    input.value = text;
    sendChatMessage();
}

function appendMessage(sender, htmlContent) {
    const box = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${sender}`;

    const icon = sender === 'bot' ? '<i class="fa-solid fa-robot"></i>' : '<i class="fa-solid fa-user"></i>';
    msgDiv.innerHTML = `
        <div class="msg-avatar">${icon}</div>
        <div class="msg-bubble">${htmlContent}</div>
    `;
    box.appendChild(msgDiv);
    box.scrollTop = box.scrollHeight;
}

function appendTypingIndicator() {
    const box = document.getElementById('chatMessages');
    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'chat-msg bot';
    div.innerHTML = `
        <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="msg-bubble"><i class="fa-solid fa-circle-notch fa-spin"></i> Analyzing...</div>
    `;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

/* 6. SUCCESS ADVISOR */
async function loadAdvisorData() {
    try {
        const res = await fetch(`/api/success/dashboard?student_id=${currentStudentId}`);
        if (!res.ok) return;
        const data = await res.json();

        // Populate study plan checklist
        const checklist = document.getElementById('studyPlanChecklist');
        if (checklist && data.study_plan) {
            checklist.innerHTML = '';
            data.study_plan.forEach(task => {
                const item = document.createElement('div');
                item.className = `checklist-item ${task.status === 'Completed' ? 'completed' : ''}`;
                item.innerHTML = `
                    <label class="custom-checkbox">
                        <input type="checkbox" ${task.status === 'Completed' ? 'checked' : ''} onchange="toggleTask(${task.id}, this)">
                        <span class="checkmark"></span>
                    </label>
                    <div class="task-info">
                        <span class="task-title">${task.title}</span>
                        <span class="task-meta">${task.subject_code} • Est. ${task.estimated_minutes} mins</span>
                    </div>
                `;
                checklist.appendChild(item);
            });
        }

        // Populate prescriptive recommendations
        const recList = document.getElementById('recommendationList');
        if (recList && data.recommendations) {
            recList.innerHTML = '';
            data.recommendations.forEach(rec => {
                const card = document.createElement('div');
                card.className = 'rec-card';
                card.innerHTML = `
                    <div class="rec-header">
                        <span class="rec-type ${rec.type.toLowerCase()}">${rec.type}</span>
                        <span class="rec-priority">${rec.priority} Priority</span>
                    </div>
                    <div class="rec-body">
                        <h5>${rec.title}</h5>
                        <p>${rec.description}</p>
                    </div>
                `;
                recList.appendChild(card);
            });
        }
    } catch (err) {
        console.warn('Advisor data fetch error:', err);
        // Hydrate from OFFLINE_DATA fallback
        const checklist = document.getElementById('studyPlanChecklist');
        if (checklist) {
            checklist.innerHTML = '';
            OFFLINE_DATA.study_plan.forEach(task => {
                const item = document.createElement('div');
                item.className = `checklist-item ${task.status === 'Completed' ? 'completed' : ''}`;
                item.innerHTML = `
                    <label class="custom-checkbox">
                        <input type="checkbox" ${task.status === 'Completed' ? 'checked' : ''} onchange="toggleTask(${task.id}, this)">
                        <span class="checkmark"></span>
                    </label>
                    <div class="task-info">
                        <span class="task-title">${task.title}</span>
                        <span class="task-meta">${task.subject_code} • Est. ${task.estimated_minutes} mins</span>
                    </div>
                `;
                checklist.appendChild(item);
            });
        }
        const recList = document.getElementById('recommendationList');
        if (recList) {
            recList.innerHTML = '';
            OFFLINE_DATA.recommendations.forEach(rec => {
                const card = document.createElement('div');
                card.className = 'rec-card';
                card.innerHTML = `
                    <div class="rec-header">
                        <span class="rec-type ${rec.type.toLowerCase()}">${rec.type}</span>
                        <span class="rec-priority">${rec.priority} Priority</span>
                    </div>
                    <div class="rec-body">
                        <h5>${rec.title}</h5>
                        <p>${rec.description}</p>
                    </div>
                `;
                recList.appendChild(card);
            });
        }
    }
}

async function toggleTask(taskId, checkbox) {
    const status = checkbox.checked ? 'Completed' : 'Pending';
    try {
        await fetch(`/api/success/tasks/${taskId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });
        const parent = checkbox.closest('.checklist-item');
        if (parent) {
            if (checkbox.checked) parent.classList.add('completed');
            else parent.classList.remove('completed');
        }
    } catch (err) {
        console.error(err);
    }
}

function refreshStudyPlan() {
    loadAdvisorData();
}

/* 7. BIOMETRIC ATTENDANCE */
async function toggleCamera() {
    const video = document.getElementById('cameraVideo');
    const laser = document.getElementById('scannerLaser');
    const startBtn = document.getElementById('startCameraBtn');
    const captureBtn = document.getElementById('captureFaceBtn');

    if (mediaStream) {
        // Stop camera
        mediaStream.getTracks().forEach(t => t.stop());
        mediaStream = null;
        video.srcObject = null;
        laser.classList.remove('active');
        startBtn.innerHTML = '<i class="fa-solid fa-video"></i> Start Camera';
        captureBtn.disabled = true;
    } else {
        // Start camera
        try {
            mediaStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
            video.srcObject = mediaStream;
            laser.classList.add('active');
            startBtn.innerHTML = '<i class="fa-solid fa-video-slash"></i> Stop Camera';
            captureBtn.disabled = false;
        } catch (err) {
            alert('Unable to access camera: ' + err.message);
        }
    }
}

async function verifyFace() {
    const feedback = document.getElementById('biometricFeedback');
    try {
        const res = await fetch('/api/attendance/verify-face', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: currentStudentId, image_data: 'webrtc_snapshot' })
        });
        const data = await res.json();
        if (data.success) {
            alert(`✅ FaceLock AI Verified! Attendance recorded for ${data.student_name}.`);
            loadAttendanceData();
            loadOverviewData();
        } else {
            alert('❌ Face verification failed: ' + (data.error || 'Face not recognized'));
        }
    } catch (err) {
        alert('Verification error: ' + err.message);
    }
}

async function verifyFingerprint() {
    const feedback = document.getElementById('biometricFeedback');
    feedback.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Triggering hardware sensor...';

    try {
        // Check WebAuthn sensor availability
        if (window.PublicKeyCredential) {
            const available = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
            console.log('WebAuthn sensor status:', available);
        }

        const res = await fetch('/api/attendance/verify-fingerprint', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: currentStudentId, credential_id: 'webauthn_bio_token' })
        });
        const data = await res.json();
        if (data.success) {
            feedback.innerHTML = `<span class="text-success"><i class="fa-solid fa-check-circle"></i> Biometric Verified! Attendance logged for ${data.student_name}.</span>`;
            loadAttendanceData();
            loadOverviewData();
        } else {
            feedback.innerHTML = `<span class="text-danger"><i class="fa-solid fa-triangle-exclamation"></i> Fingerprint mismatch.</span>`;
        }
    } catch (err) {
        feedback.innerHTML = `<span class="text-danger">${err.message}</span>`;
    }
}

async function loadAttendanceData() {
    try {
        const res = await fetch(`/api/attendance/status/${currentStudentId}`);
        if (!res.ok) return;
        const data = await res.json();

        const tbody = document.getElementById('attendanceLogsTbody');
        if (tbody && data.recent_logs) {
            tbody.innerHTML = '';
            data.recent_logs.forEach(log => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${log.date || 'Today'}</td>
                    <td>${log.subject || 'MCA Core'}</td>
                    <td><i class="fa-solid fa-shield"></i> ${log.method || 'Biometric'}</td>
                    <td><span class="status-badge ${log.status.toLowerCase()}">${log.status}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (err) {
        console.warn('Attendance history fetch error:', err);
        const tbody = document.getElementById('attendanceLogsTbody');
        if (tbody) {
            tbody.innerHTML = '';
            OFFLINE_DATA.attendance_logs.forEach(log => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${log.date}</td>
                    <td>${log.subject}</td>
                    <td><i class="fa-solid fa-shield"></i> ${log.method}</td>
                    <td><span class="status-badge ${log.status.toLowerCase()}">${log.status}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }
    }
}

/* ML Attendance Habit Predictor */
async function updatePredictor() {
    const studyHours = parseFloat(document.getElementById('sliderStudyHours').value);
    const sleepHours = parseFloat(document.getElementById('sliderSleepHours').value);
    const travelTime = parseFloat(document.getElementById('sliderTravelTime').value);

    document.getElementById('studyHoursVal').textContent = studyHours.toFixed(1);
    document.getElementById('sleepHoursVal').textContent = sleepHours.toFixed(1);
    document.getElementById('travelTimeVal').textContent = travelTime;

    try {
        const res = await fetch('/api/attendance/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                study_hours: studyHours,
                sleep_hours: sleepHours,
                travel_time_minutes: travelTime,
                course: 'b.tech',
                year: '3rd year'
            })
        });
        const data = await res.json();

        const percentEl = document.getElementById('predPercent');
        const badgeEl = document.getElementById('predRiskBadge');
        const recEl = document.getElementById('predRecommendation');

        percentEl.textContent = `${data.attendance_probability}%`;
        percentEl.style.color = data.risk_color;
        badgeEl.textContent = data.risk_level;
        badgeEl.style.borderColor = data.risk_color;
        recEl.textContent = data.recommendation;
    } catch (err) {
        console.warn('ML predictor error:', err);
    }
}

/* 8. ACADEMIC ANALYTICS */
async function predictUciGrade() {
    const g1 = parseFloat(document.getElementById('uciG1').value);
    const g2 = parseFloat(document.getElementById('uciG2').value);
    const studytime = parseInt(document.getElementById('uciStudyTime').value);
    const absences = parseInt(document.getElementById('uciAbsences').value);

    try {
        const res = await fetch('/api/academic/predict-grade', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ G1: g1, G2: g2, studytime, absences })
        });
        const data = await res.json();

        document.getElementById('uciPredictedScore').textContent = `${data.predicted_score} / 20 (${data.letter_grade})`;
        const passText = data.is_pass ? `Pass Probability: 94.2% (${data.performance_band})` : 'At Risk (< 10/20)';
        document.getElementById('uciResultBox').querySelector('.res-sub').textContent = passText;
    } catch (err) {
        alert('Grade prediction error: ' + err.message);
    }
}

async function predictOuladOutcome() {
    const clicks = parseInt(document.getElementById('ouladClicks').value);
    const score = parseFloat(document.getElementById('ouladScore').value);
    const assessments = parseInt(document.getElementById('ouladAssessments').value);

    try {
        const res = await fetch('/api/academic/predict-outcome', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ total_vle_clicks: clicks, avg_score: score, assessments_count: assessments })
        });
        const data = await res.json();

        document.getElementById('ouladOutcome').textContent = data.predicted_outcome;
        document.getElementById('ouladResultBox').querySelector('.res-sub').textContent = `Confidence: ${(data.confidence * 100).toFixed(1)}%`;
    } catch (err) {
        alert('Outcome prediction error: ' + err.message);
    }
}

async function loadAcademicData() {
    try {
        const res = await fetch(`/api/academic/results?student_id=${currentStudentId}`);
        if (!res.ok) return;
        const data = await res.json();

        const tbody = document.getElementById('academicResultsTbody');
        if (tbody && data.results) {
            tbody.innerHTML = '';
            data.results.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${item.subject_code}</strong></td>
                    <td>${item.subject_name}</td>
                    <td>${item.exam_type}</td>
                    <td>${item.score} / ${item.max_score} (${item.percentage}%)</td>
                    <td><span class="status-badge present">${item.grade}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (err) {
        console.warn('Academic data fetch error:', err);
        const tbody = document.getElementById('academicResultsTbody');
        if (tbody) {
            tbody.innerHTML = '';
            OFFLINE_DATA.results.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${item.subject_code}</strong></td>
                    <td>${item.subject_name}</td>
                    <td>${item.exam_type}</td>
                    <td>${item.score} / ${item.max_score} (${item.percentage}%)</td>
                    <td><span class="status-badge present">${item.grade}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }
    }
}

/* 9. CAREER & RESUME */
async function analyzeResumeSkills() {
    const text = document.getElementById('resumeInput').value.trim();
    if (!text) {
        alert('Please paste resume text or a skill summary.');
        return;
    }

    try {
        const res = await fetch('/api/career/analyze-resume', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_text: text })
        });
        const data = await res.json();

        // Populate skills cloud
        const cloud = document.getElementById('skillsCloud');
        if (cloud && data.extracted_skills) {
            cloud.innerHTML = '';
            data.extracted_skills.forEach(skill => {
                const tag = document.createElement('span');
                tag.className = 'skill-tag';
                tag.textContent = skill;
                cloud.appendChild(tag);
            });
        }

        // Target match score
        if (data.target_match) {
            document.getElementById('careerMatchPercent').textContent = `${data.target_match.match_percentage}%`;
        }
    } catch (err) {
        alert('Resume analysis error: ' + err.message);
    }
}

/* 10. TIMETABLE & EXAMINATIONS */
async function loadTimetableData() {
    try {
        const res = await fetch('/api/timetable');
        if (res.ok) {
            const data = await res.json();
            const tbody = document.getElementById('timetableTbody');
            if (tbody && data.slots) {
                tbody.innerHTML = '';
                data.slots.forEach(slot => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><strong>${slot.day}</strong></td>
                        <td>${slot.time_slot}</td>
                        <td>${slot.subject_code} - ${slot.subject_name}</td>
                        <td>${slot.room}</td>
                        <td>${slot.faculty_name}</td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }

        // Load examinations
        const examRes = await fetch('/api/timetable/examinations');
        if (examRes.ok) {
            const examData = await examRes.json();
            const examsTbody = document.getElementById('examsTbody');
            if (examsTbody && examData.examinations) {
                examsTbody.innerHTML = '';
                examData.examinations.forEach(exam => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><strong>${exam.exam_name}</strong></td>
                        <td>${exam.subject_code} - ${exam.subject_name}</td>
                        <td>${exam.exam_date}</td>
                        <td>${exam.time_slot}</td>
                        <td>${exam.room}</td>
                    `;
                    examsTbody.appendChild(tr);
                });
            }
        }
    } catch (err) {
        console.warn('Timetable fetch error:', err);
        const tbody = document.getElementById('timetableTbody');
        if (tbody) {
            tbody.innerHTML = '';
            OFFLINE_DATA.timetable.forEach(slot => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${slot.day}</strong></td>
                    <td>${slot.time_slot}</td>
                    <td>${slot.subject_code} - ${slot.subject_name}</td>
                    <td>${slot.room}</td>
                    <td>${slot.faculty_name}</td>
                `;
                tbody.appendChild(tr);
            });
        }
        const examsTbody = document.getElementById('examsTbody');
        if (examsTbody) {
            examsTbody.innerHTML = '';
            OFFLINE_DATA.examinations.forEach(exam => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${exam.exam_name}</strong></td>
                    <td>${exam.subject_code} - ${exam.subject_name}</td>
                    <td>${exam.exam_date}</td>
                    <td>${exam.time_slot}</td>
                    <td>${exam.room}</td>
                `;
                examsTbody.appendChild(tr);
            });
        }
    }
}

/* 11. ASSIGNMENTS */
async function loadAssignmentsData() {
    try {
        const res = await fetch(`/api/assignments?student_id=${currentStudentId}`);
        if (!res.ok) return;
        const data = await res.json();

        const tbody = document.getElementById('assignmentsTbody');
        if (tbody && data.assignments) {
            tbody.innerHTML = '';
            data.assignments.forEach(a => {
                const tr = document.createElement('tr');
                const isSubmitted = a.status === 'Submitted';
                tr.innerHTML = `
                    <td><strong>${a.title}</strong></td>
                    <td>${a.subject_code} - ${a.subject_name}</td>
                    <td>${new Date(a.due_date).toLocaleDateString()}</td>
                    <td>${a.max_marks} pts</td>
                    <td><span class="status-badge ${isSubmitted ? 'present' : 'pending'}">${a.status}</span></td>
                    <td>
                        <button class="small-btn ${isSubmitted ? 'glass' : 'primary'}" onclick="openAssignmentModal(${a.id}, '${a.title.replace(/'/g, "\\'")}')">
                            ${isSubmitted ? 'Re-submit' : 'Submit'}
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (err) {
        console.warn('Assignments fetch error:', err);
        const tbody = document.getElementById('assignmentsTbody');
        if (tbody) {
            tbody.innerHTML = '';
            OFFLINE_DATA.assignments.forEach(a => {
                const tr = document.createElement('tr');
                const isSubmitted = a.status === 'Submitted';
                tr.innerHTML = `
                    <td><strong>${a.title}</strong></td>
                    <td>${a.subject_code} - ${a.subject_name}</td>
                    <td>${a.due_date}</td>
                    <td>${a.max_marks} pts</td>
                    <td><span class="status-badge ${isSubmitted ? 'present' : 'pending'}">${a.status}</span></td>
                    <td>
                        <button class="small-btn ${isSubmitted ? 'glass' : 'primary'}" onclick="openAssignmentModal(${a.id}, '${a.title.replace(/'/g, "\'")}')">
                            ${isSubmitted ? 'Re-submit' : 'Submit'}
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    }
}

function openAssignmentModal(id, title) {
    document.getElementById('modalAssignmentId').value = id;
    document.getElementById('modalAssignmentTitle').textContent = `Submit: ${title}`;
    document.getElementById('assignmentModal').classList.add('active');
}

function closeAssignmentModal() {
    document.getElementById('assignmentModal').classList.remove('active');
}

async function submitAssignmentAction() {
    const id = document.getElementById('modalAssignmentId').value;
    const content = document.getElementById('submissionContent').value.trim();
    if (!content) {
        alert('Please provide your submission link or content.');
        return;
    }

    try {
        const res = await fetch('/api/assignments/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                assignment_id: parseInt(id),
                student_id: currentStudentId,
                content: content
            })
        });
        const data = await res.json();
        if (data.submission) {
            alert('🎉 Assignment submitted successfully!');
            closeAssignmentModal();
            loadAssignmentsData();
            loadOverviewData();
        }
    } catch (err) {
        alert('Submission failed: ' + err.message);
    }
}

/* 12. NOTICES */
async function loadNoticesData() {
    try {
        const res = await fetch('/api/notices');
        if (!res.ok) return;
        const data = await res.json();

        const grid = document.getElementById('noticeCardsGrid');
        if (grid && data.notices) {
            grid.innerHTML = '';
            data.notices.forEach(n => {
                const card = document.createElement('div');
                card.className = 'content-card';
                card.innerHTML = `
                    <div class="card-header">
                        <span class="badge-tag">${n.category}</span>
                        <small class="text-muted">${n.published_at}</small>
                    </div>
                    <div class="card-body">
                        <h4>${n.title}</h4>
                        <p class="mt-2 text-secondary" style="font-size: 13px; line-height: 1.5;">${n.content}</p>
                    </div>
                `;
                grid.appendChild(card);
            });
        }
    } catch (err) {
        console.warn('Notices fetch error:', err);
        const grid = document.getElementById('noticeCardsGrid');
        if (grid) {
            grid.innerHTML = '';
            OFFLINE_DATA.notices.forEach(n => {
                const card = document.createElement('div');
                card.className = 'content-card';
                card.innerHTML = `
                    <div class="card-header">
                        <span class="badge-tag">${n.category}</span>
                        <small class="text-muted">${n.published_at}</small>
                    </div>
                    <div class="card-body">
                        <h4>${n.title}</h4>
                        <p class="mt-2 text-secondary" style="font-size: 13px; line-height: 1.5;">${n.content}</p>
                    </div>
                `;
                grid.appendChild(card);
            });
        }
    }
}

async function summarizeNotices() {
    try {
        const res = await fetch('/api/notices/summarize');
        const data = await res.json();
        alert(`📌 AI Campus Bulletins Summary:\n\n${data.summary}`);
    } catch (err) {
        alert('Summary error: ' + err.message);
    }
}

/* 13. GRIEVANCES */
async function submitGrievance() {
    const category = document.getElementById('grievanceCategory').value;
    const subject = document.getElementById('grievanceSubject').value.trim();
    const desc = document.getElementById('grievanceDescription').value.trim();
    const alertBox = document.getElementById('grievanceAlert');

    if (!subject || !desc) {
        alertBox.innerHTML = '<span class="text-danger">Please fill in both subject and description.</span>';
        return;
    }

    try {
        const res = await fetch('/api/grievances', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: currentStudentId,
                category,
                subject,
                description: desc
            })
        });
        const data = await res.json();
        alertBox.innerHTML = `<span class="text-success">✅ Grievance filed successfully (Ticket #${data.grievance.ticket_number}).</span>`;
        document.getElementById('grievanceSubject').value = '';
        document.getElementById('grievanceDescription').value = '';
        loadGrievancesData();
    } catch (err) {
        alertBox.innerHTML = `<span class="text-danger">Submission error: ${err.message}</span>`;
    }
}

async function loadGrievancesData() {
    try {
        const res = await fetch(`/api/grievances?student_id=${currentStudentId}`);
        if (!res.ok) return;
        const data = await res.json();

        const tbody = document.getElementById('grievancesTbody');
        if (tbody && data.grievances) {
            tbody.innerHTML = '';
            data.grievances.forEach(g => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${g.ticket_number}</strong></td>
                    <td>${g.category}</td>
                    <td>${g.subject}</td>
                    <td><span class="status-badge ${g.status === 'Resolved' ? 'present' : 'pending'}">${g.status}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (err) {
        console.warn('Grievances fetch error:', err);
        const tbody = document.getElementById('grievancesTbody');
        if (tbody) {
            tbody.innerHTML = '';
            OFFLINE_DATA.grievances.forEach(g => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${g.ticket_number}</strong></td>
                    <td>${g.category}</td>
                    <td>${g.subject}</td>
                    <td><span class="status-badge ${g.status === 'Resolved' ? 'present' : 'pending'}">${g.status}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }
    }
}

/* 14. NOTIFICATIONS DRAWER */
function initNotifications() {
    const btn = document.getElementById('notificationBtn');
    const panel = document.getElementById('notificationsPanel');
    const markReadBtn = document.getElementById('markAllReadBtn');

    if (btn && panel) {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            panel.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!panel.contains(e.target) && e.target !== btn) {
                panel.classList.remove('active');
            }
        });
    }

    if (markReadBtn) {
        markReadBtn.addEventListener('click', async () => {
            try {
                await fetch('/api/notifications/mark-all-read', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ student_id: currentStudentId })
                });
                document.querySelectorAll('.notif-item').forEach(el => el.classList.remove('unread'));
                const badge = document.getElementById('notifBadge');
                if (badge) badge.style.display = 'none';
            } catch (e) {
                console.warn(e);
            }
        });
    }
}
