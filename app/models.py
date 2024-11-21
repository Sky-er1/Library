from typing import Optional
from enum import Enum

from sqlmodel import Field, SQLModel, create_engine

from app.config import settings


class BookStatus(str, Enum):
    AVAILABLE = 'в наличи'
    ISSUED = 'выдана'


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    author: str = Field(nullable=False)
    year: int = Field(nullable=False, description='Год издания книги')
    status: BookStatus = Field(default=BookStatus.AVAILABLE, nullable=False)


DATABASE_URL = settings.build_url()
engine = create_engine(DATABASE_URL, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)
