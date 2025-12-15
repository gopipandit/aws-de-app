const API_BASE_URL = '';
let currentPage = 1;
let totalPages = 1;
let allQuestions = [];
let editingQuestionId = null;

window.addEventListener('DOMContentLoaded', () => {
    loadQuestions();
    initializeForm();
});

async function loadQuestions(page = 1) {
    const container = document.getElementById('questions-list');
    container.innerHTML = '<div class="loading">Loading questions...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/questions?page=${page}&limit=50`);

        if (!response.ok) {
            throw new Error('Failed to load questions');
        }

        const data = await response.json();
        allQuestions = data.questions;
        currentPage = data.currentPage;
        totalPages = data.totalPages;

        displayQuestions();
        displayPagination();

    } catch (error) {
        console.error('Error loading questions:', error);
        container.innerHTML = '<div class="loading">Failed to load questions.</div>';
    }
}

function displayQuestions() {
    const container = document.getElementById('questions-list');

    if (allQuestions.length === 0) {
        container.innerHTML = '<div class="loading">No questions found.</div>';
        return;
    }

    container.innerHTML = '';

    allQuestions.forEach(question => {
        const questionItem = document.createElement('div');
        questionItem.className = 'question-item';

        // Use _id if id is not available
        const qId = question.id || question._id;

        if (editingQuestionId === qId) {
            questionItem.classList.add('active');
        }

        const questionText = question.question_text || 'No text';
        const displayText = questionText.length > 150 ? questionText.substring(0, 150) + '...' : questionText;

        questionItem.innerHTML = `
            <div class="question-text">${displayText}</div>
            <div class="question-meta">
                Set: ${question.question_set || 'N/A'} |
                ${question.difficulty || 'Medium'} |
                Correct: ${(question.correct_answers || []).join(', ')}
            </div>
            <div class="question-actions">
                <button class="btn btn-primary btn-sm" onclick="editQuestion('${qId}')">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteQuestion('${qId}')">Delete</button>
            </div>
        `;

        container.appendChild(questionItem);
    });
}

function displayPagination() {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    if (totalPages <= 1) return;

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.className = 'btn btn-sm';
        button.classList.add(i === currentPage ? 'btn-primary' : 'btn-secondary');
        button.textContent = i;
        button.onclick = () => loadQuestions(i);
        pagination.appendChild(button);
    }
}

function initializeForm() {
    const keys = ['A', 'B', 'C', 'D'];
    keys.forEach(key => addOption(key));
}

function addOption(key = null) {
    const container = document.getElementById('options-container');

    if (!key) {
        const existing = container.querySelectorAll('.option-row');
        const lastKey = existing.length > 0 ?
            existing[existing.length - 1].querySelector('.option-key').textContent : '@';
        key = String.fromCharCode(lastKey.charCodeAt(0) + 1);
    }

    const row = document.createElement('div');
    row.className = 'option-row';
    row.innerHTML = `
        <span class="option-key">${key}</span>
        <input type="text" class="option-value" placeholder="Option ${key} text" required>
        <label title="Mark as correct" style="display: flex; align-items: center; gap: 5px; cursor: pointer;">
            <input type="checkbox" class="option-correct">
            <span style="font-size: 12px;">Correct</span>
        </label>
        <button type="button" class="btn btn-danger btn-sm" onclick="removeOption(this)">×</button>
    `;

    container.appendChild(row);
}

function removeOption(button) {
    button.parentElement.remove();
}

async function saveQuestion(e) {
    e.preventDefault();

    const questionId = document.getElementById('question-id').value;
    const questionText = document.getElementById('question-text').value.trim();
    const category = document.getElementById('category').value.trim();
    const difficulty = document.getElementById('difficulty').value;
    const questionSet = parseInt(document.getElementById('question-set').value);

    // Collect options
    const optionRows = document.querySelectorAll('.option-row');
    const options = {};
    const correctAnswers = [];

    optionRows.forEach(row => {
        const key = row.querySelector('.option-key').textContent;
        const value = row.querySelector('.option-value').value.trim();
        const isCorrect = row.querySelector('.option-correct').checked;

        if (value) {
            options[key] = value;
            if (isCorrect) {
                correctAnswers.push(key);
            }
        }
    });

    if (correctAnswers.length === 0) {
        alert('Please mark at least one correct answer!');
        return;
    }

    const questionData = {
        question_text: questionText,
        options: options,
        correct_answers: correctAnswers,
        category: category,
        difficulty: difficulty,
        question_set: questionSet
    };

    try {
        let response;

        if (questionId) {
            response = await fetch(`${API_BASE_URL}/api/questions/${questionId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(questionData)
            });
        } else {
            response = await fetch(`${API_BASE_URL}/api/questions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(questionData)
            });
        }

        if (!response.ok) {
            throw new Error('Failed to save question');
        }

        alert(questionId ? 'Question updated!' : 'Question added!');
        resetForm();
        loadQuestions(currentPage);

    } catch (error) {
        console.error('Error saving question:', error);
        alert('Failed to save question.');
    }
}

async function editQuestion(questionId) {
    try {
        console.log('Editing question with ID:', questionId);
        const response = await fetch(`${API_BASE_URL}/api/questions/${questionId}`);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            throw new Error('Failed to load question');
        }

        const question = await response.json();
        console.log('Loaded question:', question);
        editingQuestionId = questionId;

        document.getElementById('form-title').textContent = 'Edit Question';
        document.getElementById('question-id').value = question.id;
        document.getElementById('question-text').value = question.question_text;
        document.getElementById('category').value = question.category;
        document.getElementById('difficulty').value = question.difficulty;
        document.getElementById('question-set').value = question.question_set;

        // Clear and recreate options
        const optionsContainer = document.getElementById('options-container');
        optionsContainer.innerHTML = '';

        Object.entries(question.options).forEach(([key, value]) => {
            addOption(key);
            const rows = optionsContainer.querySelectorAll('.option-row');
            const lastRow = rows[rows.length - 1];
            lastRow.querySelector('.option-value').value = value;
            lastRow.querySelector('.option-correct').checked = question.correct_answers.includes(key);
        });

        displayQuestions();

        // Scroll to form
        document.getElementById('form-title').scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Error loading question:', error);
        alert('Failed to load question.');
    }
}

async function deleteQuestion(questionId) {
    if (!confirm('Delete this question?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/questions/${questionId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete question');
        }

        alert('Question deleted!');
        loadQuestions(currentPage);

        if (editingQuestionId === questionId) {
            resetForm();
        }

    } catch (error) {
        console.error('Error deleting question:', error);
        alert('Failed to delete question.');
    }
}

function showNewQuestionForm() {
    resetForm();
}

function resetForm() {
    editingQuestionId = null;
    document.getElementById('form-title').textContent = 'Add New Question';
    document.getElementById('question-form').reset();
    document.getElementById('question-id').value = '';

    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';

    const keys = ['A', 'B', 'C', 'D'];
    keys.forEach(key => addOption(key));

    displayQuestions();
}
