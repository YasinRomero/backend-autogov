from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def send_message(self, chat_id: str, mensaje: str, files=None) -> str:
        pass

    @abstractmethod
    def get_serializable_history(self, chat_id: str):
        pass

    @abstractmethod
    def upload_and_wait(self, file_path):
        pass
    
    @abstractmethod
    def clear_all_files(self):
        pass

    @abstractmethod
    def get_fileList(self):
        pass