"""Database models and API schemas for the Bookshelf API.

The module defines three core entities:

* ``Author`` — a person who writes books.
* ``Book`` — a title in the library, linked to a single author.
* ``Loan`` — a record of a book being borrowed by a named borrower.

Table models (persisted with SQLModel) are kept separate from the request and
response schemas so the public API contract can evolve independently of the
storage layer.
"""

from datetime import date, datetime, timezone

from sqlmodel import Field, Relationship, SQLModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Table models
# ---------------------------------------------------------------------------
class Author(SQLModel, table=True):
    """A book author."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    biography: str | None = Field(default=None)

    books: list["Book"] = Relationship(back_populates="author")


class Book(SQLModel, table=True):
    """A book held in the library."""

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    isbn: str | None = Field(default=None, index=True)
    published_year: int | None = Field(default=None)
    author_id: int = Field(foreign_key="author.id", index=True)

    author: Author | None = Relationship(back_populates="books")
    loans: list["Loan"] = Relationship(back_populates="book")


class Loan(SQLModel, table=True):
    """A record of a book being borrowed."""

    id: int | None = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id", index=True)
    borrower: str
    loaned_on: date = Field(default_factory=lambda: _utcnow().date())
    returned_on: date | None = Field(default=None)

    book: Book | None = Relationship(back_populates="loans")


# ---------------------------------------------------------------------------
# Author schemas
# ---------------------------------------------------------------------------
class AuthorCreate(SQLModel):
    name: str
    biography: str | None = None


class AuthorUpdate(SQLModel):
    name: str | None = None
    biography: str | None = None


class AuthorRead(SQLModel):
    id: int
    name: str
    biography: str | None = None


# ---------------------------------------------------------------------------
# Book schemas
# ---------------------------------------------------------------------------
class BookCreate(SQLModel):
    title: str
    author_id: int
    isbn: str | None = None
    published_year: int | None = None


class BookUpdate(SQLModel):
    title: str | None = None
    author_id: int | None = None
    isbn: str | None = None
    published_year: int | None = None


class BookRead(SQLModel):
    id: int
    title: str
    author_id: int
    isbn: str | None = None
    published_year: int | None = None


# ---------------------------------------------------------------------------
# Loan schemas
# ---------------------------------------------------------------------------
class LoanCreate(SQLModel):
    book_id: int
    borrower: str


class LoanRead(SQLModel):
    id: int
    book_id: int
    borrower: str
    loaned_on: date
    returned_on: date | None = None
