from sqlalchemy.orm import Session

from app.integrations.ai.provider.llama.llama_client import llama_client
from app.models.chat import Chat
from app.models.message import Message
from app.modules.ai.schemas import AskRequest, AskResponse

def ask_strategy_llama(data: AskRequest, db: Session, user_id: int) -> AskResponse:
    try:

        chat_existente = db.query(Chat).filter(Chat.id == data.chat_id).first()

        if not chat_existente:
            chat_existente = Chat(id=data.chat_id, user_id=user_id, title=data.question[:20] + "...")
            db.add(chat_existente)
            db.commit()

        mensajes_db = db.query(Message).filter(Message.chat_id == data.chat_id).order_by(Message.created_at.desc()).limit(3).all()

        mensajes_db.reverse()

        historial_previo = [{"role": m.role, "content": m.content} for m in mensajes_db]
        
        resultado_json = llama_client.send_message(
            mensaje_actual=data.question,
            historial_previo=historial_previo
        )

        respuesta_ia = resultado_json.get("answer", "Sin respuesta.")
        steps_ia = resultado_json.get("steps") if resultado_json.get("has_steps") else None

        nuevo_msg_user = Message(chat_id=data.chat_id, role="user", content=data.question)
        nuevo_msg_ia = Message(chat_id=data.chat_id, role="assistant", content=respuesta_ia)

        db.add_all([nuevo_msg_user, nuevo_msg_ia])
        db.commit()
        
        return AskResponse(
            chat_id=data.chat_id,
            answer=respuesta_ia,
            steps=steps_ia
        )
    
    except Exception as e:
        db.rollback()
        print(f"[Strategy Llama - ERROR]: {e}")
        return AskResponse(
            chat_id=data.chat_id, 
            answer="Error con la estrategia de Llama o la DB", 
            steps=None
        )