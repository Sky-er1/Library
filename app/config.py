from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# Определение корневой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Загрузка переменных окружения из .env файла
find_dotenv()
load_dotenv()


class Settings(BaseSettings):
    # Подключение к PostgreSQL
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    def build_url(self) -> str:
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
