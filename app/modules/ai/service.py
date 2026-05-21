import os

from sqlalchemy.orm import Session

from app.integrations.ai.provider.gemini import gemini_client
from app.models.chat import Chat
from app.models.message import Message
from app.modules.ai.schemas import AskRequest, AskResponse, HistorialResponse
from app.modules.ai.strategies import strategy_genai
from app.modules.ai.strategies.strategy_genai import ask_strategy_genai
from app.modules.ai.strategies.strategy_llama import ask_strategy_llama

ESTRATEGIAS_IA_ASK = {
    "llama": ask_strategy_llama,
    "gemini": ask_strategy_genai,
    "genai": ask_strategy_genai
    # Alias para gemini porque me olvide varias veces de cual le puse XD
}


def ask_ai(data: AskRequest, db, user_id: int) -> AskResponse:
    proveedor_solicitado = data.provider.lower() if data.provider else "gemini"
    
    estrategia_elegida = ESTRATEGIAS_IA_ASK.get(proveedor_solicitado, ask_strategy_genai)
    
    return estrategia_elegida(data, db, user_id)

def get_chat_history(chat_id: str, db: Session) -> HistorialResponse:
    # LOGICA LEGACY : LA DEJO POR SI LAS DUDAS
    # history = gemini_client.get_serializable_history(chat_id)
    # return HistorialResponse(chat_id=chat_id, history=history, count=len(history))
    try:
        mensajes_db = (
            db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .all()
        )
        
        history = [
            {"role": m.role, "message": m.content} 
            for m in mensajes_db
        ]
        
        return HistorialResponse(
            chat_id=chat_id, 
            history=history, 
            count=len(history)
        )
    
    except Exception as e:
        print(f"[Service Get History DB - ERROR]: {e}")
        return HistorialResponse(chat_id=chat_id, history=[], count=0)
    finally:
        db.close()

def clear_ai_service():
    gemini_client.clear_all_files()
    strategy_genai._cached_guia_file = None
    return {"status": "success", "message": "Cache y archivos borrados correctamente."}

def get_fileList():
    return gemini_client.getfilelist()

def get_user_chats_list(db: Session, user_id: int):
    try:
        chats = (
            db.query(Chat)
            .filter(Chat.user_id == user_id)
            .order_by(Chat.created_at.desc())
            .all()
        )
        return [
            {
                "chat_id": c.id, 
                "title": c.title, 
                "created_at": c.created_at.strftime("%Y-%m-%d %H:%M")
            } 
            for c in chats
        ]
    finally:
        db.close()