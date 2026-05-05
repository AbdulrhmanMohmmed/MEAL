from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str = "MEAL System - Yemen"
    APP_VERSION: str = "2.0.0"
    SECRET_KEY: str = "meal-system-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    DATABASE_URL: str = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(__file__)), 'meal.db')}"
    KOBO_API_URL: str = "https://kf.kobotoolbox.org"
    KOBO_API_TOKEN: str = ""
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")

    class Config:
        env_file = ".env"


settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
