---
title: Test against isolated, throwaway databases
status: Accepted
date: 2026-07-15
deciders: Ira Rainey
---

## Context

Tests that share a database with development, or with each other, become
order-dependent and flaky: leftover rows from one test change the outcome of
another. The application already supports overriding its database location
through the `BOOKSHELF_DATABASE_URL` environment variable and through the
`get_session` dependency.

## Decision

Tests will run against an **isolated, throwaway database** rather than the
development database.

- Point tests at an in-memory or temporary SQLite database via
  `BOOKSHELF_DATABASE_URL` or by overriding the `get_session` dependency.
- Each test (or test module) starts from a known, empty state and does not
  depend on data left behind by other tests.
- Tests must be deterministic and independent of execution order.

## Consequences

- Test runs are reliable and repeatable, with no shared mutable state.
- Tests are fast because they avoid a persistent on-disk database.
- The example project does not yet ship a test suite; this ADR sets the
  strategy any future tests must follow.
