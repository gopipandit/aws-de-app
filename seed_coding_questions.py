from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('uri')
DB_NAME = 'AWS_DE_V2'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coding_questions_collection = db['coding_questions']

# Sample Python Questions
python_questions = [
    {
        "title": "Two Sum",
        "language": "python",
        "difficulty": "Easy",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "examples": [
            {
                "input": "nums = [2,7,11,15], target = 9",
                "output": "[0,1]",
                "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
            },
            {
                "input": "nums = [3,2,4], target = 6",
                "output": "[1,2]",
                "explanation": ""
            }
        ],
        "constraints": "2 <= nums.length <= 10^4, -10^9 <= nums[i] <= 10^9, Only one valid answer exists.",
        "starter_code": "def two_sum(nums, target):\n    \"\"\"\n    :type nums: List[int]\n    :type target: int\n    :rtype: List[int]\n    \"\"\"\n    # Write your code here\n    pass\n\n# Test\nprint(two_sum([2, 7, 11, 15], 9))  # Expected: [0, 1]",
        "test_cases": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "output": [0, 1]},
            {"input": {"nums": [3, 2, 4], "target": 6}, "output": [1, 2]},
            {"input": {"nums": [3, 3], "target": 6}, "output": [0, 1]}
        ],
        "created_at": datetime.now()
    },
    {
        "title": "Reverse String",
        "language": "python",
        "difficulty": "Easy",
        "description": "Write a function that reverses a string. The input string is given as an array of characters s. You must do this by modifying the input array in-place with O(1) extra memory.",
        "examples": [
            {
                "input": "s = ['h','e','l','l','o']",
                "output": "['o','l','l','e','h']",
                "explanation": ""
            },
            {
                "input": "s = ['H','a','n','n','a','h']",
                "output": "['h','a','n','n','a','H']",
                "explanation": ""
            }
        ],
        "constraints": "1 <= s.length <= 10^5, s[i] is a printable ascii character.",
        "starter_code": "def reverse_string(s):\n    \"\"\"\n    :type s: List[str]\n    :rtype: None Do not return anything, modify s in-place instead.\n    \"\"\"\n    # Write your code here\n    pass\n\n# Test\ns = ['h','e','l','l','o']\nreverse_string(s)\nprint(s)  # Expected: ['o','l','l','e','h']",
        "test_cases": [
            {"input": {"s": ['h','e','l','l','o']}, "output": ['o','l','l','e','h']},
            {"input": {"s": ['H','a','n','n','a','h']}, "output": ['h','a','n','n','a','H']}
        ],
        "created_at": datetime.now()
    },
    {
        "title": "Valid Palindrome",
        "language": "python",
        "difficulty": "Easy",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string s, return true if it is a palindrome, or false otherwise.",
        "examples": [
            {
                "input": "s = 'A man, a plan, a canal: Panama'",
                "output": "true",
                "explanation": "'amanaplanacanalpanama' is a palindrome."
            },
            {
                "input": "s = 'race a car'",
                "output": "false",
                "explanation": "'raceacar' is not a palindrome."
            }
        ],
        "constraints": "1 <= s.length <= 2 * 10^5, s consists only of printable ASCII characters.",
        "starter_code": "def is_palindrome(s):\n    \"\"\"\n    :type s: str\n    :rtype: bool\n    \"\"\"\n    # Write your code here\n    pass\n\n# Test\nprint(is_palindrome('A man, a plan, a canal: Panama'))  # Expected: True",
        "test_cases": [
            {"input": {"s": "A man, a plan, a canal: Panama"}, "output": True},
            {"input": {"s": "race a car"}, "output": False},
            {"input": {"s": " "}, "output": True}
        ],
        "created_at": datetime.now()
    }
]

# Sample PySpark Questions
pyspark_questions = [
    {
        "title": "DataFrame Basic Operations",
        "language": "pyspark",
        "difficulty": "Easy",
        "description": "Given a DataFrame with columns 'name', 'age', and 'salary', write code to filter employees with age greater than 30 and select only the 'name' and 'salary' columns. Then, order the result by salary in descending order.",
        "examples": [
            {
                "input": "DataFrame with columns: name, age, salary",
                "output": "Filtered and sorted DataFrame with name and salary columns",
                "explanation": "Filter by age > 30, select name and salary, order by salary descending"
            }
        ],
        "constraints": "Use PySpark DataFrame API",
        "starter_code": "from pyspark.sql import SparkSession\nfrom pyspark.sql.functions import *\n\nspark = SparkSession.builder.appName('solution').getOrCreate()\n\n# Sample data\ndata = [\n    ('John', 28, 50000),\n    ('Sarah', 35, 75000),\n    ('Mike', 42, 90000),\n    ('Emma', 31, 65000)\n]\ndf = spark.createDataFrame(data, ['name', 'age', 'salary'])\n\n# Write your solution here\nresult = df  # Replace with your solution\n\nresult.show()",
        "test_cases": [],
        "created_at": datetime.now()
    },
    {
        "title": "Data Aggregation",
        "language": "pyspark",
        "difficulty": "Medium",
        "description": "Given a DataFrame with sales data (columns: 'product', 'category', 'amount'), write code to calculate the total sales amount for each category and find the category with the highest total sales.",
        "examples": [
            {
                "input": "Sales DataFrame with product, category, amount columns",
                "output": "Aggregated data showing total sales per category",
                "explanation": "Group by category and sum the amount"
            }
        ],
        "constraints": "Use PySpark aggregation functions",
        "starter_code": "from pyspark.sql import SparkSession\nfrom pyspark.sql.functions import *\n\nspark = SparkSession.builder.appName('solution').getOrCreate()\n\n# Sample data\ndata = [\n    ('Laptop', 'Electronics', 1200),\n    ('Phone', 'Electronics', 800),\n    ('Shirt', 'Clothing', 50),\n    ('Pants', 'Clothing', 70),\n    ('TV', 'Electronics', 1500)\n]\ndf = spark.createDataFrame(data, ['product', 'category', 'amount'])\n\n# Write your solution here\nresult = df  # Replace with your solution\n\nresult.show()",
        "test_cases": [],
        "created_at": datetime.now()
    },
    {
        "title": "Join Operations",
        "language": "pyspark",
        "difficulty": "Medium",
        "description": "Given two DataFrames - employees (id, name, dept_id) and departments (dept_id, dept_name) - write code to join them and display employee names along with their department names.",
        "examples": [
            {
                "input": "Two DataFrames: employees and departments",
                "output": "Joined DataFrame with employee names and department names",
                "explanation": "Perform inner join on dept_id"
            }
        ],
        "constraints": "Use PySpark join operations",
        "starter_code": "from pyspark.sql import SparkSession\n\nspark = SparkSession.builder.appName('solution').getOrCreate()\n\n# Sample data\nemployees_data = [(1, 'John', 101), (2, 'Sarah', 102), (3, 'Mike', 101)]\nemployees = spark.createDataFrame(employees_data, ['id', 'name', 'dept_id'])\n\ndepartments_data = [(101, 'Engineering'), (102, 'Marketing'), (103, 'Sales')]\ndepartments = spark.createDataFrame(departments_data, ['dept_id', 'dept_name'])\n\n# Write your solution here\nresult = employees  # Replace with your solution\n\nresult.show()",
        "test_cases": [],
        "created_at": datetime.now()
    }
]

