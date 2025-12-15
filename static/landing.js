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

            // Check if user has attempted this set
            const attempt = userAttempts.find(a =>
                a.question_set_number === set.setNumber && a.status === 'completed'
            );

            if (attempt) {
                setItem.classList.add('completed');
            }

            setItem.innerHTML = `
                <div class="set-number">Set ${set.setNumber}</div>
                <div class="set-info">${set.questionCount} questions</div>
                ${attempt ? `<div class="set-score">Score: ${attempt.score}/${attempt.total_questions}</div>` : ''}
            `;

            setItem.onclick = () => startQuiz(set.setNumber);
            setListDiv.appendChild(setItem);
        });

    } catch (error) {
        console.error('Error loading question sets:', error);
        loadingDiv.style.display = 'none';
        errorDiv.textContent = 'Failed to load question sets. Please make sure the server is running.';
        errorDiv.style.display = 'block';
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
