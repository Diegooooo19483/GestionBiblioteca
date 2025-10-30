import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    # === Configuración general ===
    APP_NAME: str = os.getenv("APP_NAME", "GestionBiblioteca")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # === Base de datos ===
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./BibliotecaApi.db")

    # === Otros valores opcionales ===
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE", 10))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
