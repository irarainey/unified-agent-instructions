---
title: Use FastAPI and SQLModel for the example API
status: Accepted
date: 2026-07-15
deciders: Ira Rainey
---

## Context

The example project needs a small but realistic REST API surface — enough to
show conventions like routing, validation, persistence, and error handling —
without becoming a large application that distracts from its real purpose of
demonstrating agent instruction and context files.

The chosen stack should be idiomatic, widely understood, and expressible in
modern Python so that any conventions captured in instruction files map onto
patterns an agent is likely to encounter elsewhere.

## Decision

We will build the API with **FastAPI** and persist data with **SQLModel** on
top of SQLite.

- **FastAPI** provides declarative routing, dependency injection, and
  automatic request/response validation and OpenAPI documentation, which
  gives agents clear, conventional patterns to follow.
- **SQLModel** unifies the persistence model and the Pydantic schema layer,
  while still allowing separate request/response schemas where the public
  contract should differ from the stored shape.
- **SQLite** keeps the example self-contained and zero-configuration. The
  database URL is overridable via the `BOOKSHELF_DATABASE_URL` environment
  variable so an in-memory database can be used for throwaway runs.

The domain models three entities — `Author`, `Book`, and `Loan` — with table
models kept separate from the API schemas.

## Consequences

- The example runs with no external services, so it is easy to clone and
  start.
- SQLModel table models must avoid `from __future__ import annotations`,
  because deferred string annotations break SQLAlchemy relationship
  resolution; this constraint is a useful, concrete rule to encode in
  instruction files.
- Swapping SQLite for another database later is mostly a matter of changing
  the connection URL and driver, since SQLModel sits on SQLAlchemy.
