from app.db.session import SessionLocal
from app.models.feedback_category import FeedbackCategory

def init_data():
    db = SessionLocal()
    try:
        if db.query(FeedbackCategory).count() == 0:
            categories = [
                FeedbackCategory(title="Matrimonio Civil", description="..."),
                FeedbackCategory(title="Actas de Nacimiento", description="..."),
                FeedbackCategory(title="Bienes y Propiedades", description="...")
            ]
            db.add_all(categories)
            db.commit()
    finally:
        db.close()