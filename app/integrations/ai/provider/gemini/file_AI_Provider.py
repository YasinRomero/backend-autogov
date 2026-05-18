from abc import abstractmethod

from app.integrations.ai.provider.chat_provider import ChatProvider

class FileAIProvider(ChatProvider):
    @abstractmethod
    def upload_and_wait(self, file_path):
        pass

    @abstractmethod
    def clear_all_files(self):
        pass

    @abstractmethod
    def get_fileList(self):
        pass