/**
 * CORTEX • 120Hz HIGH-REFRESH RATE COLLEGE AI SYSTEM
 * Interactive, Modern, Clutter-Free Campus Experience
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
    
    // Sidebar Elements
    const sidebarContainer = document.getElementById('sidebar-container');
    const sidebarBackdrop = document.getElementById('sidebar-backdrop');
    const sidebarCollapseBtn = document.getElementById('sidebar-collapse-btn');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebarSearchInput = document.getElementById('sidebar-search-input');
    
    // Interactive 3D Orb & FPS Badge
    const interactiveOrb = document.getElementById('interactive-orb');
    const orbCore = document.getElementById('orb-core');
    const orbAura = document.getElementById('orb-aura');
    const fpsCounter = document.getElementById('fps-counter');
    const ambientCanvas = document.getElementById('ambient-canvas');
    const toastContainer = document.getElementById('toast-container');

    /* ==========================================================================
       1. 120Hz PRECISION AMBIENT CANVAS & FPS BENCHMARK ENGINE
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
                hue: Math.random() > 0.5 ? 265 : 285 // Lavender / violet tones
            });
        }
    }

    function render120HzLoop(now) {
        const dt = (now - lastFrameTime) / 1000;
        lastFrameTime = now;
        frameCount++;

        // Smooth FPS Calculation
        if (now - lastFpsUpdate >= 500) {
            const currentFps = Math.round((frameCount * 1000) / (now - lastFpsUpdate));
            fpsSmoothed = Math.min(144, Math.round(fpsSmoothed * 0.7 + currentFps * 0.3));
            if (fpsCounter) {
                fpsCounter.textContent = `${fpsSmoothed} FPS`;
            }
            frameCount = 0;
            lastFpsUpdate = now;
        }

        // Draw Ambient Particles
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
       2. INTERACTIVE 3D LIQUID ORB (PHYSICS & SOUNDWAVE)
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
        
        // Smooth lerp
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
            showToast("College AI Core Online • 120Hz Interpolation");
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
        }, 2400);
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
       5. STATE TRANSITIONS & TYPEWRITER CHAT RENDERING
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

    // Dynamic Follow-up Suggestions Generator based on topic
    function getFollowUpSuggestions(query) {
        const lower = query.toLowerCase();
        if (lower.includes('admission') || lower.includes('eligibility')) {
            return [
                { label: "💰 Fee structure", query: "What is the fee structure for engineering?" },
                { label: "📚 Courses offered", query: "What courses and branches are offered?" },
                { label: "📞 Contact office", query: "How can I contact the college administration?" }
            ];
        } else if (lower.includes('fee') || lower.includes('cost') || lower.includes('scholarship')) {
            return [
                { label: "🏢 Hostel accommodation", query: "Does the college provide hostel facilities?" },
                { label: "💼 Placement records", query: "What is the highest placement package?" },
                { label: "🎓 Admission cutoff", query: "What is the admission cutoff score?" }
            ];
        } else if (lower.includes('placement') || lower.includes('package') || lower.includes('company')) {
            return [
                { label: "🏢 Top recruiters", query: "Which companies visit for campus placement?" },
                { label: "📚 B.Tech departments", query: "What courses and engineering branches are offered?" },
                { label: "💰 Average package", query: "What is the average placement package?" }
            ];
        } else {
            return [
                { label: "🎓 Admission requirements", query: "What is the admission process and eligibility criteria?" },
                { label: "💰 Annual fees", query: "How much is the college fee for engineering?" },
                { label: "🏢 Hostel & mess", query: "Does the college have hostel facilities?" }
            ];
        }
    }

    function renderAiResponse(fullText, userQuery) {
        const row = document.createElement('div');
        row.className = 'chat-msg-row ai-msg-row';
        
        const card = document.createElement('div');
        card.className = 'ai-chat-card';

        const p = document.createElement('p');
        p.className = 'ai-msg-text';
        
        // Streaming typewriter cursor
        const cursor = document.createElement('span');
        cursor.className = 'streaming-cursor';
        p.appendChild(cursor);
        card.appendChild(p);

        // Actions row (Thumbs, Copy, Speak)
        const actions = document.createElement('div');
        actions.className = 'ai-msg-actions';
        actions.innerHTML = `
            <button class="ai-action-icon-btn thumbs-up" title="Helpful" aria-label="Thumbs up">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
                </svg>
            </button>
            <button class="ai-action-icon-btn thumbs-down" title="Unhelpful" aria-label="Thumbs down">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3"></path>
                </svg>
            </button>
            <button class="ai-action-icon-btn copy-btn" title="Copy text" aria-label="Copy">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
            </button>
            <button class="ai-action-icon-btn speak-btn" title="Listen audio" aria-label="Speak">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                    <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                </svg>
            </button>
        `;

        actions.querySelector('.thumbs-up').addEventListener('click', function () {
            this.classList.toggle('active');
            actions.querySelector('.thumbs-down').classList.remove('active');
            showToast("Thank you for your feedback!");
        });

        actions.querySelector('.thumbs-down').addEventListener('click', function () {
            this.classList.toggle('active');
            actions.querySelector('.thumbs-up').classList.remove('active');
            showToast("Feedback recorded.");
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
        const charsPerFrame = Math.max(1, Math.ceil(textLength / 60)); // Fast responsive stream

        function streamText() {
            if (charIndex < textLength) {
                const nextChunk = fullText.slice(charIndex, charIndex + charsPerFrame);
                p.insertBefore(document.createTextNode(nextChunk), cursor);
                charIndex += charsPerFrame;
                scrollToBottom();
                requestAnimationFrame(streamText);
            } else {
                cursor.remove();
                
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
       6. BACKEND ML INTEGRATION
       ========================================================================== */
    async function dispatchUserQuery(queryText) {
        if (!queryText || isWaitingForResponse) return;
        isWaitingForResponse = true;

        // Switch view to conversation
        switchToConversationState();

        // Clear inputs
        if (cortexUserInput) cortexUserInput.value = '';
        if (conversationInput) conversationInput.value = '';

        // Render user message
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
            renderAiResponse(botResponse, queryText);
            activeConversation.push({ sender: 'ai', text: botResponse });
        } catch (error) {
            console.error("Chat error:", error);
            renderAiResponse("I apologize, but I could not connect to the campus assistant knowledge server. Please check your connection and try again.", queryText);
        } finally {
            isWaitingForResponse = false;
        }
    }

    /* ==========================================================================
       7. EVENT LISTENERS & SHORTCUTS
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
                showToast(`Assistant context: ${e.target.textContent}`);
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
            activeConversation.forEach((msg, idx) => {
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

    // Global Keyboard Shortcuts (⌘K / Ctrl+K, Slash, Escape)
    document.addEventListener('keydown', (e) => {
        // Ctrl+K / Cmd+K -> Focus Sidebar Search
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            if (window.innerWidth <= 992) openMobileSidebar();
            if (sidebarSearchInput) sidebarSearchInput.focus();
        }
        // Escape -> Close drawer or return to hero view
        if (e.key === 'Escape') {
            closeMobileSidebar();
            if (cortexDropdownWrapper) cortexDropdownWrapper.classList.remove('open');
        }
        // '/' when not inside input -> Focus main input
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
       8. INITIALIZATION
       ========================================================================== */
    initAmbientCanvas();
    initSpeechRecognition();

})();
