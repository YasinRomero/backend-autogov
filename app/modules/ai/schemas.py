from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel

class AskRequest(BaseModel):
    chat_id: str = "session_default"
    question: str
    provider: Optional[str] = "gemini"
    document: Optional[str] = None
    image: Optional[str] = None

class AskResponse(BaseModel):
    chat_id: str
    answer: str
    steps: Optional[List[str]] = None

class MessageContent(BaseModel):
    role: str 
    message: str

class HistorialResponse(BaseModel):
    chat_id: str
    history: list[MessageContent]
    count: int

class RenameChatRequest(BaseModel):
    title: str

class BaseAIService(ABC):
    @abstractmethod
    def buscar_y_redactar(self, messages: list) -> dict:
        pass
        
    @abstractmethod
    def listar_archivos(self) -> list:
        pass

    @abstractmethod
    def limpiar_sistema(self) -> dict:
        pass