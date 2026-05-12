from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def send_message(self, chat_id: str, mensaje: str, files=None) -> str:
        pass

    @abstractmethod
    def get_historial(self, chat_id: str):
        pass