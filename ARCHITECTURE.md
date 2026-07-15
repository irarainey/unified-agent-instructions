# ARCHITECTURE

Structure and boundaries of the Bookshelf API. Implementation detail lives in
the code; this file describes shape, not line-level behaviour.

## Shape

A single FastAPI service backed by SQLite via SQLModel. Layered:

    routers (HTTP)  ->  models (tables + schemas)  <->  database (engine/session)

## Entry points

- `src/bookshelf/main.py` — `create_app()` builds the FastAPI app; `app` is the
  module-level instance. Tables are created on startup (lifespan).
- `src/bookshelf/__main__.py` — runs the app with uvicorn (`uv run bookshelf`).
- `src/bookshelf/seed.py` — CLI that creates and populates the database
  (`uv run bookshelf-seed`).

## Boundaries and data-flow rules

- A request enters a router handler, which takes a session from the
  `get_session` dependency, uses a SQLModel `Session` against SQLite, and
  returns a response schema. See ADR 0006.
- Table models and API schemas are distinct types; handlers convert between
  them at the boundary. See ADR 0005.
- The database URL is read from `BOOKSHELF_DATABASE_URL` (default
  `sqlite:///bookshelf.db`), so tests and throwaway runs can redirect storage.

## Component map

- `routers/authors.py` — author CRUD.
- `routers/books.py` — book CRUD; validates the referenced author exists.
- `routers/loans.py` — borrow and return; enforces loan invariants (ADR 0009).
- `models.py` — `Author`, `Book`, `Loan` table models and their
  create/update/read schemas.
- `database.py` — engine, `get_session`, `create_db_and_tables`.
- `seed.py` + `data/seed_data.json` — seeding from a reviewable JSON fixture.

## Deeper references

- Framework and persistence choice: ADR 0002.
- Model/schema separation: ADR 0005. Session injection: ADR 0006.
- No per-area design docs exist beyond the ADRs under `docs/adrs/`.