# Sample SQL Questions
sql_questions = [
    {
        "title": "Select Employees with High Salary",
        "language": "sql",
        "difficulty": "Easy",
        "description": "Write a SQL query to select all employees who have a salary greater than 70000 from the 'employees' table. Order the results by salary in descending order.",
        "examples": [
            {
                "input": "employees table: (id, name, salary, department)",
                "output": "All columns for employees with salary > 70000, ordered by salary DESC",
                "explanation": ""
            }
        ],
        "constraints": "Use standard SQL syntax",
        "starter_code": "-- Write your SQL query here\nSELECT * FROM employees\nWHERE -- Complete this query\n;",
        "test_cases": [],
        "created_at": datetime.now()
    },
    {
        "title": "Department-wise Employee Count",
        "language": "sql",
        "difficulty": "Medium",
        "description": "Write a SQL query to find the number of employees in each department. Display the department name and the count of employees. Only include departments with more than 2 employees.",
        "examples": [
            {
                "input": "employees table with department column",
                "output": "department, employee_count (where count > 2)",
                "explanation": "Group by department and count employees"
            }
        ],
        "constraints": "Use GROUP BY and HAVING clauses",
        "starter_code": "-- Write your SQL query here\nSELECT department, COUNT(*) as employee_count\nFROM employees\n-- Complete this query\n;",
        "test_cases": [],
        "created_at": datetime.now()
    },
    {
        "title": "Find Second Highest Salary",
        "language": "sql",
        "difficulty": "Medium",
        "description": "Write a SQL query to find the second highest salary from the employees table. If there is no second highest salary, return NULL.",
        "examples": [
            {
                "input": "employees table with salary column",
                "output": "The second highest salary value",
                "explanation": "Use subquery or LIMIT/OFFSET"
            }
        ],
        "constraints": "Handle edge cases where there might not be a second highest salary",
        "starter_code": "-- Write your SQL query here\nSELECT \n-- Complete this query\nFROM employees\n;",
        "test_cases": [],
        "created_at": datetime.now()
    },
    {
        "title": "Join Tables and Aggregate",
        "language": "sql",
        "difficulty": "Hard",
        "description": "Given two tables - orders (order_id, customer_id, amount, order_date) and customers (customer_id, name, city) - write a query to find the total order amount for each customer in each city. Display customer name, city, and total amount ordered by total amount in descending order.",
        "examples": [
            {
                "input": "orders and customers tables",
                "output": "customer_name, city, total_amount (ordered by total DESC)",
                "explanation": "JOIN tables and GROUP BY customer and city"
            }
        ],
        "constraints": "Use JOIN and GROUP BY",
        "starter_code": "-- Write your SQL query here\nSELECT \n    c.name,\n    c.city,\n    -- Complete this query\nFROM customers c\n-- Complete the JOIN and aggregation\n;",
        "test_cases": [],
        "created_at": datetime.now()
    }
]

def seed_database():
    print("Starting to seed coding questions...")

    # Clear existing data
    coding_questions_collection.delete_many({})
    print("Cleared existing coding questions")

    # Insert Python questions
    if python_questions:
        result = coding_questions_collection.insert_many(python_questions)
        print(f"Inserted {len(result.inserted_ids)} Python questions")

    # Insert PySpark questions
    if pyspark_questions:
        result = coding_questions_collection.insert_many(pyspark_questions)
        print(f"Inserted {len(result.inserted_ids)} PySpark questions")

    # Insert SQL questions
    if sql_questions:
        result = coding_questions_collection.insert_many(sql_questions)
        print(f"Inserted {len(result.inserted_ids)} SQL questions")

    # Summary
    total_count = coding_questions_collection.count_documents({})
    print(f"\n✓ Total questions in database: {total_count}")

    # Count by language
    for lang in ['python', 'pyspark', 'sql']:
        count = coding_questions_collection.count_documents({"language": lang})
        print(f"  - {lang.upper()}: {count} questions")

if __name__ == "__main__":
    try:
        seed_database()
        print("\n✓ Database seeding completed successfully!")
    except Exception as e:
        print(f"\n✗ Error seeding database: {e}")
    finally:
        client.close()
