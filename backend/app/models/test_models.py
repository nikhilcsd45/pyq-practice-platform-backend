from pydantic import BaseModel
from typing import List, Dict, Optional

class Option(BaseModel):
    id: str
    text: str

class Question(BaseModel):
    id: str
    text: str
    options: List[Option]
    correct_option_id: str
    explanation: str
    subject: str
    topic: str
    difficulty: str

class QuestionOut(BaseModel):
    id: str
    text: str
    options: List[Option]
    subject: str
    topic: str
    difficulty: str

class Test(BaseModel):
    id: str
    title: str
    description: str
    duration: int  # in minutes
    total_questions: int
    subjects: List[str]
    difficulty: str
    question_ids: List[str]

class TestOut(BaseModel):
    id: str
    title: str
    description: str
    duration: int
    total_questions: int
    subjects: List[str]
    difficulty: str
    questions: List[QuestionOut]

class SubmittedAnswer(BaseModel):
    question_id: str
    selected_option_id: str

class TestSubmission(BaseModel):
    test_id: str
    username: str
    answers: List[SubmittedAnswer]
    
class TestSubmissionResult(BaseModel):
    submission_id: str
    test_id: str
    username: str
    score: float
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    unattempted: int
    time_taken: Optional[int] = None
    weak_topics: List[Dict[str, str]]
