from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    priority = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    state = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())

    message = relationship("Message", back_populates="steps")
