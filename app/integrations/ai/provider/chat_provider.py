from abc import ABC, abstractmethod

class ChatProvider(ABC):
    @abstractmethod
    def send_message(self, chat_id: str, mensaje: str) -> str:
        pass

    @abstractmethod
    def get_serializable_history(self, chat_id: str):
        pass