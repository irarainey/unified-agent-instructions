---
title: Manage the project with uv, Python 3.12, and a src layout
status: Accepted
date: 2026-07-15
deciders: Ira Rainey
---

## Context

The example needs a reproducible, modern Python setup that is quick to
recreate on any machine and that reflects current best practice, so that
tooling conventions captured in instruction files stay relevant.

Two recurring sources of subtle bugs in Python projects are inconsistent
dependency resolution and accidental reliance on the current working
directory being importable. Both are worth designing out from the start in a
project meant to model good conventions.

## Decision

We will standardise on the following project tooling:

- **uv** for environment and dependency management. The virtual environment
  lives in `.venv`, dependencies are declared in `pyproject.toml`, and the
  resolved set is locked with `uv sync`.
- **Python 3.12**, pinned via `.python-version` and `requires-python` in
  `pyproject.toml`, so everyone runs the same interpreter series.
- A **`src/` layout**, with the importable package at `src/bookshelf/`. This
  prevents the repository root from being implicitly importable and forces
  the package to be installed (or `src` added to `PYTHONPATH`) exactly as it
  would be in production.
- Tests and tooling resolve the package through `pythonpath = ["src"]` and
  the editable install produced by `uv sync`.

## Consequences

- A fresh checkout becomes runnable with `uv sync`, and the API starts with
  `uv run bookshelf` or the VS Code "FastAPI: Uvicorn" debug configuration.
- The `src/` layout adds one level of nesting but eliminates a whole class of
  import-path ambiguity, which is a good convention to model.
- Contributors need `uv` installed; this is a deliberate trade of a small
  onboarding step for fast, reproducible environments.
