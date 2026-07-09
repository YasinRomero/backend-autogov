from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.ai.schemas import AskFormRequest, AskRequest, AskResponse, HistorialResponse, RenameChatRequest, UpdateStateRequest
from app.modules.ai.service import ask_ai, clear_ai_service, delete_all_chats, delete_chat_by_id, get_chat_history, get_fileList, get_user_chats_list, rename_chat_title, update_chat_state
from app.modules.auth.dependencies import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post("/ask", response_model=AskResponse)
async def aiask(data: AskFormRequest = Depends(), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await ask_ai(data=data, db=db, user_id=current_user["user_id"])

@router.get("/history/{chat_id}", response_model=HistorialResponse)
async def fetch_history(chat_id: str, db: Session = Depends(get_db)):
    return get_chat_history(chat_id, db)

@router.get("/chats", response_model=list)
def list_user_conversations(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_user_chats_list(db, user_id=current_user["user_id"] )

@router.delete("/clearchats")
def clear_user_conversations(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delete_all_chats(db, user_id=current_user["user_id"])

@router.delete("/chats/delete/{chat_id}")
def delete_single_conversation(chat_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delete_chat_by_id(chat_id=chat_id, db=db, user_id=current_user["user_id"])

@router.put("/chats/rename/{chat_id}", response_model=dict)
def rename_chat(chat_id: str, data: RenameChatRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return rename_chat_title(chat_id=chat_id, new_title=data.title, db=db, user_id=current_user["user_id"])

@router.put("/chats/state/{chat_id}", response_model=dict)
def update_chat_state_endpoint(chat_id: str, data: UpdateStateRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return update_chat_state(chat_id=chat_id, new_state=data.state, db=db, user_id=current_user["user_id"])

## PROXIMAMENTE DEPRECADOS
@router.post("/clearfiles", response_model=dict)
def clear_ai_system():
    return clear_ai_service()

## PROXIMAMENTE DEPRECADOS
@router.get("/files", response_model=list)
def list_ai_files():
    try:
        files = get_fileList()
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener archivos: {str(e)}")
