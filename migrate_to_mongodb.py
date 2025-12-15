from pymongo import MongoClient
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv('uri')
DB_NAME = 'AWS_DE_V2'

def migrate_qna_to_mongodb():
    """Migrate questions from qna.json to MongoDB Atlas"""

    # Read qna.json
    with open('qna.json', 'r', encoding='utf-8') as f:
        questions_data = json.load(f)

    print(f"Found {len(questions_data)} questions in qna.json")

    # Connect to MongoDB
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    questions_collection = db['questions']

    print(f"Connected to database: {DB_NAME}")

    # Clear existing questions
    result = questions_collection.delete_many({})
    print(f"Cleared {result.deleted_count} existing questions")

    # Split questions into sets of 50
    questions_per_set = 50
    imported_count = 0
    questions_to_insert = []

    for i, item in enumerate(questions_data):
        set_number = (i // questions_per_set) + 1

        # Convert single correct_answer to array if needed
        if isinstance(item.get('correct_answer'), list):
            correct_answers = item['correct_answer']
        else:
            correct_answers = [item.get('correct_answer', 'A')]

        # Get category and difficulty if present
        category = item.get('category', 'AWS Data Engineering')
        difficulty = item.get('difficulty', 'Medium')

        # Determine if question has multiple correct answers
        has_multiple_answers = len(correct_answers) > 1

        # Prepare question document
        question_doc = {
            'question_text': item['question_text'],
            'options': item['options'],
            'correct_answers': correct_answers,
            'has_multiple_answers': has_multiple_answers,
            'category': category,
            'difficulty': difficulty,
            'question_set': set_number,
            'created_at': datetime.now()
        }

        questions_to_insert.append(question_doc)
        imported_count += 1

        if imported_count % 100 == 0:
            print(f"Prepared {imported_count} questions...")

    # Insert all questions
    print("Inserting questions into MongoDB...")
    result = questions_collection.insert_many(questions_to_insert)
    print(f"Inserted {len(result.inserted_ids)} questions")

    # Show statistics
    pipeline = [
        {'$group': {
            '_id': '$question_set',
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]

    sets = list(questions_collection.aggregate(pipeline))

    print(f"\nMigration completed successfully!")
    print(f"Total questions imported: {imported_count}")
    print(f"Number of question sets: {len(sets)}")
    print(f"\nQuestion distribution by set:")

    for s in sets:
        print(f"Set {s['_id']}: {s['count']} questions")

    print(f"\nMongoDB Database: {DB_NAME}")
    print(f"Collection: questions")

    client.close()

if __name__ == '__main__':
    migrate_qna_to_mongodb()
