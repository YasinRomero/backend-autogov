import inspect
import os

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.integrations.ai.provider.gemini import gemini_client
from app.models.chat import Chat
from app.models.message import Message
from app.models.step import Step
from app.modules.ai.schemas import AskRequest, AskResponse, HistorialResponse
from app.modules.ai.strategies import strategy_genai
from app.modules.ai.strategies.strategy_genai import ask_strategy_genai
from app.modules.ai.strategies.strategy_llama import ask_strategy_llama

ESTRATEGIAS_IA_ASK = {
    "llama": ask_strategy_llama,
    "gemini": ask_strategy_genai,
    "genai": ask_strategy_genai,
    # Alias para gemini porque me olvide varias veces de cual le puse XD
}


async def ask_ai(data: AskRequest, db: Session, user_id: int) -> AskResponse:
    proveedor_solicitado = data.provider.lower() if data.provider else "gemini"

    estrategia_elegida = ESTRATEGIAS_IA_ASK.get(proveedor_solicitado, ask_strategy_genai)

    if inspect.iscoroutinefunction(estrategia_elegida):
        return await estrategia_elegida(data, db, user_id)

    return estrategia_elegida(data, db, user_id)


def get_chat_history(chat_id: str, db: Session) -> HistorialResponse:
    # LOGICA LEGACY : LA DEJO POR SI LAS DUDAS
    # history = gemini_client.get_serializable_history(chat_id)
    # return HistorialResponse(chat_id=chat_id, history=history, count=len(history))
    try:
        mensajes_db = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.asc()).all()

        history = []
        for m in mensajes_db:
            pasos_db = db.query(Step).filter(Step.message_id == m.id).all()
            pasos_map = [{"id": p.id, "state": p.state, "priority": p.priority, "message": p.content} for p in pasos_db]
            history.append({"role": m.role, "message": m.content, "steps": pasos_map})

        return HistorialResponse(chat_id=chat_id, history=history, count=len(history))

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
        chats = db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.created_at.desc()).all()
        return [
            {"chat_id": c.id, "title": c.title, "created_at": c.created_at.strftime("%Y-%m-%d %H:%M"), "state": c.state}
            for c in chats
        ]
    finally:
        db.close()


def delete_all_chats(db: Session, user_id: int):
    try:

        db.query(Chat).filter(Chat.user_id == user_id).delete(synchronize_session=False)
        db.commit()

        return {
            "status": "success",
            "message": "Todos tus chats, mensajes y archivos temporales han sido eliminados correctamente.",
        }

    except Exception as e:
        db.rollback()
        print(f"[Service Clear Chats - ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Error interno al intentar vaciar el historial de chats.")
    finally:
        db.close()


def delete_chat_by_id(chat_id: str, db: Session, user_id: int):
    try:
        chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).first()

        if not chat:
            raise HTTPException(status_code=404, detail="El chat no existe o no tienes permisos para eliminarlo.")

        db.delete(chat)
        db.commit()

        return {"status": "success", "message": f"El chat '{chat_id}' y todos sus mensajes han sido eliminados."}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"[Service Delete Chat - ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Error interno al intentar eliminar el chat.")


def rename_chat_title(chat_id: str, new_title: str, db: Session, user_id: int):
    try:
        chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).first()

        if not chat:
            raise HTTPException(status_code=404, detail="El chat no existe o no tienes permisos para modificarlo.")

        chat.title = new_title
        db.commit()
        db.refresh(chat)

        return {
            "status": "success",
            "message": "Chat renombrado exitosamente.",
            "chat_id": chat.id,
            "new_title": chat.title,
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"[Service Rename Chat - ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Error interno al intentar renombrar el chat.")


def update_chat_state(chat_id: str, new_state: str, db: Session, user_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat no encontrado")

    chat.state = new_state
    db.commit()
    db.refresh(chat)
    return {"message": "Estado actualizado correctamente", "new_state": chat.state}


def update_step_state(step_id: int, new_state: bool, db: Session):
    step = db.query(Step).filter(Step.id == step_id).first()
    if not step:
        raise HTTPException(status_code=404, detail="Step no encontrado")

    step.state = new_state
    db.commit()
    db.refresh(step)
    return {"message": "Estado actualizado correctamente", "new_state": step.state}
