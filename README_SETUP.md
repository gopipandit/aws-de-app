# AWS Data Engineering Quiz App - Python/Flask Version

A simple, personal-use quiz application built with Python Flask and SQLite.

## Features

- **SQLite Database** - No external database needed
- **User Tracking** - Enter your name and track your progress
- **Question Sets** - Questions divided into sets of 50
- **Multiple Correct Answers** - Supports questions with single or multiple correct answers
- **Progress Tracking** - View your previous attempts and scores
- **Admin Panel** - Add, edit, and delete questions easily
- **No Node.js Required** - Simple Python-based solution

## Setup Instructions

### 1. Install Python

Make sure you have Python 3.7 or higher installed. You already have Python 3.11.5.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install Flask (the only dependency needed).

### 3. Migrate Data

Import your questions from qna.json to the SQLite database:

```bash
python migrate_data.py
```

This will:
- Create a SQLite database file `quiz_app.db`
- Import all questions from qna.json
- Split questions into sets of 50
- Show statistics about the import

### 4. Run the Application

```bash
python app.py
```

The application will start on http://localhost:5000

### 5. Access the Application

- **Main Quiz**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin

## How to Use

### For Quiz Taking:

1. Go to http://localhost:5000
2. Enter your name
3. Select a question set (50 questions each)
4. Answer questions one by one
5. Get instant feedback (green = correct, red = incorrect)
6. View your score and finish the quiz
7. Your progress is saved automatically

### For Managing Questions (Admin):

1. Go to http://localhost:5000/admin
2. View all questions with pagination
3. Click "New Question" to add a question
4. Fill in question text, options (A, B, C, D, etc.)
5. Check the boxes for correct answers (can be multiple)
6. Set category, difficulty, and question set number
7. Save the question
8. Edit or delete existing questions as needed

## File Structure

```
aws-de-app/
├── app.py                  # Main Flask application
├── migrate_data.py         # Script to import qna.json to database
├── requirements.txt        # Python dependencies
├── quiz_app.db            # SQLite database (created after migration)
├── qna.json               # Original questions file
├── templates/
│   ├── landing.html       # Landing page with user login
│   ├── quiz.html          # Quiz interface
│   └── admin.html         # Admin panel
└── static/
    ├── styles.css         # Shared CSS styles
    ├── landing.js         # Landing page JavaScript
    ├── quiz-app.js        # Quiz logic
    └── admin.js           # Admin panel logic
```

## Database Schema

The SQLite database contains 4 tables:

1. **questions**
   - id, question_text, options (JSON), correct_answers (JSON)
   - category, difficulty, question_set
   - created_at

2. **users**
   - id, name, created_at, last_active

3. **attempts**
   - id, user_id, user_name, question_set_number
   - score, total_questions, status
   - started_at, completed_at

4. **answers**
   - id, attempt_id, question_id
   - selected_answers (JSON), is_correct
   - answered_at

## API Endpoints

### User Endpoints
- `POST /api/users/login` - Login or create user

### Question Endpoints
- `GET /api/questions/sets` - Get all question sets
- `GET /api/questions/set/<set_number>` - Get questions for a specific set
- `GET /api/questions` - Get all questions (admin, with pagination)
- `GET /api/questions/<id>` - Get single question (admin)
- `POST /api/questions` - Create new question (admin)
- `PUT /api/questions/<id>` - Update question (admin)
- `DELETE /api/questions/<id>` - Delete question (admin)

### Attempt Endpoints
- `POST /api/attempts/start` - Start a new attempt
- `POST /api/attempts/<id>/answer` - Submit an answer
- `POST /api/attempts/<id>/complete` - Complete an attempt

## Stopping the Server

To stop the Flask server, press `Ctrl+C` in the terminal where it's running.

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, you can change it in `app.py`:
```python
app.run(debug=True, port=5001)  # Change to any available port
```

### Database Issues

If you need to reset the database:
1. Delete `quiz_app.db`
2. Run `python migrate_data.py` again

### Import Errors

If you get import errors, make sure Flask is installed:
```bash
pip install Flask
```

## Notes

- This is designed for personal use - no authentication is implemented
- The database file `quiz_app.db` stores all your data locally
- You can backup your data by copying the `quiz_app.db` file
- The admin panel is open to anyone - suitable for personal/trusted use only

## Advantages of This Solution

- ✅ No Node.js or npm needed
- ✅ No external database server (uses SQLite)
- ✅ Simple Python installation
- ✅ All data stored locally
- ✅ Easy to backup (just copy the .db file)
- ✅ Perfect for personal use
- ✅ Fast and lightweight
