from fastapi import APIRouter

from app.modules.ai.schemas import AskRequest, AskResponse
from app.modules.ai.service import askai

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def aiask(data: AskRequest):
    return askai(data)
