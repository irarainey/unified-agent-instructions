"""Seed the Bookshelf database from a JSON fixture.

Creates the database and tables (if needed) and populates them with sample
authors, books, and loans defined in ``data/seed_data.json``.

Run it with::

    uv run python -m bookshelf.seed

By default the script refuses to run against a database that already contains
data. Pass ``--reset`` to drop and recreate all tables before seeding, or
``--force`` to insert into a non-empty database.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from importlib import resources

from sqlmodel import Session, SQLModel, select

from bookshelf.database import create_db_and_tables, engine
from bookshelf.models import Author, Book, Loan


def _load_seed_data() -> dict[str, list[dict]]:
    """Read the bundled seed fixture from the package data directory."""
    source = resources.files("bookshelf.data").joinpath("seed_data.json")
    return json.loads(source.read_text(encoding="utf-8"))


def _parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def _database_is_empty(session: Session) -> bool:
    return session.exec(select(Author)).first() is None


def seed(*, reset: bool = False, force: bool = False) -> dict[str, int]:
    """Create tables and insert the seed data.

    Returns a count of the rows inserted per entity.
    """
    if reset:
        SQLModel.metadata.drop_all(engine)

    create_db_and_tables()

    data = _load_seed_data()

    with Session(engine) as session:
        if not _database_is_empty(session) and not (reset or force):
            raise RuntimeError(
                "Database already contains data. Re-run with --reset to drop and "
                "recreate the tables, or --force to insert anyway."
            )

        for row in data["authors"]:
            session.add(Author(**row))
        for row in data["books"]:
            session.add(Book(**row))
        for row in data["loans"]:
            session.add(
                Loan(
                    id=row["id"],
                    book_id=row["book_id"],
                    borrower=row["borrower"],
                    loaned_on=_parse_date(row["loaned_on"]),
                    returned_on=_parse_date(row.get("returned_on")),
                )
            )
        session.commit()

    return {
        "authors": len(data["authors"]),
        "books": len(data["books"]),
        "loans": len(data["loans"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the Bookshelf database.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate all tables before seeding.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Insert seed data even if the database is not empty.",
    )
    args = parser.parse_args()

    try:
        counts = seed(reset=args.reset, force=args.force)
    except RuntimeError as exc:
        raise SystemExit(f"error: {exc}") from None

    total = sum(counts.values())
    print(
        f"Seeded {total} rows: "
        f"{counts['authors']} authors, "
        f"{counts['books']} books, "
        f"{counts['loans']} loans."
    )


if __name__ == "__main__":
    main()
