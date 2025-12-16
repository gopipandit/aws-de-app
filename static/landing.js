const API_BASE_URL = '';
let currentUser = null;
let questionSets = [];
let userAttempts = [];

// Check authentication on page load
window.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('login-screen').style.display = 'none';
    await checkAuth();
});

async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/check`);

        if (response.ok) {
            const data = await response.json();
            currentUser = data.user;
            await loadUserProgress();
            await showQuestionSets();
        } else {
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Auth check error:', error);
        window.location.href = '/';
    }
}

async function loadUserProgress() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users/progress`);

        if (response.ok) {
            const data = await response.json();
            userAttempts = data.attempts;
        }
    } catch (error) {
        console.error('Error loading progress:', error);
        userAttempts = [];
    }
}

async function showQuestionSets() {
    document.getElementById('question-sets-screen').style.display = 'block';

    document.getElementById('welcome-message').textContent = `Welcome, ${currentUser.name}!`;

    // Set user info in profile dropdown
    const initials = currentUser.name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);

    // Populate header profile dropdown
    document.getElementById('user-initials-header').textContent = initials;
    document.getElementById('dropdown-user-name-header').textContent = currentUser.name;
    document.getElementById('dropdown-user-email-header').textContent = currentUser.email;

    // Update user stats
    document.getElementById('total-attempts').textContent = userAttempts.length;

    const completedAttempts = userAttempts.filter(a => a.status === 'completed');
    let bestScore = 0;
    if (completedAttempts.length > 0) {
        bestScore = Math.max(...completedAttempts.map(a =>
            Math.round((a.score / a.total_questions) * 100)
        ));
    }
    document.getElementById('best-score').textContent = `${bestScore}%`;

    // Load question sets
    await loadQuestionSets();
}

async function loadQuestionSets() {
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error-message');
    const setListDiv = document.getElementById('set-list');

    loadingDiv.style.display = 'block';
    errorDiv.style.display = 'none';
    setListDiv.innerHTML = '';

    try {
        const response = await fetch(`${API_BASE_URL}/api/questions/sets`);

        if (!response.ok) {
            throw new Error('Failed to load question sets');
        }

        questionSets = await response.json();
        loadingDiv.style.display = 'none';

        if (questionSets.length === 0) {
            errorDiv.textContent = 'No question sets found. Please run the migration script first.';
            errorDiv.style.display = 'block';
            return;
        }

        // Display question sets
        questionSets.forEach(set => {
            const setItem = document.createElement('div');
            setItem.className = 'set-item';
            setItem.dataset.setNumber = set.setNumber;

            // Check if user has attempted this set
            const attempt = userAttempts.find(a =>
                a.question_set_number === set.setNumber && a.status === 'completed'
            );

            if (attempt) {
                setItem.classList.add('completed');
            }

            const scoreHtml = attempt ? `<div class="set-score">✓ Score: ${attempt.score}/${attempt.total_questions}</div>` : '';

            setItem.innerHTML = `
                <div class="set-header" onclick="toggleSetExpansion(${set.setNumber})">
                    <div class="set-header-left">
                        <div class="set-number">Set ${set.setNumber}</div>
                        <div class="set-info">
                            <span>📝 ${set.questionCount} questions</span>
                            ${scoreHtml}
                        </div>
                    </div>
                    <div class="set-header-right">
                        <button class="start-quiz-btn" onclick="event.stopPropagation(); startQuiz(${set.setNumber})">
                            Start Quiz →
                        </button>
                        <span class="expand-icon">▼</span>
                    </div>
                </div>
                <div class="set-content">
                    <div class="questions-preview">
                        <h4>Questions Preview:</h4>
                        <div class="loading-questions">Click to load questions...</div>
                    </div>
                </div>
            `;

            setListDiv.appendChild(setItem);
        });

    } catch (error) {
        console.error('Error loading question sets:', error);
        loadingDiv.style.display = 'none';
        errorDiv.textContent = 'Failed to load question sets. Please make sure the server is running.';
        errorDiv.style.display = 'block';
    }
}

async function toggleSetExpansion(setNumber) {
    const setItem = document.querySelector(`.set-item[data-set-number="${setNumber}"]`);
    const wasExpanded = setItem.classList.contains('expanded');

    // Close all other expanded sets
    document.querySelectorAll('.set-item.expanded').forEach(item => {
        if (item !== setItem) {
            item.classList.remove('expanded');
        }
    });

    // Toggle current set
    if (wasExpanded) {
        setItem.classList.remove('expanded');
    } else {
        setItem.classList.add('expanded');

        // Load questions if not already loaded
        const previewDiv = setItem.querySelector('.questions-preview');
        if (previewDiv.dataset.loaded !== 'true') {
            await loadQuestionPreview(setNumber, previewDiv);
        }
    }
}

async function loadQuestionPreview(setNumber, previewDiv) {
    const loadingDiv = previewDiv.querySelector('.loading-questions');
    loadingDiv.textContent = 'Loading questions...';

    try {
        const response = await fetch(`${API_BASE_URL}/api/questions/set/${setNumber}`);

        if (!response.ok) {
            throw new Error('Failed to load questions');
        }

        const questions = await response.json();

        // Create question list
        const questionListHtml = questions.slice(0, 10).map((q, idx) => {
            // Truncate long question text
            const questionText = q.question_text.length > 120
                ? q.question_text.substring(0, 120) + '...'
                : q.question_text;

            return `
                <li class="question-item">
                    <span class="question-number">Q${idx + 1}.</span>
                    <span class="question-text">${questionText}</span>
                </li>
            `;
        }).join('');

        const moreText = questions.length > 10
            ? `<li class="question-item" style="color: #999; font-style: italic;">
                    <span class="question-number"></span>
                    <span class="question-text">... and ${questions.length - 10} more questions</span>
                </li>`
            : '';

        previewDiv.innerHTML = `
            <h4>Questions Preview (${questions.length} total):</h4>
            <ul class="question-list">
                ${questionListHtml}
                ${moreText}
            </ul>
        `;

        previewDiv.dataset.loaded = 'true';

    } catch (error) {
        console.error('Error loading questions:', error);
        loadingDiv.textContent = 'Failed to load questions. Click to try again.';
        loadingDiv.style.color = '#dc3545';
    }
}

function startQuiz(setNumber) {
    localStorage.setItem('selectedSet', setNumber);
    window.location.href = '/quiz';
}

async function logout() {
    try {
        await fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: 'POST'
        });
        window.location.href = '/';
    } catch (error) {
        console.error('Logout error:', error);
        window.location.href = '/';
    }
}

// Profile dropdown functions
function toggleProfileDropdown() {
    const dropdown = document.getElementById('profile-dropdown-header');
    dropdown.classList.toggle('show');
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const profileContainer = document.querySelector('.user-profile-container');
    const dropdownHeader = document.getElementById('profile-dropdown-header');

    if (profileContainer && dropdownHeader && !profileContainer.contains(event.target)) {
        dropdownHeader.classList.remove('show');
    }
});

async function handleLogout(event) {
    event.preventDefault();

    try {
        await fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: 'POST'
        });
        window.location.href = '/';
    } catch (error) {
        console.error('Logout failed:', error);
        window.location.href = '/';
    }
}
