from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.ai.schemas import AskFormRequest, UpdateStepStateRequest, AskResponse, HistorialResponse, RenameChatRequest, UpdateStateRequest
from app.modules.ai.service import ask_ai, clear_ai_service, delete_all_chats, delete_chat_by_id, get_chat_history, get_fileList, get_user_chats_list, rename_chat_title, update_chat_state, update_step_state
from app.modules.auth.dependencies import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post("/ask", response_model=AskResponse)
async def aiask(data: AskFormRequest = Depends(), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Envía una consulta y/o archivo al asistente de IA para realizar o continuar un trámite municipal.
    """
    return await ask_ai(data=data, db=db, user_id=current_user["user_id"])

@router.get("/history/{chat_id}", response_model=HistorialResponse)
async def fetch_history(chat_id: str, db: Session = Depends(get_db)):
    """
    Recupera el historial completo de mensajes y el estado de los pasos de un chat específico.
    """
    return get_chat_history(chat_id, db)

@router.get("/chats", response_model=list)
def list_user_conversations(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Lista todos los chats o conversaciones creadas por el usuario autenticado.
    """
    return get_user_chats_list(db, user_id=current_user["user_id"] )

@router.delete("/clearchats")
def clear_user_conversations(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Elimina todos los chats y su historial pertenecientes al usuario autenticado.
    """
    return delete_all_chats(db, user_id=current_user["user_id"])

@router.delete("/chats/delete/{chat_id}")
def delete_single_conversation(chat_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Elimina un chat específico identificado por su ID.
    """
    return delete_chat_by_id(chat_id=chat_id, db=db, user_id=current_user["user_id"])

@router.put("/chats/rename/{chat_id}", response_model=dict)
def rename_chat(chat_id: str, data: RenameChatRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Renombra el título de un chat específico del usuario.
    """
    return rename_chat_title(chat_id=chat_id, new_title=data.title, db=db, user_id=current_user["user_id"])

@router.put("/chats/state/{chat_id}", response_model=dict)
def update_chat_state_endpoint(chat_id: str, data: UpdateStateRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Actualiza el estado actual de un trámite municipal en el chat especificado.
    """
    return update_chat_state(chat_id=chat_id, new_state=data.state, db=db, user_id=current_user["user_id"])

@router.put("/chats/steps/update/{step_id}", response_model=dict)
def update_step_state_endpoint(step_id: int, data: UpdateStepStateRequest, db: Session = Depends(get_db)):
    """
    Actualiza el estado de un paso o requisito específico dentro del flujo del trámite.
    """
    return update_step_state(step_id=step_id, new_state=data.state, db=db)

## PROXIMAMENTE DEPRECADOS
@router.post("/clearfiles", response_model=dict)
def clear_ai_system():
    """
    [Próximamente Deprecado] Limpia o elimina todos los archivos temporales guardados en el servicio de IA.
    """
    return clear_ai_service()

## PROXIMAMENTE DEPRECADOS
@router.get("/files", response_model=list)
def list_ai_files():
    """
    [Próximamente Deprecado] Obtiene una lista de todos los archivos asociados al servicio de IA.
    """
    try:
        files = get_fileList()
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener archivos: {str(e)}")
