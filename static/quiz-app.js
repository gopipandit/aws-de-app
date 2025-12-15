const API_BASE_URL = '';
let currentUser = null;
let questions = [];
let currentQuestionIndex = 0;
let currentAttempt = null;
let selectedSet = null;
let selectedAnswers = new Set();
let answeredQuestions = new Map();
let timerInterval = null;
let startTime = null;
let elapsedSeconds = 0;

const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');
const scoreDisplay = document.getElementById('score');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const finishBtn = document.getElementById('finish-btn');
const submitAnswerBtn = document.getElementById('submit-answer-btn');
const resultMessage = document.getElementById('result-message');
const multiSelectHint = document.getElementById('multi-select-hint');
const timerDisplay = document.getElementById('timer');
const questionsList = document.getElementById('questions-list');

// Initialize
window.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/check`);
        if (!response.ok) {
            window.location.href = '/';
            return;
        }
        const data = await response.json();
        currentUser = data.user;
        document.getElementById('user-display').textContent = currentUser.name;
    } catch (error) {
        window.location.href = '/';
        return;
    }

    // Get selected question set
    selectedSet = parseInt(localStorage.getItem('selectedSet'));
    if (!selectedSet) {
        window.location.href = '/';
        return;
    }

    document.getElementById('quiz-title').textContent = `Question Set ${selectedSet}`;
    document.getElementById('quiz-set-title').textContent = `Set ${selectedSet}`;

    await loadQuestions();
    startTimer();
});

// Timer Functions
function startTimer() {
    startTime = Date.now();
    timerInterval = setInterval(updateTimer, 1000);
}

function updateTimer() {
    elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
    const hours = Math.floor(elapsedSeconds / 3600);
    const minutes = Math.floor((elapsedSeconds % 3600) / 60);
    const seconds = elapsedSeconds % 60;

    timerDisplay.textContent =
        `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function getFormattedTime() {
    const hours = Math.floor(elapsedSeconds / 3600);
    const minutes = Math.floor((elapsedSeconds % 3600) / 60);
    const seconds = elapsedSeconds % 60;

    if (hours > 0) {
        return `${hours}h ${minutes}m ${seconds}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${seconds}s`;
    } else {
        return `${seconds}s`;
    }
}

async function loadQuestions() {
    try {
        questionText.textContent = 'Loading questions...';

        const response = await fetch(`${API_BASE_URL}/api/questions/set/${selectedSet}`);
        if (!response.ok) {
            throw new Error('Failed to load questions');
        }

        questions = await response.json();

        if (questions.length === 0) {
            questionText.textContent = 'No questions found in this set.';
            return;
        }

        // Start a new attempt
        await startNewAttempt();

        renderQuestionsList();
        displayQuestion();
    } catch (error) {
        console.error('Error loading questions:', error);
        questionText.textContent = 'Error loading questions. Please make sure the server is running.';
    }
}

function renderQuestionsList() {
    questionsList.innerHTML = '';

    questions.forEach((question, index) => {
        const questionItem = document.createElement('div');
        questionItem.className = 'question-item';
        questionItem.onclick = () => goToQuestion(index);

        const answered = answeredQuestions.has(question._id);
        const isCorrect = answered ? answeredQuestions.get(question._id).isCorrect : false;

        if (index === currentQuestionIndex) {
            questionItem.classList.add('active');
        }

        if (answered) {
            questionItem.classList.add('answered');
            if (isCorrect) {
                questionItem.classList.add('correct');
            } else {
                questionItem.classList.add('incorrect');
            }
        }

        questionItem.innerHTML = `
            <div class="question-item-header">
                <span class="question-number">Q${index + 1}</span>
                <span class="question-status">${answered ? (isCorrect ? '✓' : '✗') : ''}</span>
            </div>
            <div class="question-preview">${question.question_text}</div>
        `;

        questionsList.appendChild(questionItem);
    });
}

function goToQuestion(index) {
    if (index >= 0 && index < questions.length) {
        currentQuestionIndex = index;
        displayQuestion();
        renderQuestionsList();
    }
}

