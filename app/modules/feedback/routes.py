from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.models.feedback import Feedback
from app.modules.feedback import service
from app.modules.feedback.schemas import CategoryCount, FeedbackCreate, FeedbackResponse # Importa tu modelo

router = APIRouter()

@router.post("/", response_model=FeedbackResponse)
def create_feedback(data: FeedbackCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return service.create_feedback(db=db, data=data, user_id=current_user["user_id"])

@router.get("/", response_model=list[FeedbackResponse])
def get_all_feedbacks(db: Session = Depends(get_db)):
    return service.get_all_feedbacks(db=db)

@router.get("/counts", response_model=list[CategoryCount])
def get_counts(db: Session = Depends(get_db)):
    return service.get_feedback_counts_by_category(db)