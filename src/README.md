# Bookshelf API — Developer Guide

This is the developer-level guide to the code under `src/bookshelf/`. The
top-level [README.md](../README.md) explains why this project exists (as a
demo for shared AI agent instructions); this file explains how the API itself
is put together, so you can find your way around the code, run it locally,
and know where a change belongs.

For the reasoning behind specific design choices, see the ADRs under
[`docs/adrs/`](../docs/adrs/) — this guide describes shape and flow, not
rationale.

## What it does

The Bookshelf API is a small REST service for a library. It exposes CRUD
endpoints over three related entities:

- **Authors** — people who write books.
- **Books** — titles in the library, each linked to one author.
- **Loans** — records of a book being borrowed and (eventually) returned.

A book can only be on one active loan at a time, and once a loan is returned
it cannot be returned again — see
[ADR 0009](../docs/adrs/0009-loan-lifecycle-invariants.md) for why.

## How it's built

- **FastAPI** provides routing, request/response validation, and the
  auto-generated OpenAPI docs at `/docs`.
- **SQLModel** (built on SQLAlchemy and Pydantic) defines both the database
  tables and, separately, the API's request/response schemas.
- **SQLite** is the database, reached through a single SQLAlchemy engine.

See [ADR 0002](../docs/adrs/0002-use-fastapi-and-sqlmodel.md) for why this
stack was chosen.

## How a request flows

```text
client
  -> router handler (routers/*.py)
       -> get_session dependency (database.py) hands it a Session
       -> handler queries/writes SQLModel table models (models.py)
       -> handler converts the result to a response schema
  <- JSON response
```

- Every handler receives its database session via FastAPI's dependency
  injection (`Depends(get_session)`) rather than opening one itself — see
  [ADR 0006](../docs/adrs/0006-use-dependency-injection-for-sessions.md).
- Table models (`Author`, `Book`, `Loan`) describe how data is stored.
  `*Create`, `*Update`, and `*Read` schemas describe what the API accepts and
  returns. Handlers convert between the two explicitly — see
  [ADR 0005](../docs/adrs/0005-separate-table-models-from-api-schemas.md).

## Project structure

```text
src/bookshelf/
  __init__.py        # Package version
  __main__.py         # `uv run bookshelf` entry point — runs uvicorn with reload
  main.py             # create_app(): builds the FastAPI app, registers routers,
                       # creates tables on startup, and adds the /health endpoint
  database.py         # SQLAlchemy engine, get_session dependency, table creation
  models.py           # Author/Book/Loan table models and their Create/Update/Read schemas
  seed.py             # `uv run bookshelf-seed` entry point — loads data/seed_data.json
  data/
    seed_data.json    # Sample authors, books, and loans used by seed.py
  routers/
    authors.py        # /authors CRUD
    books.py           # /books CRUD; validates the referenced author exists
    loans.py           # /loans — borrow and return, enforcing the loan invariants
```

### Module responsibilities at a glance

| Module | Responsible for |
| --- | --- |
| `main.py` | Assembling the app: routers, startup lifecycle, `/health` |
| `database.py` | The database connection and handing out sessions |
| `models.py` | The shape of stored data and the public API contract |
| `routers/*.py` | HTTP behaviour — validation, status codes, error responses |
| `seed.py` | Populating a fresh database with reviewable sample data |

## Configuration

The only environment-driven setting is the database location:

- `BOOKSHELF_DATABASE_URL` — defaults to `sqlite:///bookshelf.db`. Point this
  at an in-memory database (`sqlite://`) for tests or throwaway runs. See
  [ADR 0007](../docs/adrs/0007-test-against-throwaway-databases.md).

## Running and seeding locally

From the repository root, with dependencies installed (`uv sync --extra
dev`):

```bash
# Populate the database with sample data (6 authors, 15 books, 6 loans)
uv run bookshelf-seed

# Re-run against a database that already has data
uv run bookshelf-seed --force

# Drop and recreate all tables first, then seed
uv run bookshelf-seed --reset

# Start the API with hot reload on http://127.0.0.1:8000
uv run bookshelf
```

Once running, visit `/docs` for interactive OpenAPI documentation, or
`/health` for a liveness check.

## Making changes

- New Python code follows
  [`.github/instructions/python.instructions.md`](../.github/instructions/python.instructions.md)
  — 3.12 type hints, PEP 8 via Ruff, and docstrings that explain *why*, not
  *what*.
- Run the formatter and linter after changing code:

  ```bash
  uv run ruff format
  uv run ruff check --fix
  ```

- If a change would touch one of the `CRITICAL` constraints in
  [`CONTEXT.md`](../CONTEXT.md) — such as the loan invariants or the ban on
  `from __future__ import annotations` in `models.py` — read the linked ADR
  first rather than working around it.
- No test suite exists yet, but `pytest` is configured (`pythonpath =
  ["src"]`, `testpaths = ["tests"]`) and should follow
  [ADR 0007](../docs/adrs/0007-test-against-throwaway-databases.md) once
  added.
