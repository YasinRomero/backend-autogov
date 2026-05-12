from app.integrations.ai.provider import AIProvider
from app.integrations.ai.provider.gemini_manager import GeminiManager

ai_service: AIProvider = GeminiManager()

def ask_ai(prompt: str, chat_id: str, files=None):
    return ai_service.send_message(chat_id, prompt, files=files)

def get_chat_history(chat_id: str):
    return ai_service.get_historial(chat_id)