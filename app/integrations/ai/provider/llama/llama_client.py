import requests
from app.core.config import settings
from app.integrations.ai.provider.chat_provider import ChatProvider

class LlamaClient(ChatProvider):
    def __init__(self):
        self.api_url = "https://anglit-university.hf.space/ai/ask"
        self.headers = {
            "Content-Type": "application/json",
            "X-Internal-Key": settings.INTERNAL_IA_KEY
        }

    def send_message(self, mensaje_actual: str, historial_previo: list) -> dict:
        try:
            mensajes_payload = list(historial_previo)
            
            mensajes_payload.append({
                "role": "user",
                "content": mensaje_actual
            })
            
            payload = {
                "messages": mensajes_payload
            }
            
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=12)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[Llama - ERROR] Status: {response.status_code} - {response.text}")
                return self._fallback_error("[ERROR] : El microservicio fallo")
                
        except requests.exceptions.Timeout:
            return self._fallback_error("[Llama - ERROR] : La consulta al servidor de Llama tardo demasiado tiempo en responder.")
        except Exception as e:
            print(f"[Llama - Exception] Error de conexión: {str(e)}")
            return self._fallback_error("Llama - ERROR] : No se pudo establecer conexión con el microservicio de contingencia.")

    def _fallback_error(self, mensaje_error: str) -> dict:
        return {
            "answer": f"Ocurrio un inconveniente en el microservicio: {mensaje_error}",
            "has_steps": False,
            "steps": []
        }
    
    def get_serializable_history(self, chat_id: str):
        ## ToDo : Falta
        pass

llama_client = LlamaClient()