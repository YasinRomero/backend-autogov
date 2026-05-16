from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel

class Step(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

class AskRequest(BaseModel):
    question: str
    document: Optional[str] = None
    image: Optional[str] = None

class AskResponse(BaseModel):
    chat_id: str
    answer: str
    steps: Optional[list[Step]] = None

class MessageContent(BaseModel):
    role: str 
    message: str

class HistorialResponse(BaseModel):
    chat_id: str
    history: list[MessageContent]
    count: int

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