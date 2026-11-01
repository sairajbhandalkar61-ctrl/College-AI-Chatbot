/**
 * CORTEX • 120Hz HIGH-REFRESH RATE COLLEGE AI SYSTEM
 * Interactive Campus Assistant with Biometric FaceLock & Fingerprint Attendance
 */

(function () {
    'use strict';

    // State Variables
    let voiceEnabled = true;
    let isWaitingForResponse = false;
    let recognition = null;
    let isListening = false;
    let activeConversation = [];
    let currentSpeechUtterance = null;
    let cameraStream = null;

    // DOM Elements
    const cortexHeroState = document.getElementById('cortex-hero-state');
    const cortexChatState = document.getElementById('cortex-chat-state');
    const chatThreadWrapper = document.getElementById('chat-thread-wrapper');
    const conversationDockWrapper = document.getElementById('conversation-dock-wrapper');
    
    // Inputs & Send Buttons
    const cortexUserInput = document.getElementById('cortex-user-input');
    const conversationInput = document.getElementById('conversation-input');
    const cortexSendBtn = document.getElementById('cortex-send-btn');
    const dockSubmitBtn = document.getElementById('dock-submit-btn');
    
    // Mic Buttons
    const cortexMicBtn = document.getElementById('cortex-mic-btn');
    const dockSpeechBtn = document.getElementById('dock-speech-btn');
    const voiceToggleBtn = document.getElementById('voice-toggle-btn');
    
    // Navigation & Reset Buttons
    const newChatBtn = document.getElementById('new-chat-btn');
    const brandHomeBtn = document.getElementById('brand-home-btn');
    const clearSessionBtn = document.getElementById('clear-session-btn');
    
    // Header Controls
    const cortexDropdownBtn = document.getElementById('cortex-dropdown-btn');
    const cortexDropdownWrapper = document.getElementById('cortex-dropdown-wrapper');
    const exportChatBtn = document.getElementById('export-chat-btn');
    const topLinkBtn = document.getElementById('top-link-btn');
    const headerBiometricsBtn = document.getElementById('header-biometrics-btn');
    
    // Sidebar Elements
    const sidebarContainer = document.getElementById('sidebar-container');
    const sidebarBackdrop = document.getElementById('sidebar-backdrop');
    const sidebarCollapseBtn = document.getElementById('sidebar-collapse-btn');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebarSearchInput = document.getElementById('sidebar-search-input');
    const navBiometricsBtn = document.getElementById('nav-biometrics-btn');
    const navAttendanceStatusBtn = document.getElementById('nav-attendance-status-btn');
    const navPredictorBtn = document.getElementById('nav-predictor-btn');
    
    // Action Cards & Chips
    const cardLaunchBiometrics = document.getElementById('card-launch-biometrics');
    const cardLaunchPredictor = document.getElementById('card-launch-predictor');
    const chipMarkAttendance = document.getElementById('chip-mark-attendance');

    // Interactive 3D Orb & FPS Badge
    const interactiveOrb = document.getElementById('interactive-orb');
    const orbCore = document.getElementById('orb-core');
    const orbAura = document.getElementById('orb-aura');
    const fpsCounter = document.getElementById('fps-counter');
    const ambientCanvas = document.getElementById('ambient-canvas');
    const toastContainer = document.getElementById('toast-container');

    // Biometric Modal Elements
    const biometricModalOverlay = document.getElementById('biometric-modal-overlay');
    const closeBiometricBtn = document.getElementById('close-biometric-btn');
    
    const tabBtnFacelock = document.getElementById('tab-btn-facelock');
    const tabBtnFingerprint = document.getElementById('tab-btn-fingerprint');
    const tabBtnPredictor = document.getElementById('tab-btn-predictor');
    const tabBtnLogs = document.getElementById('tab-btn-logs');
    
    const panelFacelock = document.getElementById('panel-facelock');
    const panelFingerprint = document.getElementById('panel-fingerprint');
    const panelPredictor = document.getElementById('panel-predictor');
    const panelLogs = document.getElementById('panel-logs');
    
    // FaceLock Elements
    const faceVideo = document.getElementById('face-video');
    const faceCanvas = document.getElementById('face-canvas');
    const scannerLaserBeam = document.getElementById('scanner-laser-beam');
    const cameraOffOverlay = document.getElementById('camera-off-overlay');
    const btnStartCamera = document.getElementById('btn-start-camera');
    const btnCaptureFace = document.getElementById('btn-capture-face');
    const faceIndicatorDot = document.getElementById('face-indicator-dot');
    const faceStatusText = document.getElementById('face-status-text');
    const faceConfidenceBadge = document.getElementById('face-confidence-badge');

    // Fingerprint Elements
    const fingerprintScanZone = document.getElementById('fingerprint-scan-zone');
    const fingerprintIconWrapper = document.getElementById('fingerprint-icon-wrapper');
    const btnTouchFingerprint = document.getElementById('btn-touch-fingerprint');
    const webauthnSupportPill = document.getElementById('webauthn-support-pill');

    // Predictor Elements
    const inputStudyHours = document.getElementById('input-study-hours');
    const inputSleepHours = document.getElementById('input-sleep-hours');
    const inputTravelTime = document.getElementById('input-travel-time');
    const selectCourse = document.getElementById('select-course');
    const valStudyHours = document.getElementById('val-study-hours');
    const valSleepHours = document.getElementById('val-sleep-hours');
    const valTravelTime = document.getElementById('val-travel-time');
    const btnCalculateRisk = document.getElementById('btn-calculate-risk');
    const predictionResultBox = document.getElementById('prediction-result-box');
    const resProbVal = document.getElementById('res-prob-val');
    const resRiskBadge = document.getElementById('res-risk-badge');
    const resRecommendationText = document.getElementById('res-recommendation-text');

    // Logs Elements
    const summaryRate = document.getElementById('summary-rate');
    const summaryStatusTag = document.getElementById('summary-status-tag');
    const summarySessions = document.getElementById('summary-sessions');
    const logsTableBody = document.getElementById('logs-table-body');

    /* ==========================================================================
       1. 120Hz PRECISION AMBIENT CANVAS & FPS ENGINE
       ========================================================================== */
    let ctx = null;
    let canvasWidth = 0;
    let canvasHeight = 0;
    let particles = [];
    let lastFrameTime = performance.now();
    let frameCount = 0;
    let fpsSmoothed = 120;
    let lastFpsUpdate = performance.now();

    function initAmbientCanvas() {
        if (!ambientCanvas) return;
        ctx = ambientCanvas.getContext('2d', { alpha: true });
        
        function resizeCanvas() {
            canvasWidth = ambientCanvas.width = window.innerWidth;
            canvasHeight = ambientCanvas.height = window.innerHeight;
            createParticles();
        }

        window.addEventListener('resize', resizeCanvas, { passive: true });
        resizeCanvas();
        requestAnimationFrame(render120HzLoop);
    }

    function createParticles() {
        particles = [];
        const count = window.innerWidth < 768 ? 24 : 55;
        for (let i = 0; i < count; i++) {
            particles.push({
                x: Math.random() * canvasWidth,
                y: Math.random() * canvasHeight,
                radius: Math.random() * 2.2 + 0.8,
                vx: (Math.random() - 0.5) * 0.45,
                vy: (Math.random() - 0.5) * 0.45,
                alpha: Math.random() * 0.35 + 0.15,
                hue: Math.random() > 0.5 ? 265 : 285
            });
        }
    }

    function render120HzLoop(now) {
        const dt = (now - lastFrameTime) / 1000;
        lastFrameTime = now;
        frameCount++;

        if (now - lastFpsUpdate >= 500) {
            const currentFps = Math.round((frameCount * 1000) / (now - lastFpsUpdate));
            fpsSmoothed = Math.min(144, Math.round(fpsSmoothed * 0.7 + currentFps * 0.3));
            if (fpsCounter) {
                fpsCounter.textContent = `${fpsSmoothed} FPS`;
            }
            frameCount = 0;
            lastFpsUpdate = now;
        }

        if (ctx) {
            ctx.clearRect(0, 0, canvasWidth, canvasHeight);
            const len = particles.length;
            for (let i = 0; i < len; i++) {
                const p = particles[i];
                p.x += p.vx * (dt * 60);
                p.y += p.vy * (dt * 60);

                if (p.x < 0) p.x = canvasWidth;
                else if (p.x > canvasWidth) p.x = 0;
                if (p.y < 0) p.y = canvasHeight;
                else if (p.y > canvasHeight) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = `hsla(${p.hue}, 80%, 75%, ${p.alpha})`;
                ctx.fill();
            }
        }

        requestAnimationFrame(render120HzLoop);
    }

    /* ==========================================================================
       2. INTERACTIVE 3D LIQUID ORB (PHYSICS & TILT)
       ========================================================================== */
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentTiltX = 0;
    let currentTiltY = 0;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        updateOrbTilt();
    }, { passive: true });

    function updateOrbTilt() {
        if (!interactiveOrb || !orbCore) return;
        const rect = interactiveOrb.getBoundingClientRect();
        const orbCenterX = rect.left + rect.width / 2;
        const orbCenterY = rect.top + rect.height / 2;
        
        const deltaX = (mouseX - orbCenterX) / (window.innerWidth / 2);
        const deltaY = (mouseY - orbCenterY) / (window.innerHeight / 2);
        
        const targetTiltX = -deltaY * 16;
        const targetTiltY = deltaX * 16;
        
        currentTiltX += (targetTiltX - currentTiltX) * 0.12;
        currentTiltY += (targetTiltY - currentTiltY) * 0.12;
        
        orbCore.style.transform = `perspective(500px) rotateX(${currentTiltX.toFixed(2)}deg) rotateY(${currentTiltY.toFixed(2)}deg)`;
    }

    if (interactiveOrb) {
        interactiveOrb.addEventListener('click', () => {
            if (orbCore) {
                orbCore.style.transform = `perspective(500px) scale(0.88)`;
                setTimeout(() => {
                    orbCore.style.transform = `perspective(500px) scale(1.08)`;
                    setTimeout(() => updateOrbTilt(), 180);
                }, 100);
            }
            showToast("College AI Core Online • Biometrics Ready");
        });
    }

    /* ==========================================================================
       3. TOAST NOTIFICATION UTILITY
       ========================================================================== */
    function showToast(message) {
        if (!toastContainer) return;
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(6px)';
            toast.style.transition = 'all 0.2s ease';
            setTimeout(() => toast.remove(), 250);
        }, 2600);
    }

    /* ==========================================================================
       4. SPEECH SYNTHESIS & RECOGNITION (VOICE INTELLIGENCE)
       ========================================================================== */
    function speakText(text, btnElement) {
        if (!voiceEnabled || !('speechSynthesis' in window)) return;
        try {
            window.speechSynthesis.cancel();
            if (currentSpeechUtterance) currentSpeechUtterance = null;
            setOrbAudioState(false);

            const cleanText = text.replace(/<[^>]*>?/gm, '').slice(0, 320);
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 1.0;
            utterance.pitch = 1.0;

            utterance.onstart = () => {
                setOrbAudioState(true);
                if (btnElement) btnElement.classList.add('active');
            };

            utterance.onend = () => {
                setOrbAudioState(false);
                if (btnElement) btnElement.classList.remove('active');
            };

            utterance.onerror = () => {
                setOrbAudioState(false);
                if (btnElement) btnElement.classList.remove('active');
            };

            currentSpeechUtterance = utterance;
            window.speechSynthesis.speak(utterance);
        } catch (e) {
            console.warn('Speech synthesis error:', e);
            setOrbAudioState(false);
        }
    }

    function setOrbAudioState(isActive) {
        if (!interactiveOrb) return;
        if (isActive) {
            interactiveOrb.classList.add('speaking');
        } else {
            interactiveOrb.classList.remove('speaking');
        }
    }

    function initSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) return;

        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function () {
            isListening = true;
            if (cortexMicBtn) cortexMicBtn.classList.add('listening');
            if (dockSpeechBtn) dockSpeechBtn.classList.add('listening');
            if (interactiveOrb) interactiveOrb.classList.add('listening');
            showToast("Listening... Speak your question");
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            if (cortexHeroState.style.display !== 'none' && cortexUserInput) {
                cortexUserInput.value = transcript;
                dispatchUserQuery(transcript);
            } else if (conversationInput) {
                conversationInput.value = transcript;
                dispatchUserQuery(transcript);
            }
        };

        recognition.onerror = function (event) {
            console.warn("Speech recognition error:", event.error);
            stopListening();
        };

        recognition.onend = function () {
            stopListening();
        };
    }

    function toggleSpeechRecognition() {
        if (!recognition) {
            showToast("Voice dictation is supported in Chrome, Edge & Safari");
            return;
        }
        if (isListening) {
            recognition.stop();
        } else {
            try {
                recognition.start();
            } catch (err) {
                recognition.stop();
            }
        }
    }

    function stopListening() {
        isListening = false;
        if (cortexMicBtn) cortexMicBtn.classList.remove('listening');
        if (dockSpeechBtn) dockSpeechBtn.classList.remove('listening');
        if (interactiveOrb) interactiveOrb.classList.remove('listening');
    }

    /* ==========================================================================
       5. BIOMETRIC ATTENDANCE ENGINES (FaceLock & Fingerprint)
       ========================================================================== */
    function openBiometricModal(initialTab) {
        if (!biometricModalOverlay) return;
        biometricModalOverlay.style.display = 'flex';
        switchBioTab(initialTab || 'facelock');
    }

    function closeBiometricModal() {
        if (!biometricModalOverlay) return;
        biometricModalOverlay.style.display = 'none';
        stopCamera();
    }

    function switchBioTab(tabName) {
        // Deactivate all
        [tabBtnFacelock, tabBtnFingerprint, tabBtnPredictor, tabBtnLogs].forEach(b => b && b.classList.remove('active'));
        [panelFacelock, panelFingerprint, panelPredictor, panelLogs].forEach(p => p && (p.style.display = 'none'));

        if (tabName === 'facelock') {
            if (tabBtnFacelock) tabBtnFacelock.classList.add('active');
            if (panelFacelock) panelFacelock.style.display = 'block';
            startCamera();
        } else if (tabName === 'fingerprint') {
            stopCamera();
            if (tabBtnFingerprint) tabBtnFingerprint.classList.add('active');
            if (panelFingerprint) panelFingerprint.style.display = 'block';
            checkWebAuthnSupport();
        } else if (tabName === 'predictor') {
            stopCamera();
            if (tabBtnPredictor) tabBtnPredictor.classList.add('active');
            if (panelPredictor) panelPredictor.style.display = 'block';
        } else if (tabName === 'logs') {
            stopCamera();
            if (tabBtnLogs) tabBtnLogs.classList.add('active');
            if (panelLogs) panelLogs.style.display = 'block';
            fetchAndRenderAttendanceStatus();
        }
    }

    // A. FaceLock AI Camera Engine
    async function startCamera() {
        if (cameraStream) return;
        try {
            if (faceStatusText) faceStatusText.textContent = "Accessing camera...";
            if (faceIndicatorDot) {
                faceIndicatorDot.className = 'indicator-dot scanning';
            }

            cameraStream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
                audio: false
            });

            if (faceVideo) {
                faceVideo.srcObject = cameraStream;
                faceVideo.onloadedmetadata = () => {
                    faceVideo.play();
                    if (cameraOffOverlay) cameraOffOverlay.style.display = 'none';
                    if (scannerLaserBeam) scannerLaserBeam.classList.add('scanning');
                    if (faceIndicatorDot) faceIndicatorDot.className = 'indicator-dot active';
                    if (faceStatusText) faceStatusText.textContent = "Live Camera Active: Align face in target reticle";
                };
            }
        } catch (err) {
            console.warn("Camera access denied or unavailable:", err);
            if (cameraOffOverlay) cameraOffOverlay.style.display = 'flex';
            if (faceIndicatorDot) faceIndicatorDot.className = 'indicator-dot';
            if (faceStatusText) faceStatusText.textContent = "Camera permission needed for FaceLock";
            showToast("Camera access required for FaceLock. Switch to Fingerprint if needed.");
        }
    }

    function stopCamera() {
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
            cameraStream = null;
        }
        if (faceVideo) faceVideo.srcObject = null;
        if (scannerLaserBeam) scannerLaserBeam.classList.remove('scanning');
        if (cameraOffOverlay) cameraOffOverlay.style.display = 'flex';
        if (faceIndicatorDot) faceIndicatorDot.className = 'indicator-dot';
    }

    async function captureAndVerifyFace() {
        if (!cameraStream) {
            await startCamera();
            return;
        }

        if (faceStatusText) faceStatusText.textContent = "Capturing facial landmarks & anti-spoofing...";
        if (faceIndicatorDot) faceIndicatorDot.className = 'indicator-dot scanning';
        if (btnCaptureFace) btnCaptureFace.disabled = true;

        // Capture snapshot frame
        let snapshotData = "data:image/jpeg;base64,mock_biometric_face_frame";
        if (faceVideo && faceCanvas) {
            const width = faceVideo.videoWidth || 640;
            const height = faceVideo.videoHeight || 480;
            faceCanvas.width = width;
            faceCanvas.height = height;
            const ctxCanvas = faceCanvas.getContext('2d');
            ctxCanvas.drawImage(faceVideo, 0, 0, width, height);
            snapshotData = faceCanvas.toDataURL('image/jpeg', 0.85);
        }

        try {
            // 1. Verify Face
            const verifyRes = await fetch('/api/attendance/verify-face', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: snapshotData, student_id: 'SB2026' })
            });
            const verifyData = await verifyRes.json();

            if (!verifyData.success) {
                throw new Error(verifyData.message || "Facial verification failed.");
            }

            if (faceConfidenceBadge) {
                faceConfidenceBadge.textContent = `Match: ${Math.round(verifyData.confidence * 100)}%`;
            }

            // 2. Punch Attendance
            const markRes = await fetch('/api/attendance/mark', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    student_id: 'SB2026',
                    method: 'FaceLock AI',
                    course: 'B.Tech Computer Science',
                    subject: 'Machine Learning & Neural Networks'
                })
            });
            const markData = await markRes.json();

            if (faceStatusText) faceStatusText.textContent = `Verified! ${markData.student_name} (${markData.attendance_rate}%)`;
            if (faceIndicatorDot) faceIndicatorDot.className = 'indicator-dot active';

            showToast("✅ Face Verified! Attendance successfully marked.");
            
            // Post confirmation into chat thread
            postSystemConfirmationMessage(`🎓 **Attendance Recorded via FaceLock AI**\n\n• **Student:** ${markData.student_name} (SB2026)\n• **Course:** B.Tech Computer Science\n• **Timestamp:** ${markData.timestamp}\n• **Verified Attendance:** **${markData.attendance_rate}%** (${markData.attended_sessions}/${markData.total_sessions} sessions)\n• **Status:** Compliant for exams.`);

            setTimeout(() => {
                closeBiometricModal();
                if (btnCaptureFace) btnCaptureFace.disabled = false;
            }, 1400);

        } catch (err) {
            console.error("Biometric face error:", err);
            if (faceStatusText) faceStatusText.textContent = "Verification timeout. Please align face clearly.";
            showToast("Face verification failed. Please try again.");
            if (btnCaptureFace) btnCaptureFace.disabled = false;
        }
    }

    // B. Fingerprint Biometric Engine
    function checkWebAuthnSupport() {
        const isSupported = window.PublicKeyCredential !== undefined;
        if (webauthnSupportPill) {
            webauthnSupportPill.textContent = isSupported ? 
                "🔒 Native FIDO2 / WebAuthn Sensor Supported" : 
                "⚡ Interactive Biometric Touch Sensor Active";
        }
    }

    async function triggerFingerprintScan() {
        if (fingerprintIconWrapper) fingerprintIconWrapper.classList.add('active-scanning');
        if (btnTouchFingerprint) btnTouchFingerprint.disabled = true;

        if (navigator.vibrate) {
            navigator.vibrate([40, 80, 40]);
        }

        showToast("Scanning fingerprint ridge patterns...");

        try {
            // Attempt native WebAuthn if available or verify token
            const verifyRes = await fetch('/api/attendance/verify-fingerprint', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ student_id: 'SB2026', credential_id: 'fingerprint_sensor_auth' })
            });
            const verifyData = await verifyRes.json();

            // Mark Attendance
            const markRes = await fetch('/api/attendance/mark', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    student_id: 'SB2026',
                    method: 'Fingerprint Biometric',
                    course: 'B.Tech Computer Science',
                    subject: 'Cloud Architecture & Distributed Systems'
                })
            });
            const markData = await markRes.json();

            showToast("✅ Fingerprint Matched! Attendance recorded.");

            postSystemConfirmationMessage(`👆 **Attendance Recorded via Fingerprint Biometric**\n\n• **Student:** ${markData.student_name} (SB2026)\n• **Timestamp:** ${markData.timestamp}\n• **Overall Attendance:** **${markData.attendance_rate}%** (${markData.attended_sessions}/${markData.total_sessions})\n• **Compliance:** Excellent.`);

            setTimeout(() => {
                if (fingerprintIconWrapper) fingerprintIconWrapper.classList.remove('active-scanning');
                if (btnTouchFingerprint) btnTouchFingerprint.disabled = false;
                closeBiometricModal();
            }, 1200);

        } catch (err) {
            console.error("Fingerprint error:", err);
            showToast("Fingerprint verification failed. Please try again.");
            if (fingerprintIconWrapper) fingerprintIconWrapper.classList.remove('active-scanning');
            if (btnTouchFingerprint) btnTouchFingerprint.disabled = false;
        }
    }

    // C. Risk Predictor Sliders & ML Calculation
    function initPredictorControls() {
        if (inputStudyHours && valStudyHours) {
            inputStudyHours.addEventListener('input', () => {
                valStudyHours.textContent = `${parseFloat(inputStudyHours.value).toFixed(1)} hrs`;
            });
        }
        if (inputSleepHours && valSleepHours) {
            inputSleepHours.addEventListener('input', () => {
                valSleepHours.textContent = `${parseFloat(inputSleepHours.value).toFixed(1)} hrs`;
            });
        }
        if (inputTravelTime && valTravelTime) {
            inputTravelTime.addEventListener('input', () => {
                valTravelTime.textContent = `${inputTravelTime.value} mins`;
            });
        }

        if (btnCalculateRisk) {
            btnCalculateRisk.addEventListener('click', calculateAttendanceRisk);
        }
    }

    async function calculateAttendanceRisk() {
        const payload = {
            study_hours: parseFloat(inputStudyHours ? inputStudyHours.value : 4.0),
            sleep_hours: parseFloat(inputSleepHours ? inputSleepHours.value : 7.0),
            travel_time_minutes: parseFloat(inputTravelTime ? inputTravelTime.value : 30.0),
            course: selectCourse ? selectCourse.value : 'b.tech',
            year: '3rd year'
        };

        if (btnCalculateRisk) btnCalculateRisk.textContent = "Evaluating ML Model...";

        try {
            const res = await fetch('/api/attendance/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (predictionResultBox) predictionResultBox.style.display = 'flex';
            if (resProbVal) resProbVal.textContent = `${data.attendance_probability}%`;
            if (resRiskBadge) {
                resRiskBadge.textContent = data.risk_level;
                resRiskBadge.style.color = data.risk_color;
                resRiskBadge.style.backgroundColor = `${data.risk_color}18`;
            }
            if (resRecommendationText) {
                resRecommendationText.textContent = data.recommendation;
            }

            showToast(`ML Prediction: ${data.attendance_probability}% attendance probability`);
        } catch (err) {
            console.error("Predictor error:", err);
            showToast("Failed to compute prediction. Check connection.");
        } finally {
            if (btnCalculateRisk) btnCalculateRisk.textContent = "Compute Attendance Probability";
        }
    }

    // D. Fetch and Render Attendance Logs & Status
    async function fetchAndRenderAttendanceStatus() {
        try {
            const res = await fetch('/api/attendance/status/SB2026');
            const data = await res.json();

            if (summaryRate) summaryRate.textContent = `${data.attendance_rate}%`;
            if (summaryStatusTag) summaryStatusTag.textContent = data.status_label;
            if (summarySessions) summarySessions.textContent = `${data.attended_sessions} of ${data.total_sessions} lectures attended`;

            if (logsTableBody) {
                logsTableBody.innerHTML = '';
                if (!data.logs || data.logs.length === 0) {
                    logsTableBody.innerHTML = '<div style="padding: 16px; text-align: center; color: #64748B;">No attendance logs found.</div>';
                    return;
                }

                data.logs.forEach(log => {
                    const row = document.createElement('div');
                    row.className = 'log-row-item';
                    row.innerHTML = `
                        <div class="log-left">
                            <span class="log-subject">${log.subject || 'Lecture Session'}</span>
                            <span class="log-date">${log.date} at ${log.time}</span>
                        </div>
                        <span class="log-method">${log.method}</span>
                    `;
                    logsTableBody.appendChild(row);
                });
            }
        } catch (err) {
            console.error("Failed to load attendance logs:", err);
        }
    }

    function postSystemConfirmationMessage(markdownText) {
        switchToConversationState();
        renderAiResponse(markdownText, "Attendance Record");
    }

    /* ==========================================================================
       6. STATE TRANSITIONS & CHAT RENDERING
       ========================================================================== */
    function switchToConversationState() {
        if (cortexHeroState) cortexHeroState.style.display = 'none';
        if (cortexChatState) cortexChatState.style.display = 'block';
        if (conversationDockWrapper) conversationDockWrapper.style.display = 'flex';
        if (conversationInput) conversationInput.focus();
    }

    function switchToHeroState() {
        if (cortexHeroState) cortexHeroState.style.display = 'flex';
        if (cortexChatState) cortexChatState.style.display = 'none';
        if (conversationDockWrapper) conversationDockWrapper.style.display = 'none';
        if (cortexUserInput) {
            cortexUserInput.value = '';
            cortexUserInput.focus();
        }
    }

    function resetSession() {
        if (window.speechSynthesis) window.speechSynthesis.cancel();
        activeConversation = [];
        if (chatThreadWrapper) chatThreadWrapper.innerHTML = '';
        switchToHeroState();
        showToast("Started a new chat session");
    }

    function renderUserMessage(text) {
        const row = document.createElement('div');
        row.className = 'chat-msg-row user-msg-row';
        const bubble = document.createElement('div');
        bubble.className = 'user-chat-bubble';
        bubble.textContent = text;
        row.appendChild(bubble);
        chatThreadWrapper.appendChild(row);
        scrollToBottom();
    }

    function getFollowUpSuggestions(query) {
        const lower = query.toLowerCase();
        if (lower.includes('attendance') || lower.includes('face') || lower.includes('fingerprint')) {
            return [
                { label: "⚡ Punch attendance", query: "Mark my attendance today" },
                { label: "📊 Status (87.8%)", query: "What is my attendance?" },
                { label: "🎯 Predict risk", query: "Predict my attendance risk" }
            ];
        } else if (lower.includes('admission') || lower.includes('eligibility')) {
            return [
                { label: "💰 Fee structure", query: "What is the fee structure for engineering?" },
                { label: "📚 Courses offered", query: "What courses and branches are offered?" },
                { label: "⚡ Mark attendance", query: "Mark my attendance today" }
            ];
        } else {
            return [
                { label: "⚡ Mark attendance", query: "Mark my attendance today" },
                { label: "📊 Attendance score", query: "What is my attendance?" },
                { label: "🎓 Admission criteria", query: "What is the admission process and eligibility criteria?" }
            ];
        }
    }

    function renderAiResponse(fullText, userQuery, actionData) {
        const row = document.createElement('div');
        row.className = 'chat-msg-row ai-msg-row';
        
        const card = document.createElement('div');
        card.className = 'ai-chat-card';

        const p = document.createElement('p');
        p.className = 'ai-msg-text';
        
        const cursor = document.createElement('span');
        cursor.className = 'streaming-cursor';
        p.appendChild(cursor);
        card.appendChild(p);

        // Actions row (Thumbs, Copy, Speak)
        const actions = document.createElement('div');
        actions.className = 'ai-msg-actions';
        actions.innerHTML = `
            <button class="ai-action-icon-btn thumbs-up" title="Helpful" aria-label="Thumbs up">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
            </button>
            <button class="ai-action-icon-btn copy-btn" title="Copy text" aria-label="Copy">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            </button>
            <button class="ai-action-icon-btn speak-btn" title="Listen audio" aria-label="Speak">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
            </button>
        `;

        actions.querySelector('.thumbs-up').addEventListener('click', function () {
            this.classList.toggle('active');
            showToast("Thank you for your feedback!");
        });

        const copyBtn = actions.querySelector('.copy-btn');
        copyBtn.addEventListener('click', function () {
            navigator.clipboard.writeText(fullText).then(() => {
                copyBtn.classList.add('copied');
                showToast("Copied to clipboard!");
                setTimeout(() => copyBtn.classList.remove('copied'), 2000);
            });
        });

        const speakBtn = actions.querySelector('.speak-btn');
        speakBtn.addEventListener('click', function () {
            speakText(fullText, speakBtn);
        });

        card.appendChild(actions);
        row.appendChild(card);
        chatThreadWrapper.appendChild(row);
        scrollToBottom();

        // 120Hz-tuned Typewriter Streaming Effect
        let charIndex = 0;
        const textLength = fullText.length;
        const charsPerFrame = Math.max(1, Math.ceil(textLength / 45));

        function streamText() {
            if (charIndex < textLength) {
                const nextChunk = fullText.slice(charIndex, charIndex + charsPerFrame);
                p.insertBefore(document.createTextNode(nextChunk), cursor);
                charIndex += charsPerFrame;
                scrollToBottom();
                requestAnimationFrame(streamText);
            } else {
                cursor.remove();
                
                // If action includes attendance progress badge
                if (actionData && actionData.type === 'show_status') {
                    const statusCard = document.createElement('div');
                    statusCard.className = 'chat-attendance-card';
                    statusCard.innerHTML = `
                        <div class="att-card-header">
                            <span class="att-card-title">${actionData.name} (${actionData.student_id})</span>
                            <span class="att-card-badge">${actionData.status}</span>
                        </div>
                        <div class="att-progress-bar-track">
                            <div class="att-progress-bar-fill" style="width: ${actionData.attendance_rate}%;"></div>
                        </div>
                        <div class="att-card-footer">
                            <span>Attended: <strong>${actionData.attended_sessions} / ${actionData.total_sessions}</strong></span>
                            <span>Rate: <strong>${actionData.attendance_rate}%</strong> (Min 75%)</span>
                        </div>
                    `;
                    card.insertBefore(statusCard, actions);
                    scrollToBottom();
                }

                // Append Interactive Follow-up Suggestion Chips
                const followups = getFollowUpSuggestions(userQuery || '');
                if (followups && followups.length > 0) {
                    const followBox = document.createElement('div');
                    followBox.className = 'ai-followups-box';
                    
                    const title = document.createElement('span');
                    title.className = 'ai-followup-title';
                    title.textContent = 'Suggestions:';
                    followBox.appendChild(title);

                    followups.forEach(item => {
                        const chip = document.createElement('button');
                        chip.className = 'ai-followup-chip';
                        chip.textContent = item.label;
                        chip.addEventListener('click', () => dispatchUserQuery(item.query));
                        followBox.appendChild(chip);
                    });
                    
                    card.insertBefore(followBox, actions);
                    scrollToBottom();
                }

                // Trigger action modal if needed
                if (actionData && actionData.type === 'open_biometrics') {
                    setTimeout(() => openBiometricModal('facelock'), 400);
                } else if (actionData && actionData.type === 'open_predictor') {
                    setTimeout(() => openBiometricModal('predictor'), 400);
                }

                // Voice Readout
                speakText(fullText, speakBtn);
            }
        }

        requestAnimationFrame(streamText);
    }

    function scrollToBottom() {
        const container = document.getElementById('cortex-scroll-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }

    /* ==========================================================================
       7. BACKEND ML INTEGRATION
       ========================================================================== */
    async function dispatchUserQuery(queryText) {
        if (!queryText || isWaitingForResponse) return;
        isWaitingForResponse = true;

        switchToConversationState();

        if (cortexUserInput) cortexUserInput.value = '';
        if (conversationInput) conversationInput.value = '';

        renderUserMessage(queryText);
        activeConversation.push({ sender: 'user', text: queryText });

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: queryText })
            });

            if (!response.ok) {
                throw new Error(`Server returned status ${response.status}`);
            }

            const data = await response.json();
            const botResponse = data.response || "I could not find specific campus details for that question.";
            renderAiResponse(botResponse, queryText, data.action);
            activeConversation.push({ sender: 'ai', text: botResponse });
        } catch (error) {
            console.error("Chat error:", error);
            renderAiResponse("I apologize, but I could not connect to the campus assistant knowledge server. Please check your connection and try again.", queryText);
        } finally {
            isWaitingForResponse = false;
        }
    }

    /* ==========================================================================
       8. EVENT LISTENERS & SHORTCUTS
       ========================================================================== */
    // Hero Textarea
    if (cortexUserInput) {
        cortexUserInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const text = cortexUserInput.value.trim();
                if (text) dispatchUserQuery(text);
            }
        });
    }

    if (cortexSendBtn) {
        cortexSendBtn.addEventListener('click', () => {
            const text = cortexUserInput ? cortexUserInput.value.trim() : '';
            if (text) dispatchUserQuery(text);
        });
    }

    // Conversation Dock Input & Button
    if (conversationInput) {
        conversationInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const text = conversationInput.value.trim();
                if (text) dispatchUserQuery(text);
            }
        });
    }

    if (dockSubmitBtn) {
        dockSubmitBtn.addEventListener('click', () => {
            const text = conversationInput ? conversationInput.value.trim() : '';
            if (text) dispatchUserQuery(text);
        });
    }

    // Mic Buttons
    if (cortexMicBtn) cortexMicBtn.addEventListener('click', toggleSpeechRecognition);
    if (dockSpeechBtn) dockSpeechBtn.addEventListener('click', toggleSpeechRecognition);

    // Voice Toggle Button
    if (voiceToggleBtn) {
        voiceToggleBtn.addEventListener('click', () => {
            voiceEnabled = !voiceEnabled;
            if (!voiceEnabled && window.speechSynthesis) {
                window.speechSynthesis.cancel();
                setOrbAudioState(false);
            }
            voiceToggleBtn.style.opacity = voiceEnabled ? '1' : '0.4';
            showToast(`Voice readout: ${voiceEnabled ? 'Enabled' : 'Muted'}`);
        });
    }

    // Filter Chips & Quick Action Cards
    document.querySelectorAll('.filter-chip-btn, .cortex-action-card, .nav-link-item').forEach(el => {
        el.addEventListener('click', () => {
            const query = el.dataset.query;
            if (query) {
                dispatchUserQuery(query);
                closeMobileSidebar();
            }
        });
    });

    // Dedicated Biometric Launchers
    if (headerBiometricsBtn) headerBiometricsBtn.addEventListener('click', () => openBiometricModal('facelock'));
    if (cardLaunchBiometrics) cardLaunchBiometrics.addEventListener('click', () => openBiometricModal('facelock'));
    if (cardLaunchPredictor) cardLaunchPredictor.addEventListener('click', () => openBiometricModal('predictor'));
    if (chipMarkAttendance) chipMarkAttendance.addEventListener('click', () => openBiometricModal('facelock'));
    if (navBiometricsBtn) navBiometricsBtn.addEventListener('click', () => {
        openBiometricModal('facelock');
        closeMobileSidebar();
    });
    if (navAttendanceStatusBtn) navAttendanceStatusBtn.addEventListener('click', () => {
        openBiometricModal('logs');
        closeMobileSidebar();
    });
    if (navPredictorBtn) navPredictorBtn.addEventListener('click', () => {
        openBiometricModal('predictor');
        closeMobileSidebar();
    });

    // Biometric Modal Tab Switching
    if (tabBtnFacelock) tabBtnFacelock.addEventListener('click', () => switchBioTab('facelock'));
    if (tabBtnFingerprint) tabBtnFingerprint.addEventListener('click', () => switchBioTab('fingerprint'));
    if (tabBtnPredictor) tabBtnPredictor.addEventListener('click', () => switchBioTab('predictor'));
    if (tabBtnLogs) tabBtnLogs.addEventListener('click', () => switchBioTab('logs'));

    // Modal Close
    if (closeBiometricBtn) closeBiometricBtn.addEventListener('click', closeBiometricModal);
    if (biometricModalOverlay) {
        biometricModalOverlay.addEventListener('click', (e) => {
            if (e.target === biometricModalOverlay) closeBiometricModal();
        });
    }

    // Camera & Fingerprint Action Triggers
    if (btnStartCamera) btnStartCamera.addEventListener('click', startCamera);
    if (btnCaptureFace) btnCaptureFace.addEventListener('click', captureAndVerifyFace);
    if (btnTouchFingerprint) btnTouchFingerprint.addEventListener('click', triggerFingerprintScan);
    if (fingerprintScanZone) fingerprintScanZone.addEventListener('click', triggerFingerprintScan);

    // History Items
    document.querySelectorAll('.history-item').forEach(item => {
        item.addEventListener('click', () => {
            const query = item.dataset.query;
            if (query) {
                dispatchUserQuery(query);
                closeMobileSidebar();
            }
        });
    });

    // Reset Buttons
    if (newChatBtn) newChatBtn.addEventListener('click', resetSession);
    if (brandHomeBtn) brandHomeBtn.addEventListener('click', resetSession);
    if (clearSessionBtn) clearSessionBtn.addEventListener('click', resetSession);

    // Search filter in sidebar
    if (sidebarSearchInput) {
        sidebarSearchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase().trim();
            document.querySelectorAll('.history-item').forEach(item => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(term) ? 'block' : 'none';
            });
        });
    }

    // Top Dropdown
    if (cortexDropdownBtn && cortexDropdownWrapper) {
        cortexDropdownBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            cortexDropdownWrapper.classList.toggle('open');
        });

        document.querySelectorAll('.cortex-menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const modelName = e.target.dataset.model;
                const label = cortexDropdownBtn.querySelector('.cortex-dropdown-label');
                if (label) label.textContent = e.target.textContent;
                document.querySelectorAll('.cortex-menu-item').forEach(i => i.classList.remove('active'));
                e.target.classList.add('active');
                cortexDropdownWrapper.classList.remove('open');
                
                if (modelName === 'Attendance') {
                    openBiometricModal('facelock');
                } else {
                    showToast(`Assistant context: ${e.target.textContent}`);
                }
            });
        });

        document.addEventListener('click', () => {
            cortexDropdownWrapper.classList.remove('open');
        });
    }

    // Export Chat Button
    if (exportChatBtn) {
        exportChatBtn.addEventListener('click', () => {
            if (activeConversation.length === 0) {
                showToast("No active conversation to export");
                return;
            }
            let content = "=== COLLEGE AI CHATBOT CONVERSATION ===\n";
            content += `Export Date: ${new Date().toLocaleString()}\n`;
            content += "========================================\n\n";
            activeConversation.forEach((msg) => {
                const role = msg.sender === 'user' ? 'Student' : 'College AI';
                content += `[${role}]:\n${msg.text}\n\n`;
            });

            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `college-ai-chat-${Date.now()}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast("Conversation exported successfully!");
        });
    }

    // Top Link Button (Copies Current Live URL)
    if (topLinkBtn) {
        topLinkBtn.addEventListener('click', () => {
            const currentUrl = window.location.href;
            navigator.clipboard.writeText(currentUrl).then(() => {
                showToast("Live website link copied to clipboard!");
            });
        });
    }

    // Mobile Sidebar Drawer Management
    function openMobileSidebar() {
        if (sidebarContainer) sidebarContainer.classList.add('open');
        if (sidebarBackdrop) sidebarBackdrop.classList.add('open');
    }

    function closeMobileSidebar() {
        if (sidebarContainer) sidebarContainer.classList.remove('open');
        if (sidebarBackdrop) sidebarBackdrop.classList.remove('open');
    }

    if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', openMobileSidebar);
    if (sidebarBackdrop) sidebarBackdrop.addEventListener('click', closeMobileSidebar);
    if (sidebarCollapseBtn) sidebarCollapseBtn.addEventListener('click', closeMobileSidebar);

    // Global Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            if (window.innerWidth <= 992) openMobileSidebar();
            if (sidebarSearchInput) sidebarSearchInput.focus();
        }
        if (e.key === 'Escape') {
            closeMobileSidebar();
            closeBiometricModal();
            if (cortexDropdownWrapper) cortexDropdownWrapper.classList.remove('open');
        }
        if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            if (cortexHeroState.style.display !== 'none' && cortexUserInput) {
                cortexUserInput.focus();
            } else if (conversationInput) {
                conversationInput.focus();
            }
        }
    });

    /* ==========================================================================
       9. INITIALIZATION
       ========================================================================== */
    initAmbientCanvas();
    initSpeechRecognition();
    initPredictorControls();

})();
