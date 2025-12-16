from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime
from dotenv import load_dotenv
import bcrypt
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth_page'))
        return f(*args, **kwargs)
    return decorated_function

# MongoDB connection
MONGO_URI = os.getenv('uri')
DB_NAME = 'AWS_DE_V2'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
questions_collection = db['questions']
users_collection = db['users']
attempts_collection = db['attempts']
coding_questions_collection = db['coding_questions']
coding_submissions_collection = db['coding_submissions']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/login')
def login_page():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('auth.html')

@app.route('/signup')
def signup_page():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('auth.html')

@app.route('/auth')
def auth_page():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('auth.html')

@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/certification/aws-dea')
def aws_dea_cert():
    return render_template('aws_dea_cert.html')

@app.route('/coding-practice')
def coding_practice():
    return render_template('coding_practice.html')

@app.route('/interview-prep')
def interview_prep():
    return render_template('interview_prep.html')

# User Profile Pages
@app.route('/account')
@login_required
def account():
    return render_template('under_construction.html', page_title='Account')

@app.route('/settings')
@login_required
def settings():
    return render_template('under_construction.html', page_title='Settings')

@app.route('/my-courses')
@login_required
def my_courses():
    return render_template('my_courses.html')

@app.route('/my-courses/aws-certified-data-engineer-associate')
@login_required
def aws_dea_course():
    return render_template('landing.html')

@app.route('/payments')
@login_required
def payments():
    return render_template('under_construction.html', page_title='Payments')

@app.route('/exam-history')
@login_required
def exam_history():
    return render_template('exam_history.html')

@app.route('/performance-analytics')
@login_required
def performance_analytics():
    return render_template('under_construction.html', page_title='Performance Analytics')

# Authentication Routes

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()

    if not email or not password or not name:
        return jsonify({'error': 'All fields are required'}), 400

    # Check if user already exists
    existing_user = users_collection.find_one({'email': email})
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create user
    result = users_collection.insert_one({
        'email': email,
        'name': name,
        'password': hashed_password,
        'created_at': datetime.now(),
        'last_active': datetime.now()
    })

    user_id = str(result.inserted_id)
    session['user_id'] = user_id
    session['user_name'] = name
    session['user_email'] = email

    return jsonify({
        'message': 'Registration successful',
        'user': {'id': user_id, 'name': name, 'email': email}
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Find user
    user = users_collection.find_one({'email': email})

    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Update last active
    users_collection.update_one(
        {'_id': user['_id']},
        {'$set': {'last_active': datetime.now()}}
    )

    user_id = str(user['_id'])
    session['user_id'] = user_id
    session['user_name'] = user['name']
    session['user_email'] = user['email']

    return jsonify({
        'message': 'Login successful',
        'user': {'id': user_id, 'name': user['name'], 'email': user['email']}
    })

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'})

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'name': session['user_name'],
                'email': session['user_email']
            }
        })
    return jsonify({'authenticated': False}), 401

# User Progress Routes

@app.route('/api/users/progress', methods=['GET'])
@login_required
def get_user_progress():
    user_id = session['user_id']

    # Get user's attempts
    attempts = list(attempts_collection.find(
        {'user_id': user_id},
        {'_id': 0}
    ).sort('created_at', -1))

    # Convert dates to strings for JSON serialization
    for attempt in attempts:
        if 'created_at' in attempt:
            attempt['created_at'] = attempt['created_at'].isoformat()
        if 'completed_at' in attempt and attempt['completed_at']:
            attempt['completed_at'] = attempt['completed_at'].isoformat()

    return jsonify({'attempts': attempts})

