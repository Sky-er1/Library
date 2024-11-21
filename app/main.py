from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List, Optional

from sqlmodel import Session, select

from app.models import Book, BookStatus
from app.database import get_session

app = FastAPI()


@app.post("/books", response_model=Book)
def add_book(
        title: str = Query(..., description="Название книги"),
        author: str = Query(..., description="Автор книги"),
        year: int = Query(..., description="Дата публикации"),
        session: Session = Depends(get_session),
):
    existing_book = session.execute(
        select(Book).where(Book.title == title, Book.author == author,
                           Book.year == year)
    ).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Boook already exists")

    new_book = Book(title=title, author=author, year=year)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)

    return new_book


@app.get("/books", response_model=List[Book])
def get_books(session: Session = Depends(get_session)):
    statement = select(Book)
    results = session.execute(statement)
    books = results.scalars().all()

    return books


@app.delete("/books", response_model=Book)
def delete_book(book_id: int = Query(None, description="ID's book"),
                session: Session = Depends(get_session)):
    result = session.execute(select(Book).where(Book.id == book_id))
    deleting_book = result.first()
    if not deleting_book:
        raise HTTPException(status_code=404, detail="No Book found")
    session.delete(deleting_book)
    session.commit()
    return deleting_book


@app.get("/books/search", response_model=List[Book])
def search_books(
        title: Optional[str] = Query(None, description="Search books by title"),
        author: Optional[str] = Query(None,
                                      description="Search books by author"),
        year: Optional[int] = Query(None, description="Search books by year"),
        session: Session = Depends(get_session),
):
    if not any([title, author, year]):
        raise HTTPException(
            status_code=400,
            detail="Pls enter on of title, author and year"
        )

    statement = select(Book)

    if title:
        statement = statement.where(Book.title.ilike(f'%{title}%'))
    if author:
        statement = statement.where(Book.author.ilike(f'%{author}%'))
    if year:
        statement = statement.where(Book.year == year)

    results = session.execute(statement)
    books = results.scalars().all()
    if not books:
        raise HTTPException(status_code=404, detail="No Books found")
    return books


@app.patch("/books/{book_id}", response_model=Book)
def update_book_status(
        book_id: int,
        new_status: BookStatus = Query(
            ...,
            description="New status of the book ('в наличии' или 'выдана')"),
        session: Session = Depends(get_session),
):
    # Проверяем, существует ли книга
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.status = new_status
    session.add(book)
    session.commit()
    session.refresh(book)

    return book