async function startNewAttempt() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/attempts/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userId: currentUser.id,
                userName: currentUser.name,
                questionSetNumber: selectedSet
            })
        });

        if (!response.ok) {
            throw new Error('Failed to start attempt');
        }

        currentAttempt = await response.json();
    } catch (error) {
        console.error('Error starting attempt:', error);
        alert('Failed to start quiz. Please try again.');
    }
}

function displayQuestion() {
    const question = questions[currentQuestionIndex];
    questionText.textContent = question.question_text;
    optionsContainer.innerHTML = '';
    resultMessage.textContent = '';
    resultMessage.className = '';
    selectedAnswers.clear();

    // Check if this question was already answered
    const isAnswered = answeredQuestions.has(question._id);
    const previousAnswer = answeredQuestions.get(question._id);

    // Check if question has multiple correct answers
    const isMultiSelect = question.has_multiple_answers === true;

    if (isMultiSelect && !isAnswered) {
        multiSelectHint.style.display = 'block';
    } else {
        multiSelectHint.style.display = 'none';
    }

    // Display options
    Object.entries(question.options).forEach(([key, value]) => {
        const button = document.createElement('button');
        button.className = 'option-btn';

        if (isMultiSelect && !isAnswered) {
            button.classList.add('multi-select');
        }

        button.innerHTML = `<span class="option-label">${key}.</span><span>${value}</span>`;

        if (isAnswered) {
            button.classList.add('disabled');
            if (previousAnswer.correctAnswers.includes(key)) {
                button.classList.add('correct');
            }
            if (previousAnswer.selectedAnswers.includes(key) && !previousAnswer.correctAnswers.includes(key)) {
                button.classList.add('incorrect');
            }
        } else {
            button.onclick = () => selectOption(key, button, isMultiSelect);
        }

        optionsContainer.appendChild(button);
    });

    // Show/hide submit button
    if (isMultiSelect && !isAnswered) {
        submitAnswerBtn.style.display = 'block';
        submitAnswerBtn.disabled = true;
    } else {
        submitAnswerBtn.style.display = 'none';
    }

    // Show previous answer message if answered
    if (isAnswered) {
        if (previousAnswer.isCorrect) {
            resultMessage.textContent = 'Correct!';
            resultMessage.className = 'correct';
        } else {
            resultMessage.textContent = `Incorrect. The correct answer(s): ${previousAnswer.correctAnswers.join(', ')}`;
            resultMessage.className = 'incorrect';
        }
    }

    updateNavigationButtons();
    updateScore();
}

function selectOption(selectedKey, selectedButton, isMultiSelect) {
    const question = questions[currentQuestionIndex];
    const isAnswered = answeredQuestions.has(question._id);
    if (isAnswered) return;

    if (isMultiSelect) {
        // Toggle selection for multi-select
        if (selectedAnswers.has(selectedKey)) {
            selectedAnswers.delete(selectedKey);
            selectedButton.classList.remove('selected');
        } else {
            selectedAnswers.add(selectedKey);
            selectedButton.classList.add('selected');
        }

        submitAnswerBtn.disabled = selectedAnswers.size === 0;
    } else {
        // Single select - submit immediately
        selectedAnswers.clear();
        selectedAnswers.add(selectedKey);
        submitAnswer();
    }
}

