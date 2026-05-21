from pydantic.v1 import BaseSettings

class Settings(BaseSettings):

    GEMINI_MODEL: str
    GEMINI_API_KEY: str

    RENIEC_API_URL: str
    RENIEC_API_KEY: str

    INTERNAL_IA_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()