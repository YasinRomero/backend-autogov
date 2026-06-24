from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class ChatContext(Base):
    __tablename__ = "chat_contexts"

    id = Column(String, primary_key=True, index=True)
    chat_id = Column(String, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())