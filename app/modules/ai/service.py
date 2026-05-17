import os

from app.integrations.ai.provider.gemini import gemini_client
from app.modules.ai.schemas import AskRequest, AskResponse, HistorialResponse

_cached_guia_file = None

PATH_GUIA_BODAS = "docs/GUIABODASLINCE.pdf"

def ask_ai(data: AskRequest) -> AskResponse:
    global _cached_guia_file 
    
    try:
        if _cached_guia_file is None:
            if os.path.exists(PATH_GUIA_BODAS):
                print("Subiendo PDF por primera vez...")
                _cached_guia_file = gemini_client.upload_and_wait(PATH_GUIA_BODAS)
        else:
            print(f"Usando PDF ya subido anteriormente: {_cached_guia_file.name}")

        archivos_mensaje = []
        if _cached_guia_file:
            archivos_mensaje.append(_cached_guia_file)

        if data.image:
            archivos_mensaje.append(data.image)

        raw_answer = gemini_client.ask_ai(
            chat_id="session_default",
            prompt=data.question, 
            files=archivos_mensaje
        )

        return AskResponse(
            chat_id="session_default",
            answer=raw_answer,
            steps=None
        )
    
    # ToDo : Cambiar las referencias de chat_id, actualmente todas son estaticas

    except Exception as e:
        print(f"Error en el service ask_ai: {e}")
        return AskResponse(
            answer="Lo siento, ocurrió un error al procesar tu solicitud municipal.",
            steps=None
        )
        

def get_chat_history(chat_id: str) -> HistorialResponse:
    history = gemini_client.get_serializable_history(chat_id)

    return HistorialResponse(
        chat_id=chat_id,
        history=history,
        count=len(history)
    )


def clear_ai_service():
    global _cached_guia_file
    gemini_client.clear_all_files()
    _cached_guia_file = None
    return {"status": "success", "message": "Archivos borrados y cache limpiado"}

def get_fileList():
    return gemini_client.getfilelist()