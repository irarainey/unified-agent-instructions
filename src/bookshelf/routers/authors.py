"""Endpoints for managing authors."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from bookshelf.database import get_session
from bookshelf.models import Author, AuthorCreate, AuthorRead, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("", response_model=list[AuthorRead])
def list_authors(session: Session = Depends(get_session)) -> list[Author]:
    return list(session.exec(select(Author)).all())


@router.post("", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(
    payload: AuthorCreate, session: Session = Depends(get_session)
) -> Author:
    author = Author.model_validate(payload)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, session: Session = Depends(get_session)) -> Author:
    author = session.get(Author, author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.patch("/{author_id}", response_model=AuthorRead)
def update_author(
    author_id: int,
    payload: AuthorUpdate,
    session: Session = Depends(get_session),
) -> Author:
    author = session.get(Author, author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Author not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(author, field, value)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, session: Session = Depends(get_session)) -> None:
    author = session.get(Author, author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Author not found")
    session.delete(author)
    session.commit()
