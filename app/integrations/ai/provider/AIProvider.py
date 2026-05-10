from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def enviar_mensaje(self, chat_id: str, mensaje: str) -> str:
        pass

    @abstractmethod
    def obtener_historial(self, chat_id: str):
        pass