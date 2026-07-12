from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    points = Column(Integer, default=0)
    
    category_id = Column(Integer, ForeignKey("feedback_categories.id", ondelete="SET NULL"))
    category = relationship("FeedbackCategory", back_populates="feedbacks")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    category = relationship("FeedbackCategory", back_populates="feedbacks")
    
    user = relationship("User")

    @property
    def category_title(self):
        if self.category_id == 0:
            return "Sugerencia de categoría"
    
        return self.category.title if self.category else "Desconocido"