async function submitAnswer() {
    if (selectedAnswers.size === 0) return;

    const question = questions[currentQuestionIndex];
    const selectedArray = Array.from(selectedAnswers);
    const correctAnswers = question.correct_answers;

    // INSTANT FEEDBACK - Check answer immediately
    const isCorrect = selectedArray.length === correctAnswers.length &&
                      selectedArray.every(ans => correctAnswers.includes(ans));

    // Store answer info immediately
    answeredQuestions.set(question._id, {
        selectedAnswers: selectedArray,
        correctAnswers: correctAnswers,
        isCorrect: isCorrect
    });

    // Disable all options
    const allButtons = optionsContainer.querySelectorAll('.option-btn');
    allButtons.forEach(btn => {
        btn.classList.add('disabled');
        btn.classList.remove('multi-select');
    });

    // Highlight correct and incorrect answers INSTANTLY
    Object.keys(question.options).forEach((key, index) => {
        const button = allButtons[index];
        if (correctAnswers.includes(key)) {
            button.classList.add('correct');
        }
        if (selectedAnswers.has(key) && !correctAnswers.includes(key)) {
            button.classList.add('incorrect');
        }
    });

    // Show result message INSTANTLY
    if (isCorrect) {
        resultMessage.textContent = 'Correct! ✓';
        resultMessage.className = 'correct';
    } else {
        resultMessage.textContent = `Incorrect. The correct answer(s): ${correctAnswers.join(', ')}`;
        resultMessage.className = 'incorrect';
    }

    submitAnswerBtn.style.display = 'none';
    multiSelectHint.style.display = 'none';
    updateScore();
    updateNavigationButtons();
    renderQuestionsList();

    // Save to backend in background (non-blocking)
    saveAnswerToBackend(question._id, selectedArray);
}

async function saveAnswerToBackend(questionId, selectedAnswers) {
    try {
        await fetch(`${API_BASE_URL}/api/attempts/${currentAttempt.id}/answer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                questionId: questionId,
                selectedAnswers: selectedAnswers
            })
        });
    } catch (error) {
        console.error('Background save failed:', error);
        // Silently fail - user already got instant feedback
    }
}

submitAnswerBtn.addEventListener('click', submitAnswer);

function updateScore() {
    const answeredCount = answeredQuestions.size;
    const correctCount = Array.from(answeredQuestions.values()).filter(a => a.isCorrect).length;

    scoreDisplay.textContent = `Score: ${correctCount}/${answeredCount}`;
}

function updateNavigationButtons() {
    prevBtn.disabled = currentQuestionIndex === 0;

    const allAnswered = answeredQuestions.size === questions.length;

    if (currentQuestionIndex === questions.length - 1) {
        nextBtn.style.display = 'none';
        if (allAnswered) {
            finishBtn.style.display = 'block';
        }
    } else {
        nextBtn.style.display = 'block';
        finishBtn.style.display = 'none';
    }
}

function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
        renderQuestionsList();
    }
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
        renderQuestionsList();
    }
}

async function finishQuiz() {
    try {
        stopTimer();
        const timeTaken = getFormattedTime();

        const response = await fetch(`${API_BASE_URL}/api/attempts/${currentAttempt.id}/complete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to complete attempt');
        }

        const completedAttempt = await response.json();

        const score = completedAttempt.score;
        const total = completedAttempt.total_questions;
        const percentage = Math.round((score / total) * 100);

        if (confirm(`Quiz Completed!\n\nYour Score: ${score}/${total} (${percentage}%)\nTime Taken: ${timeTaken}\n\nWould you like to return to the question sets?`)) {
            window.location.href = '/home';
        }
    } catch (error) {
        console.error('Error finishing quiz:', error);
        alert('Failed to save your quiz results. Please try again.');
    }
}

prevBtn.addEventListener('click', previousQuestion);
nextBtn.addEventListener('click', nextQuestion);
finishBtn.addEventListener('click', finishQuiz);

function quitQuiz() {
    const answeredCount = answeredQuestions.size;
    const totalQuestions = questions.length;
    const timeTaken = getFormattedTime();

    if (answeredCount === 0) {
        if (confirm('Are you sure you want to quit the quiz?')) {
            stopTimer();
            window.location.href = '/home';
        }
        return;
    }

    const correctCount = Array.from(answeredQuestions.values()).filter(a => a.isCorrect).length;
    const message = `You have answered ${answeredCount} out of ${totalQuestions} questions.\nYour current score: ${correctCount}/${answeredCount}\nTime elapsed: ${timeTaken}\n\nAre you sure you want to quit?`;

    if (confirm(message)) {
        stopTimer();
        window.location.href = '/home';
    }
}
