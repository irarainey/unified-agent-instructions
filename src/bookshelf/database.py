"""Database engine and session management for the Bookshelf API.

Uses SQLModel over a local SQLite database. The database file location can be
overridden with the ``BOOKSHELF_DATABASE_URL`` environment variable, which
makes it easy to point tests at an in-memory database.
"""

from __future__ import annotations

import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("BOOKSHELF_DATABASE_URL", "sqlite:///bookshelf.db")

# check_same_thread is disabled so the SQLite connection can be shared across
# FastAPI's threadpool workers.
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    """Create all tables declared on the SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session for use as a FastAPI dependency."""
    with Session(engine) as session:
        yield session
