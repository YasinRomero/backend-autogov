from pydantic import BaseModel
from typing import Optional

class FeedbackCreate(BaseModel):
    title: str
    description: Optional[str] = None
    points: int = 0
    category_id: int

class FeedbackResponse(FeedbackCreate):
    id: int
    user_id: int
    category_title: Optional[str] = None

    class Config:
        from_attributes = True

class CategoryCount(BaseModel):
    category_id: int
    total: int

    class Config:
        from_attributes = True