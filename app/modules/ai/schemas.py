from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel
from fastapi import Form, File, UploadFile

class AskRequest(BaseModel):
    chat_id: str = "session_default"
    question: str
    provider: Optional[str] = "gemini"
    document: Optional[str] = None
    image: Optional[str] = None

class AskFormRequest:
    def __init__(self,
        chat_id: str = Form("session_default"),
        question: str = Form(...),
        provider: Optional[str] = Form("gemini"),
        file: Optional[UploadFile] = File(None)
    ):
        self.chat_id = chat_id
        self.question = question
        self.provider = provider
        self.file = file

class StepContent(BaseModel):
    id: int
    state: bool
    priority: int
    message: str

class AskResponse(BaseModel):
    chat_id: str
    answer: str
    steps: List[StepContent]

class MessageContent(BaseModel):
    role: str 
    message: str
    steps: List[StepContent]

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

class UpdateStateRequest(BaseModel):
    state: str

class UpdateStepStateRequest(BaseModel):
    state: bool