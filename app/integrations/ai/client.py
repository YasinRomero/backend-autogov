from app.core.config import settings
from google import genai
from google.genai.types import Tool, GenerateContentConfig

class GeminiManager:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.sessions = {}

    def get_or_create_chat(self, chat_id):
        if chat_id not in self.sessions:
            print(f"Iniciando memoria local para el chat: {chat_id}")
            
            herramientas = [{"url_context": {}}]

            instrucciones = (
                "Eres el asistente virtual de una Municipalidad distrital limeña/Peru. "
                "Tu única fuente de verdad es el documento de requisitos que se te proporcionará en el primer mensaje. "
                "Si algo no está en el documento, di que no tienes esa información confiable pero de igual forma darás recomendaciones que no garantizan ser veridicas."
            )

            configuracion = GenerateContentConfig(
                system_instruction=instrucciones,
                tools=herramientas,
                temperature=0.1
            )

            chat = self.client.chats.create(
                model=settings.GEMINI_MODEL,
                config=configuracion
            )

            url_bodas = "https://drive.google.com/file/d/17mu3bbvLvhuLAdoz5FvQ-KVcbMIMJr-o/view?usp=sharing"
            chat.send_message(f"Analiza este documento base para nuestro chat: {url_bodas}")

            self.sessions[chat_id] = chat

        return self.sessions[chat_id]

    # def enviar_mensaje(self, chat_id, mensaje):
    #     try:
    #         chat = self.get_or_create_chat(chat_id)
    #         response = chat.send_message(mensaje)
    #         return response.text
    #     except Exception as e:
    #         print(f"DEBUG ERROR: {e}")
    #         return "Lo siento, tuve un problema al conectar con el servidor municipal."

    def send_message(self, chat_id, mensaje, files=None):
        try:
            chat = self.get_or_create_chat(chat_id)
            
            contenido = [mensaje]
            if files:
                if isinstance(files, list):
                    contenido.extend(files)
                else:
                    contenido.append(files)
            
            response = chat.send_message(message=contenido)
            return response.text
        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            return "Lo siento, tuve un problema al conectar con el servidor municipal."

    def obtener_historial(self, chat_id):
        if chat_id in self.sessions:
            return self.sessions[chat_id].get_history()
        return []