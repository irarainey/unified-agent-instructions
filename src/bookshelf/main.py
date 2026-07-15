"""FastAPI application factory and app instance for the Bookshelf API."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from bookshelf import __version__
from bookshelf.database import create_db_and_tables
from bookshelf.routers import authors, books, loans


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title="Bookshelf API",
        version=__version__,
        summary="Example library API for demonstrating agent instruction files.",
        lifespan=lifespan,
    )

    app.include_router(authors.router)
    app.include_router(books.router)
    app.include_router(loans.router)

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
