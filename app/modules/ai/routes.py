from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.ai.schemas import AskRequest, AskResponse, HistorialResponse
from app.modules.ai.service import ask_ai, clear_ai_service, get_chat_history, get_fileList
from app.modules.auth.dependencies import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post("/ask", response_model=AskResponse)
def aiask(data: AskRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return ask_ai(data=data, db=db, user_id=current_user["user_id"])

@router.post("/clearfiles", response_model=dict)
def clear_ai_system():
    return clear_ai_service()

@router.get("/history/{chat_id}", response_model=HistorialResponse)
async def fetch_history(chat_id: str):
    return get_chat_history(chat_id)

@router.get("/files", response_model=list)
def list_ai_files():
    try:
        files = get_fileList()
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener archivos: {str(e)}")
