from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any
import uuid
from datetime import datetime

from app.models.test_models import (
    Test, TestOut, QuestionOut, TestSubmission, TestSubmissionResult, SubmittedAnswer
)
from app.models.user_models import UserInDB
from app.services.auth_service import get_current_user
from app.services.data_service import (
    get_tests, get_test_by_id, get_questions_by_ids,
    get_question_by_id, add_submission
)

router = APIRouter()

@router.get("/tests", response_model=List[Dict[str, Any]])
async def get_all_tests(current_user: UserInDB = Depends(get_current_user)):
    """Get all available tests."""
    tests = get_tests()
    # Remove question_ids from response
    for test in tests:
        if "question_ids" in test:
            del test["question_ids"]
    return tests

@router.get("/tests/{test_id}", response_model=TestOut)
async def get_test_details(test_id: str, current_user: UserInDB = Depends(get_current_user)):
    """Get test details with questions."""
    test = get_test_by_id(test_id)
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    # Get questions for the test
    questions = get_questions_by_ids(test["question_ids"])
    
    # Remove correct answers from questions
    questions_out = []
    for question in questions:
        question_out = {
            "id": question["id"],
            "text": question["text"],
            "options": question["options"],
            "subject": question["subject"],
            "topic": question["topic"],
            "difficulty": question["difficulty"]
        }
        questions_out.append(question_out)
    
    return {
        "id": test["id"],
        "title": test["title"],
        "description": test["description"],
        "duration": test["duration"],
        "total_questions": test["total_questions"],
        "subjects": test["subjects"],
        "difficulty": test["difficulty"],
        "questions": questions_out
    }

@router.post("/tests/{test_id}/submit", response_model=TestSubmissionResult)
async def submit_test(
    test_id: str, 
    submission: TestSubmission,
    current_user: UserInDB = Depends(get_current_user)
):
    """Submit test answers."""
    # Verify test exists
    test = get_test_by_id(test_id)
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    # Verify user matches
    if submission.username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username in submission does not match authenticated user"
        )
    
    # Evaluate submission
    correct_answers = 0
    incorrect_answers = 0
    weak_topics = []
    attempted_questions = [ans.question_id for ans in submission.answers]
    
    for answer in submission.answers:
        question = get_question_by_id(answer.question_id)
        if not question:
            continue
        
        if answer.selected_option_id == question["correct_option_id"]:
            correct_answers += 1
        else:
            incorrect_answers += 1
            # Add to weak topics
            weak_topic = {
                "subject": question["subject"],
                "topic": question["topic"]
            }
            if weak_topic not in weak_topics:
                weak_topics.append(weak_topic)
    
    # Calculate unattempted questions
    unattempted = test["total_questions"] - len(attempted_questions)
    
    # Calculate score (as percentage)
    score = (correct_answers / test["total_questions"]) * 100 if test["total_questions"] > 0 else 0
    
    # Create submission record
    submission_id = str(uuid.uuid4())
    submission_data = {
        "id": submission_id,
        "test_id": test_id,
        "username": current_user.username,
        "answers": [{"question_id": ans.question_id, "selected_option_id": ans.selected_option_id} for ans in submission.answers],
        "score": score,
        "total_questions": test["total_questions"],
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "unattempted": unattempted,
        "weak_topics": weak_topics,
        "timestamp": datetime.now().isoformat()
    }
    
    add_submission(submission_data)
    
    return {
        "submission_id": submission_id,
        "test_id": test_id,
        "username": current_user.username,
        "score": score,
        "total_questions": test["total_questions"],
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "unattempted": unattempted,
        "weak_topics": weak_topics
    }
