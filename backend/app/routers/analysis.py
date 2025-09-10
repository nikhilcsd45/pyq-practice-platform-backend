from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any

from app.models.user_models import UserInDB
from app.services.auth_service import get_current_user
from app.services.data_service import get_submission_by_id
from app.services.gemini_service import get_ai_analysis

router = APIRouter()

@router.get("/analysis/{submission_id}", response_model=Dict[str, Any])
async def get_analysis(submission_id: str, current_user: UserInDB = Depends(get_current_user)):
    """Get AI-powered analysis for a test submission."""
    # Get submission details
    submission = get_submission_by_id(submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Verify user owns this submission
    if submission["username"] != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this submission"
        )
    
    # Get AI analysis
    analysis = await get_ai_analysis(submission["weak_topics"])
    
    # Combine submission data with analysis
    result = {
        "submission_id": submission_id,
        "score": submission["score"],
        "total_questions": submission["total_questions"],
        "correct_answers": submission["correct_answers"],
        "incorrect_answers": submission["incorrect_answers"],
        "unattempted": submission["unattempted"],
        "weak_topics": submission["weak_topics"],
        "study_plan": analysis["study_plan"]
    }
    
    return result
