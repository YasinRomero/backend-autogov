import os

from app.integrations.ai import client
from app.modules.ai.schemas import AskRequest, AskResponse

_cached_guia_file = None

PATH_GUIA_BODAS = "docs/GUIABODASLINCE.pdf"

def ask_ai(data: AskRequest) -> AskResponse:
    global _cached_guia_file 
    
    try:
        if _cached_guia_file is None:
            if os.path.exists(PATH_GUIA_BODAS):
                print("Subiendo PDF por primera vez...")
                _cached_guia_file = client.upload_and_wait(PATH_GUIA_BODAS)
        else:
            print(f"Usando PDF ya subido anteriormente: {_cached_guia_file.name}")

        archivos_mensaje = []
        if _cached_guia_file:
            archivos_mensaje.append(_cached_guia_file)

        if data.image:
            archivos_mensaje.append(data.image)

        raw_answer = client.ask_ai(
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
        
def get_chat_history(chat_id: str):
    return client.get_history(chat_id)


def clear_ai_service():
    global _cached_guia_file
    client.clear_all_files()
    _cached_guia_file = None
    return {"status": "success", "message": "Archivos borrados y cache limpiado"}

def get_fileList():
    return client.getfilelist()