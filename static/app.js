/**
 * CORTEX • COLLEGE AI CHATBOT SYSTEM
 * Implementation matching Kirill Soliar (SOLAR Digital) Dribbble Design
 */

(function () {
    'use strict';

    // State Variables
    let voiceEnabled = true;
    let isWaitingForResponse = false;
    let recognition = null;
    let isListening = false;
    let activeConversation = [];

    // DOM Elements
    const cortexHeroState = document.getElementById('cortex-hero-state');
    const cortexChatState = document.getElementById('cortex-chat-state');
    const chatThreadWrapper = document.getElementById('chat-thread-wrapper');
    const conversationDockWrapper = document.getElementById('conversation-dock-wrapper');
    
    // Inputs
    const cortexUserInput = document.getElementById('cortex-user-input');
    const conversationInput = document.getElementById('conversation-input');
    const dockSubmitBtn = document.getElementById('dock-submit-btn');
    
    // Mic Buttons
    const cortexMicBtn = document.getElementById('cortex-mic-btn');
    const dockSpeechBtn = document.getElementById('dock-speech-btn');
    
    // Navigation & Reset Buttons
    const newChatBtn = document.getElementById('new-chat-btn');
    const brandHomeBtn = document.getElementById('brand-home-btn');
    const logoutBtn = document.getElementById('logout-btn');
    
    // Header Controls
    const cortexDropdownBtn = document.getElementById('cortex-dropdown-btn');
    const cortexDropdownWrapper = document.getElementById('cortex-dropdown-wrapper');
    const exportChatBtn = document.getElementById('export-chat-btn');
    const upgradeBtn = document.getElementById('upgrade-btn');
    const topMoreBtn = document.getElementById('top-more-btn');
    const topLinkBtn = document.getElementById('top-link-btn');
    
    // Sidebar Elements
    const sidebarContainer = document.getElementById('sidebar-container');
    const sidebarBackdrop = document.getElementById('sidebar-backdrop');
    const sidebarCollapseBtn = document.getElementById('sidebar-collapse-btn');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebarSearchInput = document.getElementById('sidebar-search-input');
    
    // Footer Elements
    const translateBtn = document.getElementById('translate-btn');
    const helpBtn = document.getElementById('help-btn');
    const toastContainer = document.getElementById('toast-container');

    /* ==========================================================================
       TOAST NOTIFICATION UTILITY
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
       SPEECH SYNTHESIS (VOICE READOUT)
       ========================================================================== */
    function speakText(text) {
        if (!voiceEnabled || !('speechSynthesis' in window)) return;
        try {
            window.speechSynthesis.cancel();
            const cleanText = text.replace(/<[^>]*>?/gm, '').slice(0, 300);
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            window.speechSynthesis.speak(utterance);
        } catch (e) {
            console.warn('Speech synthesis error:', e);
        }
    }

    /* ==========================================================================
       SPEECH RECOGNITION (VOICE INPUT)
       ========================================================================== */
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
            console.warn("Speech error:", event.error);
            stopListening();
        };

        recognition.onend = function () {
            stopListening();
        };
    }

    function toggleSpeechRecognition() {
        if (!recognition) {
            showToast("Speech recognition not available on this browser");
            return;
        }
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    }

    function stopListening() {
        isListening = false;
        if (cortexMicBtn) cortexMicBtn.classList.remove('listening');
        if (dockSpeechBtn) dockSpeechBtn.classList.remove('listening');
    }

    /* ==========================================================================
       STATE TRANSITIONS & CHAT RENDERING
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
        activeConversation = [];
        if (chatThreadWrapper) chatThreadWrapper.innerHTML = '';
        switchToHeroState();
        showToast("New conversation started");
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

    function renderAiResponse(text) {
        const row = document.createElement('div');
        row.className = 'chat-msg-row ai-msg-row';
        
        const card = document.createElement('div');
        card.className = 'ai-chat-card';

        const p = document.createElement('p');
        p.className = 'ai-msg-text';
        p.textContent = text;
        card.appendChild(p);

        // Actions row (Thumbs up/down, Copy, Speak)
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

        actions.querySelector('.copy-btn').addEventListener('click', function () {
            navigator.clipboard.writeText(text).then(() => showToast("Copied to clipboard!"));
        });

        actions.querySelector('.speak-btn').addEventListener('click', function () {
            speakText(text);
        });

        card.appendChild(actions);
        row.appendChild(card);
        chatThreadWrapper.appendChild(row);
        scrollToBottom();

        // Voice Readout
        speakText(text);
    }

    function scrollToBottom() {
        const container = document.getElementById('cortex-scroll-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }

    /* ==========================================================================
       BACKEND ML INTEGRATION
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
                throw new Error(`Server returned ${response.status}`);
            }

            const data = await response.json();
            const botResponse = data.response || "No response received.";
            renderAiResponse(botResponse);
            activeConversation.push({ sender: 'ai', text: botResponse });
        } catch (error) {
            console.error("Chat error:", error);
            renderAiResponse("I apologize, but I could not connect to the campus assistant knowledge server. Please try again.");
        } finally {
            isWaitingForResponse = false;
        }
    }

    /* ==========================================================================
       EVENT LISTENERS
       ========================================================================== */
    // Hero Textarea Enter Key
    if (cortexUserInput) {
        cortexUserInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const text = cortexUserInput.value.trim();
                if (text) dispatchUserQuery(text);
            }
        });
    }

    // Conversation Dock Enter Key & Send Button
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

    // 3 Quick Action Cards
    document.querySelectorAll('.cortex-action-card').forEach(card => {
        card.addEventListener('click', (e) => {
            const query = card.dataset.query;
            if (query) dispatchUserQuery(query);
        });
    });

    // History Items
    document.querySelectorAll('.history-item').forEach(item => {
        item.addEventListener('click', (e) => {
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
    if (logoutBtn) logoutBtn.addEventListener('click', resetSession);

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
                if (label) label.textContent = modelName;
                document.querySelectorAll('.cortex-menu-item').forEach(i => i.classList.remove('active'));
                e.target.classList.add('active');
                cortexDropdownWrapper.classList.remove('open');
                showToast(`Switched model context to: ${modelName}`);
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
            let content = "Cortex College AI — Conversation Export\n";
            content += "========================================\n\n";
            activeConversation.forEach(msg => {
                content += `[${msg.sender.toUpperCase()}]: ${msg.text}\n\n`;
            });

            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `cortex_chat_${Date.now()}.txt`;
            a.click();
            URL.revokeObjectURL(url);
            showToast("Conversation exported successfully!");
        });
    }

    // Top Upgrade & Link Buttons
    if (upgradeBtn) {
        upgradeBtn.addEventListener('click', () => {
            showToast("Cortex Pro: Unlimited campus research and AI reasoning unlocked!");
        });
    }

    if (topLinkBtn) {
        topLinkBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(window.location.href).then(() => {
                showToast("Shareable chat link copied to clipboard!");
            });
        });
    }

    if (topMoreBtn) {
        topMoreBtn.addEventListener('click', () => {
            showToast("Cortex v2.5 • Scikit-Learn Decision Tree Classifier active");
        });
    }

    // Deeper Research & Tools
    const deeperResearchBtn = document.getElementById('deeper-research-btn');
    if (deeperResearchBtn) {
        deeperResearchBtn.addEventListener('click', () => {
            showToast("Deeper Research mode enabled for next question");
        });
    }

    const savedPromptsBtn = document.getElementById('saved-prompts-btn');
    if (savedPromptsBtn) {
        savedPromptsBtn.addEventListener('click', () => {
            showToast("Browse quick campus topics from the cards below");
        });
    }

    const attachFileBtn = document.getElementById('attach-file-btn');
    if (attachFileBtn) {
        attachFileBtn.addEventListener('click', () => {
            showToast("College syllabus and prospectus attachments supported");
        });
    }

    // Mobile Sidebar Drawer
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

    if (sidebarCollapseBtn) {
        sidebarCollapseBtn.addEventListener('click', () => {
            if (window.innerWidth <= 992) {
                closeMobileSidebar();
            } else {
                sidebarContainer.style.display = sidebarContainer.style.display === 'none' ? 'flex' : 'none';
                const frame = document.getElementById('window-frame');
                if (frame) {
                    frame.style.gridTemplateColumns = sidebarContainer.style.display === 'none' ? '1fr' : '260px 1fr';
                }
            }
        });
    }

    // Footer Badges
    if (translateBtn) {
        translateBtn.addEventListener('click', () => {
            showToast("Language translation: English (Default), Hindi, Spanish");
        });
    }

    if (helpBtn) {
        helpBtn.addEventListener('click', () => {
            showToast("Cortex Architecture: Scikit-learn ML + TF-IDF Vectorizer");
        });
    }

    // Initialize Speech Recognition
    initSpeechRecognition();

})();
