import sqlite3
import json

DATABASE = 'quiz_app.db'

def migrate_qna_to_db():
    """Migrate questions from qna.json to SQLite database"""

    # Read qna.json
    with open('qna.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)

    print(f"Found {len(questions_data)} questions in qna.json")

    # Connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_answers TEXT NOT NULL,
            category TEXT DEFAULT 'AWS Data Engineering',
            difficulty TEXT DEFAULT 'Medium',
            question_set INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            question_set_number INTEGER NOT NULL,
            score INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0,
            status TEXT DEFAULT 'in_progress',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            selected_answers TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (attempt_id) REFERENCES attempts (id),
            FOREIGN KEY (question_id) REFERENCES questions (id)
        )
    ''')

    print("Database tables created/verified")

    # Clear existing questions
    cursor.execute('DELETE FROM questions')
    print("Cleared existing questions")

    # Split questions into sets of 50
    questions_per_set = 50
    imported_count = 0

    for i, item in enumerate(questions_data):
        set_number = (i // questions_per_set) + 1

        # Convert options to JSON string
        options_json = json.dumps(item['options'])

        # Convert single correct_answer to array if needed
        if isinstance(item['correct_answer'], list):
            correct_answers = item['correct_answer']
        else:
            correct_answers = [item['correct_answer']]

        correct_answers_json = json.dumps(correct_answers)

        # Get category and difficulty if present
        category = item.get('category', 'AWS Data Engineering')
        difficulty = item.get('difficulty', 'Medium')

        # Insert question
        cursor.execute('''
            INSERT INTO questions
            (question_text, options, correct_answers, category, difficulty, question_set)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (item['question_text'], options_json, correct_answers_json,
              category, difficulty, set_number))

        imported_count += 1

        if imported_count % 100 == 0:
            print(f"Imported {imported_count} questions...")

    conn.commit()

    # Show statistics
    cursor.execute('''
        SELECT question_set, COUNT(*) as count
        FROM questions
        GROUP BY question_set
        ORDER BY question_set
    ''')

    sets = cursor.fetchall()

    print(f"\nMigration completed successfully!")
    print(f"Total questions imported: {imported_count}")
    print(f"Number of question sets: {len(sets)}")
    print(f"\nQuestion distribution by set:")

    for set_num, count in sets:
        print(f"Set {set_num}: {count} questions")

    conn.close()

if __name__ == '__main__':
    migrate_qna_to_db()
