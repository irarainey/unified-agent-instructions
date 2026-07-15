---
title: Use FastAPI dependency injection for database sessions
status: Accepted
date: 2026-07-15
deciders: Ira Rainey
---

## Context

Route handlers need a database session to read and write data. Creating a
session inline inside each handler couples the handler to the engine
configuration, repeats lifecycle management (open, commit, close) in every
endpoint, and makes handlers harder to test in isolation.

## Decision

We will provide sessions through **FastAPI dependency injection**.

- A single `get_session` dependency yields a session and guarantees it is
  closed when the request finishes.
- Handlers declare `session: Session = Depends(get_session)` rather than
  constructing sessions themselves.
- Tests can override the dependency to point at a throwaway database.

## Consequences

- Session lifecycle is handled consistently in one place.
- Handlers are easy to test because the session dependency can be overridden.
- Swapping the engine or session strategy is a single change in the dependency
  rather than an edit to every endpoint.
