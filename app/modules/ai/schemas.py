from typing import Optional
from pydantic import BaseModel

class Step(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

class AskRequest(BaseModel):
    question: str
    document: Optional[str] = None
    image: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    steps: Optional[list[Step]] = None

class MessageContent(BaseModel):
    role: str 
    message: str

class HistorialResponse(BaseModel):
    chat_id: str
    history: list[MessageContent]