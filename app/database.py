from typing import Generator
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from app.config import settings

# URL для синхронной базы данных
DATABASE_URL = settings.build_url()

# Создаём синхронный движок
engine = create_engine(DATABASE_URL, echo=True)

# Создаём фабрику сессий
sync_session = sessionmaker(bind=engine, expire_on_commit=False)

# Функция зависимости для получения сессии
def get_session() -> Generator[Session, None, None]:
    with sync_session() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
