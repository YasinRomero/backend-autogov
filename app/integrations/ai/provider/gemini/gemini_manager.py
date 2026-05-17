from fileinput import filelineno
import time

from app.core.config import settings
from google import genai
from google.genai.types import Tool, GenerateContentConfig
from app.integrations.ai.provider.AIProvider import AIProvider

class GeminiManager(AIProvider):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.sessions = {}
        self.uploaded_files_names = []

    def get_or_create_chat(self, chat_id):
        if chat_id not in self.sessions:
            print(f"Iniciando memoria local para el chat: {chat_id}")
            
            instrucciones = (
                "Eres el asistente virtual de una Municipalidad distrital de Lima, Perú. "
                "Tu fuente de verdad es el documento PDF adjunto. "
                "Responde con precisión basándote en el archivo. Si la información no está, "
                "indícalo y da una recomendación general no vinculante."
            )

            configuracion = GenerateContentConfig(
                system_instruction=instrucciones,
                temperature=0.1
            )

            chat = self.client.chats.create(
                model=settings.GEMINI_MODEL,
                config=configuracion
            )

            self.sessions[chat_id] = chat

        return self.sessions[chat_id]

    def upload_and_wait(self, file_path):
        print(f"Subiendo {file_path} a Google File API...")
        uploaded_file = self.client.files.upload(file=file_path)
        
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(1)
            uploaded_file = self.client.files.get(name=uploaded_file.name)
        
        if uploaded_file.state.name == "FAILED":
            raise Exception("El procesamiento del archivo en Google falló")
        
        self.uploaded_files_names.append(uploaded_file.name)
        return uploaded_file


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
            return "Error al conectar con el servidor municipal."

    def get_serializable_history(self, chat_id):
        if chat_id not in self.sessions:
            return []
            
        chat = self.sessions[chat_id]
        
        try:
            raw_history = chat.get_history() 
        except AttributeError:
            return []
        
        serializable = []
        for content in raw_history:
            text_parts = [part.text for part in content.parts if part.text]
            
            if text_parts:
                serializable.append({
                    "role": content.role,
                    "parts": [{"text": " ".join(text_parts)}]
                })
                
        return serializable
    
    def clear_all_files(self):
        print(f"Limpiando {len(self.uploaded_files_names)} archivos de Google...")
        
        for file_name in self.uploaded_files_names:
            try:
                self.client.files.delete(name=file_name)
                print(f"Eliminado: {file_name}")
            except Exception as e:
                print(f"Error al eliminar {file_name}: {e}")
        
        self.uploaded_files_names = []
        self.sessions = {} 
        print("Sistema reseteado por completo.")

    def get_fileList(self):
        files_data = []
        
        for file in self.client.files.list():
            files_data.append({
                "display_name": file.display_name,
                "name": file.name,
                "state": file.state.name,
                "created_time": str(file.create_time),
                "expiration_time": str(file.expiration_time)
            })
        return files_data