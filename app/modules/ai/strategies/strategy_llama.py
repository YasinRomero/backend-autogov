from app.integrations.ai.provider.llama import llama_client
from app.modules.ai.schemas import AskRequest, AskResponse

def ask_strategy_llama(data: AskRequest) -> AskResponse:
    try:
        # ToDo : Implementar logica de base de datos para chats
        historial_db = [] 
        
        resultado_json = llama_client.enviar_peticion(
            mensaje_actual=data.question,
            historial_previo=historial_db
        )
        
        return AskResponse(
            chat_id=data.chat_id,
            answer=resultado_json.get("answer"),
            steps=resultado_json.get("steps") if resultado_json.get("has_steps") else None
        )
    
    except Exception as e:
        print(f"[Strategy Llama - ERROR]: {e}")
        return AskResponse(
            chat_id=data.chat_id, 
            answer="Error con la estrategia de Llama.", 
            steps=None
        )