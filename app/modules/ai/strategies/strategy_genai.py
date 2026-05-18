import os

from sqlalchemy.orm import Session
from app.integrations.ai.provider.gemini import gemini_client
from app.modules.ai.schemas import AskRequest, AskResponse

PATH_GUIA_BODAS = "docs/GUIABODASLINCE.pdf"
_cached_guia_file = None

def ask_strategy_genai(data: AskRequest, db: Session, user_id: int) -> AskResponse:
    global _cached_guia_file 
    try:
        if _cached_guia_file is None:
            if os.path.exists(PATH_GUIA_BODAS):
                print("[Strategy GenAI] Subiendo PDF por primera vez...")
                _cached_guia_file = gemini_client.upload_and_wait(PATH_GUIA_BODAS)
        else:
            print(f"[Strategy GenAI] Usando PDF ya subido anteriormente: {_cached_guia_file.name}")

        archivos_mensaje = []
        if _cached_guia_file:
            archivos_mensaje.append(_cached_guia_file)
        if data.image:
            archivos_mensaje.append(data.image)

        raw_answer = gemini_client.ask_ai(
            chat_id=data.chat_id, 
            prompt=data.question, 
            files=archivos_mensaje
        )

        return AskResponse(
            chat_id=data.chat_id, 
            answer=raw_answer, 
            steps=None
        )
    except Exception as e:
        print(f"[Strategy GenAI] Error: {e}")
        return AskResponse(
            chat_id=data.chat_id, 
            answer="Error al procesar la solicitud con la estrategia de Google GenAI.", 
            steps=None
        )