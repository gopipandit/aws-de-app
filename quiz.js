let questions = [];
let currentQuestionIndex = 0;
let userAnswers = [];
let score = 0;

const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');
const questionCounter = document.getElementById('question-counter');
const scoreDisplay = document.getElementById('score');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const restartBtn = document.getElementById('restart-btn');
const resultMessage = document.getElementById('result-message');

async function loadQuestions() {
    try {
        const response = await fetch('qna.json');
        questions = await response.json();
        initQuiz();
    } catch (error) {
        questionText.textContent = 'Error loading questions. Please make sure qna.json is in the same directory.';
        console.error('Error loading questions:', error);
    }
}

function initQuiz() {
    currentQuestionIndex = 0;
    userAnswers = new Array(questions.length).fill(null);
    score = 0;
    updateScore();
    displayQuestion();
}

function displayQuestion() {
    const question = questions[currentQuestionIndex];
    questionText.textContent = question.question_text;
    optionsContainer.innerHTML = '';
    resultMessage.textContent = '';
    resultMessage.className = '';

    questionCounter.textContent = `Question ${currentQuestionIndex + 1} of ${questions.length}`;

    const optionKeys = Object.keys(question.options);
    optionKeys.forEach(key => {
        const button = document.createElement('button');
        button.className = 'option-btn';
        button.innerHTML = `<span class="option-label">${key}.</span><span>${question.options[key]}</span>`;
        button.onclick = () => selectOption(key, button);

        const userAnswer = userAnswers[currentQuestionIndex];
        if (userAnswer) {
            button.classList.add('disabled');
            if (key === question.correct_answer) {
                button.classList.add('correct');
            }
            if (key === userAnswer && userAnswer !== question.correct_answer) {
                button.classList.add('incorrect');
            }
        }

        optionsContainer.appendChild(button);
    });

    updateNavigationButtons();
}

function selectOption(selectedKey, selectedButton) {
    if (userAnswers[currentQuestionIndex]) {
        return;
    }

    const question = questions[currentQuestionIndex];
    userAnswers[currentQuestionIndex] = selectedKey;

    const allButtons = optionsContainer.querySelectorAll('.option-btn');
    allButtons.forEach(btn => {
        btn.classList.add('disabled');
    });

    const optionKeys = Object.keys(question.options);
    optionKeys.forEach((key, index) => {
        const button = allButtons[index];
        if (key === question.correct_answer) {
            button.classList.add('correct');
        }
        if (key === selectedKey && selectedKey !== question.correct_answer) {
            button.classList.add('incorrect');
        }
    });

    if (selectedKey === question.correct_answer) {
        score++;
        resultMessage.textContent = 'Correct!';
        resultMessage.className = 'correct';
    } else {
        resultMessage.textContent = `Incorrect. The correct answer is ${question.correct_answer}.`;
        resultMessage.className = 'incorrect';
    }

    updateScore();
}

function updateScore() {
    const answeredQuestions = userAnswers.filter(answer => answer !== null).length;
    scoreDisplay.textContent = `Score: ${score}/${answeredQuestions}`;
}

function updateNavigationButtons() {
    prevBtn.disabled = currentQuestionIndex === 0;

    if (currentQuestionIndex === questions.length - 1) {
        const allAnswered = userAnswers.every(answer => answer !== null);
        if (allAnswered) {
            nextBtn.style.display = 'none';
            restartBtn.style.display = 'block';
        } else {
            nextBtn.textContent = 'Next';
        }
    } else {
        nextBtn.textContent = 'Next';
        nextBtn.style.display = 'block';
        restartBtn.style.display = 'none';
    }
}

function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    }
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

function restartQuiz() {
    if (confirm(`Your final score: ${score}/${questions.length}\n\nDo you want to restart the quiz?`)) {
        initQuiz();
        nextBtn.style.display = 'block';
        restartBtn.style.display = 'none';
    }
}

prevBtn.addEventListener('click', previousQuestion);
nextBtn.addEventListener('click', nextQuestion);
restartBtn.addEventListener('click', restartQuiz);

loadQuestions();