@app.route('/api/questions/sets', methods=['GET'])
def get_question_sets():
    pipeline = [
        {'$group': {
            '_id': '$question_set',
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]

    sets = list(questions_collection.aggregate(pipeline))
    result = [{'setNumber': s['_id'], 'questionCount': s['count']} for s in sets]

    return jsonify(result)

@app.route('/api/questions/set/<int:set_number>', methods=['GET'])
def get_questions_by_set(set_number):
    questions = list(questions_collection.find(
        {'question_set': set_number}
        # Include correct_answers for instant feedback
    ).sort('_id', 1))

    # Convert ObjectId to string
    for q in questions:
        q['_id'] = str(q['_id'])
        if 'created_at' in q:
            q['created_at'] = q['created_at'].isoformat()

    return jsonify(questions)

@app.route('/api/attempts/start', methods=['POST'])
def start_attempt():
    data = request.get_json()
    user_id = data.get('userId')
    user_name = data.get('userName')
    question_set_number = data.get('questionSetNumber')

    result = attempts_collection.insert_one({
        'user_id': user_id,
        'user_name': user_name,
        'question_set_number': question_set_number,
        'answers': [],
        'score': 0,
        'total_questions': 0,
        'status': 'in_progress',
        'created_at': datetime.now(),
        'started_at': datetime.now()
    })

    return jsonify({
        'id': str(result.inserted_id),
        'userId': user_id,
        'questionSetNumber': question_set_number
    })

@app.route('/api/attempts/<attempt_id>/answer', methods=['POST'])
def submit_answer(attempt_id):
    data = request.get_json()
    question_id = data.get('questionId')
    selected_answers = data.get('selectedAnswers', [])

    # Get correct answers
    question = questions_collection.find_one({'_id': ObjectId(question_id)})

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    correct_answers = question['correct_answers']
    is_correct = sorted(selected_answers) == sorted(correct_answers)

    # Get attempt
    attempt = attempts_collection.find_one({'_id': ObjectId(attempt_id)})

    if not attempt:
        return jsonify({'error': 'Attempt not found'}), 404

    # Check if question already answered
    answers = attempt.get('answers', [])
    existing_index = next((i for i, a in enumerate(answers) if a['question_id'] == question_id), None)

    answer_obj = {
        'question_id': question_id,
        'selected_answers': selected_answers,
        'is_correct': is_correct,
        'answered_at': datetime.now()
    }

    if existing_index is not None:
        answers[existing_index] = answer_obj
    else:
        answers.append(answer_obj)

    # Calculate score
    score = sum(1 for a in answers if a['is_correct'])

    # Update attempt
    attempts_collection.update_one(
        {'_id': ObjectId(attempt_id)},
        {'$set': {
            'answers': answers,
            'score': score,
            'total_questions': len(answers)
        }}
    )

    return jsonify({
        'isCorrect': is_correct,
        'correctAnswers': correct_answers,
        'currentScore': score,
        'totalAnswered': len(answers)
    })

@app.route('/api/attempts/<attempt_id>/complete', methods=['POST'])
def complete_attempt(attempt_id):
    attempts_collection.update_one(
        {'_id': ObjectId(attempt_id)},
        {'$set': {
            'status': 'completed',
            'completed_at': datetime.now()
        }}
    )

    attempt = attempts_collection.find_one({'_id': ObjectId(attempt_id)})

    # Convert for JSON
    attempt['_id'] = str(attempt['_id'])
    if 'created_at' in attempt:
        attempt['created_at'] = attempt['created_at'].isoformat()
    if 'completed_at' in attempt:
        attempt['completed_at'] = attempt['completed_at'].isoformat()

    return jsonify(attempt)

# Admin Routes

@app.route('/api/questions', methods=['GET'])
def get_all_questions():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 50, type=int)
    skip = (page - 1) * limit

    total = questions_collection.count_documents({})
    questions = list(questions_collection.find().sort('question_set', 1).skip(skip).limit(limit))

    # Convert ObjectId to string
    for q in questions:
        q['_id'] = str(q['_id'])
        q['id'] = q['_id']  # Add id field for frontend compatibility
        if 'created_at' in q:
            q['created_at'] = q['created_at'].isoformat()

    return jsonify({
        'questions': questions,
        'currentPage': page,
        'totalPages': (total + limit - 1) // limit,
        'totalQuestions': total
    })

@app.route('/api/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    question = questions_collection.find_one({'_id': ObjectId(question_id)})

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    question['_id'] = str(question['_id'])
    question['id'] = question['_id']
    if 'created_at' in question:
        question['created_at'] = question['created_at'].isoformat()

    return jsonify(question)

@app.route('/api/questions', methods=['POST'])
def create_question():
    data = request.get_json()

    correct_answers = data['correct_answers']
    has_multiple_answers = len(correct_answers) > 1

    result = questions_collection.insert_one({
        'question_text': data['question_text'],
        'options': data['options'],
        'correct_answers': correct_answers,
        'has_multiple_answers': has_multiple_answers,
        'category': data.get('category', 'AWS Data Engineering'),
        'difficulty': data.get('difficulty', 'Medium'),
        'question_set': data['question_set'],
        'created_at': datetime.now()
    })

    return jsonify({'id': str(result.inserted_id), 'message': 'Question created'}), 201

@app.route('/api/questions/<question_id>', methods=['PUT'])
def update_question(question_id):
    data = request.get_json()

    correct_answers = data['correct_answers']
    has_multiple_answers = len(correct_answers) > 1

    questions_collection.update_one(
        {'_id': ObjectId(question_id)},
        {'$set': {
            'question_text': data['question_text'],
            'options': data['options'],
            'correct_answers': correct_answers,
            'has_multiple_answers': has_multiple_answers,
            'category': data.get('category', 'AWS Data Engineering'),
            'difficulty': data.get('difficulty', 'Medium'),
            'question_set': data['question_set'],
            'updated_at': datetime.now()
        }}
    )

    return jsonify({'message': 'Question updated'})

@app.route('/api/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    questions_collection.delete_one({'_id': ObjectId(question_id)})
    return jsonify({'message': 'Question deleted'})

# Coding Practice Routes

@app.route('/api/coding/questions/<language>', methods=['GET'])
def get_coding_questions(language):
    """Get all coding questions for a specific language"""
    questions = list(coding_questions_collection.find(
        {'language': language}
    ).sort('created_at', 1))

    # Convert ObjectId to string
    for q in questions:
        q['_id'] = str(q['_id'])
        if 'created_at' in q:
            q['created_at'] = q['created_at'].isoformat()

    return jsonify(questions)

@app.route('/api/coding/question/<question_id>', methods=['GET'])
def get_coding_question(question_id):
    """Get a specific coding question by ID"""
    question = coding_questions_collection.find_one({'_id': ObjectId(question_id)})

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    question['_id'] = str(question['_id'])
    if 'created_at' in question:
        question['created_at'] = question['created_at'].isoformat()

    return jsonify(question)

@app.route('/api/coding/run', methods=['POST'])
def run_code():
    """Run code without saving (for testing)"""
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'python')

    # Note: This is a placeholder. In production, you would:
    # 1. Use a sandboxed environment (Docker container)
    # 2. Set time limits
    # 3. Restrict system calls
    # 4. Handle different languages appropriately

    try:
        # For now, just return a success message
        # In production, you'd execute the code safely
        return jsonify({
            'success': True,
            'output': 'Code execution is not implemented yet. This is a demo.\nYour code was received and would be executed in a sandboxed environment.',
            'language': language
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/coding/submit', methods=['POST'])
def submit_code():
    """Submit code solution for evaluation"""
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'python')
    question_id = data.get('questionId')

    # Get the question to access test cases
    question = coding_questions_collection.find_one({'_id': ObjectId(question_id)})

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    # Save submission if user is logged in
    if 'user_id' in session:
        coding_submissions_collection.insert_one({
            'user_id': session['user_id'],
            'question_id': question_id,
            'language': language,
            'code': code,
            'submitted_at': datetime.now()
        })

    # Note: This is a placeholder for actual code evaluation
    # In production, you would:
    # 1. Run the code against test cases
    # 2. Compare outputs
    # 3. Measure runtime

    try:
        # Mock evaluation - randomly pass/fail for demo
        import random
        passed = random.randint(2, 3)
        total = 3

        return jsonify({
            'success': passed == total,
            'passed': passed,
            'total': total,
            'runtime': '45 ms',
            'error': None if passed == total else 'Test case 3 failed: Expected output does not match'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'passed': 0,
            'total': 3,
            'error': str(e)
        }), 400

@app.route('/api/coding/submissions', methods=['GET'])
@login_required
def get_user_submissions():
    """Get all submissions for the logged-in user"""
    user_id = session['user_id']

    submissions = list(coding_submissions_collection.find(
        {'user_id': user_id}
    ).sort('submitted_at', -1).limit(50))

    # Convert for JSON
    for sub in submissions:
        sub['_id'] = str(sub['_id'])
        if 'submitted_at' in sub:
            sub['submitted_at'] = sub['submitted_at'].isoformat()

    return jsonify({'submissions': submissions})

# Exam History Routes

@app.route('/api/exam-history', methods=['GET'])
@login_required
def get_exam_history():
    """Get all quiz attempts for the logged-in user"""
    try:
        user_id = session['user_id']

        # Get all attempts (both completed and in_progress)
        attempts = list(attempts_collection.find(
            {'user_id': user_id}
        ).sort('created_at', -1))

        # Convert for JSON
        for attempt in attempts:
            attempt['_id'] = str(attempt['_id'])

            # Convert datetime fields
            if 'created_at' in attempt and attempt['created_at']:
                attempt['created_at'] = attempt['created_at'].isoformat()

            if 'completed_at' in attempt and attempt['completed_at']:
                attempt['completed_at'] = attempt['completed_at'].isoformat()
            else:
                attempt['completed_at'] = None

            if 'started_at' in attempt and attempt['started_at']:
                attempt['started_at'] = attempt['started_at'].isoformat()
            else:
                attempt['started_at'] = None

            # Ensure answers array exists
            if 'answers' not in attempt:
                attempt['answers'] = []

            # Convert answer dates
            for answer in attempt['answers']:
                if 'answered_at' in answer and answer['answered_at']:
                    answer['answered_at'] = answer['answered_at'].isoformat()

            # Ensure required fields exist
            if 'score' not in attempt:
                attempt['score'] = 0
            if 'total_questions' not in attempt:
                attempt['total_questions'] = 0
            if 'status' not in attempt:
                attempt['status'] = 'in_progress'

        return jsonify({'attempts': attempts})

    except Exception as e:
        print(f"Error in get_exam_history: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'attempts': []}), 500

@app.route('/api/exam-history/<attempt_id>', methods=['GET'])
@login_required
def get_attempt_details(attempt_id):
    """Get detailed information about a specific attempt including all questions and answers"""
    user_id = session['user_id']

    # Get the attempt
    attempt = attempts_collection.find_one({
        '_id': ObjectId(attempt_id),
        'user_id': user_id
    })

    if not attempt:
        return jsonify({'error': 'Attempt not found'}), 404

    # Get all questions for this attempt
    question_set = attempt['question_set_number']
    questions = list(questions_collection.find({'question_set': question_set}))

    # Create a map of question_id to question data
    question_map = {str(q['_id']): q for q in questions}

    # Build detailed answers with full question and option data
    detailed_answers = []
    for answer in attempt.get('answers', []):
        question_id = answer['question_id']
        if question_id in question_map:
            question_data = question_map[question_id]
            detailed_answers.append({
                'question_id': question_id,
                'question_text': question_data['question_text'],
                'options': question_data['options'],
                'selected_answers': answer['selected_answers'],
                'correct_answers': question_data['correct_answers'],
                'is_correct': answer['is_correct'],
                'answered_at': answer['answered_at'].isoformat() if 'answered_at' in answer else None
            })

    # Prepare response
    response = {
        '_id': str(attempt['_id']),
        'user_id': attempt['user_id'],
        'user_name': attempt['user_name'],
        'question_set_number': attempt['question_set_number'],
        'score': attempt['score'],
        'total_questions': attempt['total_questions'],
        'status': attempt['status'],
        'created_at': attempt['created_at'].isoformat() if 'created_at' in attempt else None,
        'completed_at': attempt['completed_at'].isoformat() if 'completed_at' in attempt and attempt['completed_at'] else None,
        'detailed_answers': detailed_answers
    }

    return jsonify(response)

if __name__ == '__main__':
    print("Connecting to MongoDB Atlas...")
    print(f"Database: {DB_NAME}")
    print("Collections: questions, users, attempts")
    print("\nStarting Flask server...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, port=5000)
