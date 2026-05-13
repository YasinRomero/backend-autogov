from fastapi import APIRouter

from app.modules.ai.schemas import AskRequest, AskResponse
from app.modules.ai.service import ask_ai, clear_ai_service

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def aiask(data: AskRequest):
    return ask_ai(data)

@router.post("/clearfiles", response_model=dict)
def clear_ai_system():
    return clear_ai_service()
