# CONTEXT

Always-on core context. This is the only context file loaded by default. Open
the linked files only when the current task needs them.

## What this is

A repository exploring how multiple AI coding tools (GitHub Copilot, OpenCode,
Crush, Claude Code) can share consistent coding standards on one codebase. It
ships a small example service — the **Bookshelf API** (FastAPI + SQLModel +
SQLite) — for those instruction, agent, and context files to act on.

## Current state

- Example/demo stage, package version `0.1.0`.
- Bookshelf API is runnable: `uv sync --extra dev`, `uv run bookshelf-seed`,
  `uv run bookshelf`.
- 9 ADRs under `docs/adrs/`. No CI. No test suite yet (`testpaths = ["tests"]`
  is configured but `tests/` does not exist).

## Goals

- Demonstrate one shared source of truth for coding standards across Copilot,
  OpenCode, Crush, and Claude Code.
- Keep a small, real example project for the instructions and agents to act on.

## Non-goals

- Not a production library-management system; the domain is intentionally
  minimal (README).
- Not about building or implementing agents, only guiding existing ones
  (AGENTS.md, README).

## Constraints

- `CRITICAL` — A book may have only one active (unreturned) loan at a time; a
  second concurrent loan is rejected. See
  [ADR 0009](docs/adrs/0009-loan-lifecycle-invariants.md).
- `CRITICAL` — Loan returns are one-way: a returned loan cannot be returned
  again. See [ADR 0009](docs/adrs/0009-loan-lifecycle-invariants.md).
- `CRITICAL` — Modules defining SQLModel table models with relationships must
  not use `from __future__ import annotations`; it breaks SQLAlchemy
  relationship resolution at runtime. See
  [ADR 0002](docs/adrs/0002-use-fastapi-and-sqlmodel.md).
- `IMPORTANT` — A book must reference an existing author; otherwise create and
  update are rejected (`src/bookshelf/routers/books.py`).
- `IMPORTANT` — Table models are kept separate from request/response schemas.
  See [ADR 0005](docs/adrs/0005-separate-table-models-from-api-schemas.md).
- `IMPORTANT` — Database sessions come from the `get_session` FastAPI
  dependency, not created inline. See
  [ADR 0006](docs/adrs/0006-use-dependency-injection-for-sessions.md).
- `IMPORTANT` — Manage the environment and dependencies with uv; do not call
  pip. Target runtime is Python 3.12 (pinned). See
  [ADR 0003](docs/adrs/0003-use-uv-python-and-src-layout.md).
- `REFERENCE` — Lint and format with Ruff; line length 100. See
  [ADR 0004](docs/adrs/0004-use-ruff-for-linting-and-formatting.md).
- `REFERENCE` — Default database is SQLite at `sqlite:///bookshelf.db`,
  overridable with `BOOKSHELF_DATABASE_URL` (`src/bookshelf/database.py`).
- `REFERENCE` — Tests should run against a throwaway database; none exist yet.
  See [ADR 0007](docs/adrs/0007-test-against-throwaway-databases.md).

## Load on demand

- [ARCHITECTURE.md](ARCHITECTURE.md) — shape, boundaries, data-flow, component map.
- [DECISIONS.md](DECISIONS.md) — index of all ADRs, newest first.
- [docs/adrs/](docs/adrs/) — full architecture decision records.
- [README.md](README.md) — project overview and run instructions.
- [.github/instructions/](.github/instructions/) — language/file-type coding rules.
