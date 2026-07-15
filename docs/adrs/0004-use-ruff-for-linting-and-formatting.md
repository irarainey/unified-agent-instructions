---
title: Use Ruff for linting and formatting
status: Accepted
date: 2026-07-15
deciders: Ira Rainey
---

## Context

Multiple tools and AI agents edit the code in this repository, so style needs
to be deterministic and enforced by tooling rather than debated or applied by
hand. Python historically spreads this responsibility across several tools
(for example a separate formatter, import sorter, and linter), which is slower
and more to configure.

## Decision

We will use **Ruff** as the single tool for both linting and formatting Python
code.

- Configuration lives in `pyproject.toml` under `[tool.ruff]`.
- The line length is **100 characters**.
- After changing Python code, run the formatter and linter and fix any issues:

```bash
uv run ruff format
uv run ruff check --fix
```

## Consequences

- One fast tool replaces a stack of separate style tools, with a single source
  of configuration.
- Agents and contributors have a deterministic style target, so formatting
  differences never appear in diffs or reviews.
- The concrete style rules stay out of the instruction files, which reference
  this decision instead of restating it.
