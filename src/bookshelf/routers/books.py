"""Endpoints for managing books."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from bookshelf.database import get_session
from bookshelf.models import Author, Book, BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


def _ensure_author_exists(author_id: int, session: Session) -> None:
    if session.get(Author, author_id) is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=f"Author {author_id} does not exist"
        )


@router.get("", response_model=list[BookRead])
def list_books(
    author_id: int | None = None, session: Session = Depends(get_session)
) -> list[Book]:
    statement = select(Book)
    if author_id is not None:
        statement = statement.where(Book.author_id == author_id)
    return list(session.exec(statement).all())


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, session: Session = Depends(get_session)) -> Book:
    _ensure_author_exists(payload.author_id, session)
    book = Book.model_validate(payload)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, session: Session = Depends(get_session)) -> Book:
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int, payload: BookUpdate, session: Session = Depends(get_session)
) -> Book:
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")
    data = payload.model_dump(exclude_unset=True)
    if "author_id" in data:
        _ensure_author_exists(data["author_id"], session)
    for field, value in data.items():
        setattr(book, field, value)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, session: Session = Depends(get_session)) -> None:
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")
    session.delete(book)
    session.commit()
