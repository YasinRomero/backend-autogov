from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class FeedbackCategory(Base):
    __tablename__ = "feedback_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    feedbacks = relationship("Feedback", back_populates="category")