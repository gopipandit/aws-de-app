# DataEngineerPrep

**DataEngineerPrep.com** - A focused learning platform built for data engineers and data analysts who want to prepare seriously for certification exams and technical interviews.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![MongoDB](https://img.shields.io/badge/mongodb-atlas-brightgreen.svg)

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🎯 About

Most platforms either focus only on theory or provide generic coding problems that do not reflect real data engineering work. **DataEngineerPrep bridges that gap** by combining certification-oriented preparation with hands-on practice in core data engineering skills.

### Key Benefits:
- **Focused Learning**: Curated questions specifically for data engineering certifications
- **Real-World Practice**: Problems reflecting actual data engineering challenges
- **Progress Tracking**: Monitor performance and identify improvement areas
- **Organized Content**: Multiple question sets covering various AWS topics

## ✨ Features

### 🔐 Authentication System
- User registration with email and password
- Secure login with bcrypt password hashing
- Session-based authentication
- Protected routes with login requirements

### 📝 Quiz Interface
- **Full-width modern layout** with sidebar navigation
- **Real-time timer** tracking quiz duration
- **Question list sidebar** showing all questions with status indicators
- **Multiple choice questions** with single or multiple correct answers
- **Instant feedback** after each answer
- **Progress tracking** with score display
- **Question navigation**:
  - Click any question in sidebar to jump to it
  - Use Previous/Next buttons
  - Visual indicators for answered/unanswered questions

### 📊 Progress Tracking
- View all previous quiz attempts
- Track scores and completion status
- Best score statistics
- Question set completion tracking

### 👨‍💼 Admin Panel
- Add new questions with multiple options
- Edit existing questions
- Delete questions
- Support for single and multiple correct answers
- Question categorization by difficulty and sets
- Pagination for large question sets

### 🎨 User Interface
- Clean, modern design
- Responsive layout
- Color-coded status indicators:
  - Green: Correct answers
  - Red: Incorrect answers
  - Purple: Currently active question
  - Gray: Unanswered questions
- Smooth animations and transitions

## 🛠 Tech Stack

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **pymongo 4.6.3** - MongoDB driver
- **bcrypt 3.2.0** - Password hashing
- **python-dotenv 0.21.0** - Environment variable management

### Frontend
- **HTML5**
- **CSS3** (Custom styling, no frameworks)
- **Vanilla JavaScript** (No jQuery or frameworks)

### Database
- **MongoDB Atlas** - Cloud-hosted NoSQL database
- Collections: `questions`, `users`, `attempts`

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- MongoDB Atlas account (free tier available)
- Git (optional, for cloning)

## 🚀 Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd aws-de-app
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
```
Flask==3.0.0
pymongo==4.6.3
python-dotenv==0.21.0
bcrypt==3.2.0
```

## ⚙️ Configuration

### 1. Create Environment File

Create a `.env` file in the project root:

```bash
# .env
uri = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
```

Replace `<username>`, `<password>`, and `<cluster>` with your MongoDB Atlas credentials.

### 2. MongoDB Atlas Setup

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Create a database user with read/write permissions
4. Whitelist your IP address (or use 0.0.0.0/0 for testing)
5. Get your connection string and add it to `.env`

### 3. Database Name

The application uses database: `AWS_DE_V2`

Collections will be created automatically:
- `questions` - Quiz questions
- `users` - Registered users
- `attempts` - Quiz attempts and scores

## 🏃 Running the Application

### 1. Migrate Questions to MongoDB (First Time Only)

If you have existing questions in `qna.json`:

```bash
python migrate_to_mongodb.py
```

This will:
- Import all questions from `qna.json`
- Split them into sets of 50
- Add metadata like difficulty and category
- Set the `has_multiple_answers` flag

### 2. Start the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

You should see:
```
Connecting to MongoDB Atlas...
Database: AWS_DE_V2
Collections: questions, users, attempts

Starting Flask server...
Access the application at: http://localhost:5000
```

### 3. Access the Application

Open your browser and navigate to:
- **Main App**: http://localhost:5000/
- **Admin Panel**: http://localhost:5000/admin (requires login)
- **About Page**: http://localhost:5000/about

## 📁 Project Structure

```
aws-de-app/
│
├── app.py                      # Main Flask application
├── migrate_to_mongodb.py       # Migration script for questions
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── qna.json                    # Source questions data
│
├── templates/                  # HTML templates
│   ├── auth.html              # Login/Registration page
│   ├── landing.html           # Question sets dashboard
│   ├── quiz.html              # Quiz interface
│   ├── admin.html             # Admin panel
│   └── about.html             # About page
│
├── static/                     # Static files
│   ├── styles.css             # Global styles
│   ├── landing.js             # Landing page logic
│   ├── quiz-app.js            # Quiz functionality & timer
│   └── admin.js               # Admin panel logic
│
└── documentation/              # Documentation files
    ├── README.md              # This file
    ├── AUTHENTICATION.md      # Auth system details
    ├── BRANDING_UPDATE.md     # Branding changes
    ├── QUIZ_IMPROVEMENTS.md   # Quiz UI improvements
    └── ADMIN_PANEL_FIX.md     # Admin panel fixes
```

## 📖 Usage Guide

### For Students/Users

#### 1. Registration
1. Visit http://localhost:5000/
2. Click the "Register" tab
3. Enter your name, email, and password (minimum 6 characters)
4. Click "Create Account"

#### 2. Login
1. Enter your email and password
2. Click "Login"
3. You'll be redirected to the question sets dashboard

#### 3. Taking a Quiz
1. From the dashboard, click on any question set
2. The quiz interface will load with:
   - Timer in the top-left sidebar
   - Question list in the left sidebar
   - Current question in the main area
3. Select your answer(s):
   - Single-choice: Click an option (auto-submits)
   - Multiple-choice: Check all correct boxes, then click "Submit Answer"
4. Navigate using:
   - Click questions in sidebar
   - Use Previous/Next buttons
5. Click "Finish Quiz" when done

#### 4. Viewing Progress
- Your dashboard shows:
  - Total attempts
  - Best score percentage
  - Completed question sets (green checkmarks)

### For Administrators

#### 1. Accessing Admin Panel
1. Login with your account
2. Click "Admin Panel" from the dashboard
3. Or navigate directly to http://localhost:5000/admin

#### 2. Adding Questions
1. Click "+ New Question" button
2. Fill in:
   - Question text
   - Options (A, B, C, D, etc.)
   - Check correct answer(s)
   - Category (default: AWS Data Engineering)
   - Difficulty (Easy/Medium/Hard)
   - Question Set number
3. Click "Save Question"

#### 3. Editing Questions
1. Find the question in the list
2. Click "Edit" button
3. Modify fields as needed
4. Click "Save Question"

#### 4. Deleting Questions
1. Click "Delete" button next to the question
2. Confirm deletion
3. Question is permanently removed

## 🔌 API Documentation

### Authentication Endpoints

#### POST /api/auth/register
Register a new user
```json
Request:
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "mypassword"
}

Response (201):
{
  "message": "Registration successful",
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

#### POST /api/auth/login
Login existing user
```json
Request:
{
  "email": "john@example.com",
  "password": "mypassword"
}

Response (200):
{
  "message": "Login successful",
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

#### POST /api/auth/logout
Logout current user
```json
Response (200):
{
  "message": "Logout successful"
}
```

#### GET /api/auth/check
Check authentication status
```json
Response (200):
{
  "authenticated": true,
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Quiz Endpoints

#### GET /api/questions/sets
Get all available question sets
```json
Response (200):
[
  {
    "setNumber": 1,
    "questionCount": 50
  },
  {
    "setNumber": 2,
    "questionCount": 50
  }
]
```

#### GET /api/questions/set/:set_number
Get questions for a specific set
```json
Response (200):
[
  {
    "_id": "question_id",
    "question_text": "What is Amazon S3?",
    "options": {
      "A": "Storage service",
      "B": "Compute service",
      "C": "Database service",
      "D": "Network service"
    },
    "has_multiple_answers": false,
    "category": "AWS Data Engineering",
    "difficulty": "Easy",
    "question_set": 1
  }
]
```

#### POST /api/attempts/start
Start a new quiz attempt
```json
Request:
{
  "userId": "user_id",
  "userName": "John Doe",
  "questionSetNumber": 1
}

Response (200):
{
  "id": "attempt_id",
  "userId": "user_id",
  "questionSetNumber": 1
}
```

#### POST /api/attempts/:attempt_id/answer
Submit an answer
```json
Request:
{
  "questionId": "question_id",
  "selectedAnswers": ["A"]
}

Response (200):
{
  "isCorrect": true,
  "correctAnswers": ["A"],
  "currentScore": 5,
  "totalAnswered": 10
}
```

#### POST /api/attempts/:attempt_id/complete
Complete quiz attempt
```json
Response (200):
{
  "id": "attempt_id",
  "score": 45,
  "total_questions": 50,
  "status": "completed",
  "completed_at": "2025-12-15T10:30:00"
}
```

### Admin Endpoints

#### GET /api/questions?page=1&limit=50
Get paginated questions
```json
Response (200):
{
  "questions": [...],
  "currentPage": 1,
  "totalPages": 7,
  "totalQuestions": 329
}
```

#### GET /api/questions/:question_id
Get single question details

#### POST /api/questions
Create new question

#### PUT /api/questions/:question_id
Update existing question

#### DELETE /api/questions/:question_id
Delete question

## 💾 Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  email: "user@example.com",      // Unique, lowercase
  name: "User Name",
  password: "bcrypt_hash",          // Bcrypt hashed
  created_at: ISODate,
  last_active: ISODate
}
```

### Questions Collection
```javascript
{
  _id: ObjectId,
  question_text: "Question content...",
  options: {
    "A": "Option A text",
    "B": "Option B text",
    "C": "Option C text",
    "D": "Option D text"
  },
  correct_answers: ["A", "C"],     // Array of correct option keys
  has_multiple_answers: true,       // Boolean flag
  category: "AWS Data Engineering",
  difficulty: "Medium",             // Easy|Medium|Hard
  question_set: 1,                  // Set number
  created_at: ISODate
}
```

### Attempts Collection
```javascript
{
  _id: ObjectId,
  user_id: "user_id",
  user_name: "User Name",
  question_set_number: 1,
  answers: [
    {
      question_id: "question_id",
      selected_answers: ["A"],
      is_correct: true,
      answered_at: ISODate
    }
  ],
  score: 45,                        // Correct answers count
  total_questions: 50,
  status: "completed",              // in_progress|completed
  started_at: ISODate,
  completed_at: ISODate
}
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Test thoroughly before submitting PR
- Update documentation as needed

## 🐛 Troubleshooting

### Common Issues

#### 1. MongoDB Connection Error
**Error**: `ServerSelectionTimeoutError`
**Solution**:
- Check your MongoDB URI in `.env`
- Verify your IP is whitelisted in MongoDB Atlas
- Ensure internet connection is stable

#### 2. Port Already in Use
**Error**: `Address already in use`
**Solution**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

#### 3. Module Not Found
**Error**: `ModuleNotFoundError: No module named 'flask'`
**Solution**:
```bash
pip install -r requirements.txt
```

#### 4. Session Not Persisting
**Solution**:
- Check Flask `secret_key` is set in `app.py`
- Clear browser cookies
- Try incognito/private browsing mode

#### 5. Questions Not Loading
**Solution**:
- Run migration script: `python migrate_to_mongodb.py`
- Check MongoDB database has `questions` collection
- Verify data in MongoDB Atlas console

### Debug Mode
The application runs in debug mode by default. Check terminal for detailed error messages.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Flask and MongoDB
- Inspired by the need for focused data engineering preparation
- Community feedback and contributions

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation in `/documentation`
- Review troubleshooting section above

## 🔄 Version History

### v1.0.0 (Current)
- User authentication with registration and login
- Quiz interface with timer and sidebar navigation
- Progress tracking and statistics
- Admin panel for question management
- Multiple question sets (329 questions across 7 sets)
- Support for single and multiple correct answers
- Full-width responsive layout
- Real-time score tracking

---

**DataEngineerPrep** - Serious preparation for serious data engineers.

Visit: http://localhost:5000/
