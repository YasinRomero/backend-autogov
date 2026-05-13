from fastapi import APIRouter, Depends

from app.modules.ai.schemas import AskRequest, AskResponse, HistorialResponse
from app.modules.ai.service import ask_ai, clear_ai_service
from app.modules.auth.dependencies import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post("/ask", response_model=AskResponse)
def aiask(data: AskRequest):
    return ask_ai(data)

@router.post("/clearfiles", response_model=dict)
def clear_ai_system():
    return clear_ai_service()

@router.post("/historial", response_model=HistorialResponse)
def get_historial():
    return get_historial()

