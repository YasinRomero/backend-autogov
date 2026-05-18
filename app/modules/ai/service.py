import os

from app.integrations.ai.provider.gemini import gemini_client
from app.modules.ai.schemas import AskRequest, AskResponse, HistorialResponse
from app.modules.ai.strategies import strategy_genai
from app.modules.ai.strategies.strategy_genai import ask_strategy_genai
from app.modules.ai.strategies.strategy_llama import ask_strategy_llama

ESTRATEGIAS_IA = {
    "llama": ask_strategy_llama,
    "gemini": ask_strategy_genai,
    "genai": ask_strategy_genai
    # Alias para gemini porque me olvide varias veces de cual le puse XD
}

def ask_ai(data: AskRequest) -> AskResponse:
    proveedor_solicitado = data.provider.lower() if data.provider else "gemini"
    
    estrategia_elegida = ESTRATEGIAS_IA.get(proveedor_solicitado, ask_strategy_genai)
    
    return estrategia_elegida(data)

def get_chat_history(chat_id: str) -> HistorialResponse:
    history = gemini_client.get_serializable_history(chat_id)
    return HistorialResponse(chat_id=chat_id, history=history, count=len(history))


def clear_ai_service():
    gemini_client.clear_all_files()
    strategy_genai._cached_guia_file = None
    return {"status": "success", "message": "Cache y archivos borrados correctamente."}

def get_fileList():
    return gemini_client.getfilelist()