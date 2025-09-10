import json
import os
from typing import List, Dict, Any, Union

# Define paths to JSON files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")
TESTS_FILE = os.path.join(DATA_DIR, "tests.json")
SUBMISSIONS_FILE = os.path.join(DATA_DIR, "submissions.json")

# Helper functions to ensure files exist with valid JSON
def ensure_file_exists(file_path: str, default_data: Union[List, Dict] = None):
    """Ensure that a JSON file exists and contains valid JSON."""
    if default_data is None:
        default_data = []
        
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default_data, f)
    else:
        # Check if the file contains valid JSON
        try:
            with open(file_path, 'r') as f:
                json.load(f)
        except json.JSONDecodeError:
            # If not valid, overwrite with default data
            with open(file_path, 'w') as f:
                json.dump(default_data, f)

# Ensure all data files exist with valid JSON
for file_path in [USERS_FILE, QUESTIONS_FILE, TESTS_FILE, SUBMISSIONS_FILE]:
    ensure_file_exists(file_path)

# Generic read function
def read_data(file_path: str) -> List[Dict]:
    """Read data from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

# Generic write function
def write_data(file_path: str, data: List[Dict]):
    """Write data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# User specific functions
def get_users() -> List[Dict]:
    """Get all users."""
    return read_data(USERS_FILE)

def get_user_by_username(username: str) -> Dict:
    """Get a user by username."""
    users = get_users()
    for user in users:
        if user["username"] == username:
            return user
    return None

def add_user(user_data: Dict):
    """Add a new user."""
    users = get_users()
    users.append(user_data)
    write_data(USERS_FILE, users)

# Question specific functions
def get_questions() -> List[Dict]:
    """Get all questions."""
    return read_data(QUESTIONS_FILE)

def get_question_by_id(question_id: str) -> Dict:
    """Get a question by ID."""
    questions = get_questions()
    for question in questions:
        if question["id"] == question_id:
            return question
    return None

def get_questions_by_ids(question_ids: List[str]) -> List[Dict]:
    """Get questions by IDs."""
    questions = get_questions()
    return [question for question in questions if question["id"] in question_ids]

# Test specific functions
def get_tests() -> List[Dict]:
    """Get all tests."""
    return read_data(TESTS_FILE)

def get_test_by_id(test_id: str) -> Dict:
    """Get a test by ID."""
    tests = get_tests()
    for test in tests:
        if test["id"] == test_id:
            return test
    return None

# Submission specific functions
def get_submissions() -> List[Dict]:
    """Get all submissions."""
    return read_data(SUBMISSIONS_FILE)

def add_submission(submission_data: Dict):
    """Add a new submission."""
    submissions = get_submissions()
    submissions.append(submission_data)
    write_data(SUBMISSIONS_FILE, submissions)

def get_submission_by_id(submission_id: str) -> Dict:
    """Get a submission by ID."""
    submissions = get_submissions()
    for submission in submissions:
        if submission["id"] == submission_id:
            return submission
    return None

def get_submissions_by_username(username: str) -> List[Dict]:
    """Get all submissions for a user."""
    submissions = get_submissions()
    return [submission for submission in submissions if submission["username"] == username]
