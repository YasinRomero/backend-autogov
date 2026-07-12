from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.modules.feedback.schemas import FeedbackCreate

def create_feedback(db: Session, data: FeedbackCreate, user_id: int):
    nuevo_feedback = Feedback(**data.model_dump(), user_id=user_id)
    db.add(nuevo_feedback)
    db.commit()
    db.refresh(nuevo_feedback)

    return nuevo_feedback

def get_all_feedbacks(db: Session):
    return db.query(Feedback).all()

def get_feedback_counts_by_category(db: Session):
    return db.query(Feedback.category_id, func.count(Feedback.id).label("total")).group_by(Feedback.category_id).all()