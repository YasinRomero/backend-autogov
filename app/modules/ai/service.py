from app.integrations.ai import client

def ask_ai(prompt: str, chat_id: str, files=None) -> str:
    return client.ask_ai(chat_id, prompt, files=files)

def get_chat_history(chat_id: str):
    return client.get_chat_history(chat_id)