---
description: "Python coding conventions and guidelines"
applyTo: "**/*.py"
---

# Python Coding Conventions

These conventions apply to all Python code in this repository. The example
project targets **Python 3.12**, is managed with **uv**, and is linted and
formatted with **ruff**.

## General Principles

- Prioritise readability and clarity over cleverness.
- Write concise, idiomatic, and maintainable code.
- Break complex functions into smaller, well-named helpers with a single
  responsibility.
- Handle edge cases explicitly (empty inputs, invalid types, missing records)
  and fail with clear, specific errors.

## Naming and Structure

- Use `snake_case` for functions, variables, and modules; `PascalCase` for
  classes; and `UPPER_SNAKE_CASE` for constants.
- Give functions and variables descriptive names that reveal intent.
- Put imports at the top of the module, grouped standard library, third
  party, then local, and avoid imports inside function bodies.

## Type Hints

- Add type hints to all function signatures and public attributes.
- Prefer modern built-in generics and union syntax available in Python 3.12:
  use `list[str]`, `dict[str, int]`, and `str | None` rather than
  `typing.List`, `typing.Dict`, or `typing.Optional`.
- Reach for the `typing`/`collections.abc` modules only for constructs that
  have no builtin form (for example `Callable`, `Iterable`, `Protocol`).

## Docstrings and Comments

- Provide docstrings that follow **PEP 257**, placed immediately after the
  function, method, or class signature line.
- Document the purpose, parameters, return value, and any raised exceptions
  when they are not obvious from the signature.
- Comment on **why** a decision was made, not **what** the code does. Do not
  add redundant comments that merely restate the code.
- Note the purpose of any non-obvious external dependency where it is used.

## Code Style and Formatting

- Follow **PEP 8**, using 4 spaces per indentation level.
- Use blank lines to separate functions, classes, and logical blocks.
- Linting, formatting, and the configured line length are handled by Ruff —
  see [ADR 0004](../../docs/adrs/0004-use-ruff-for-linting-and-formatting.md).

## Error Handling

- Catch the most specific exception type that applies; avoid bare `except:`.
- Raise meaningful exceptions with actionable messages, and use
  `raise ... from` to preserve or intentionally suppress the cause.
- Validate inputs at boundaries (for example API request handlers) and return
  clear errors rather than letting invalid data propagate.

## Dependencies and Environment

- Manage the environment and dependencies with **uv**; do not call `pip`
  directly. Add dependencies with `uv add` and sync with `uv sync`.
- Declare all dependencies in `pyproject.toml`; never rely on globally
  installed packages.

## Related Architecture Decisions

Design and tooling decisions that shape Python code in this repository are
recorded as ADRs rather than repeated here. Follow them when writing code:

- [ADR 0002](../../docs/adrs/0002-use-fastapi-and-sqlmodel.md) — FastAPI and
  SQLModel, including why table modules avoid
  `from __future__ import annotations`.
- [ADR 0003](../../docs/adrs/0003-use-uv-python-and-src-layout.md) — uv,
  Python 3.12, and the `src/` layout.
- [ADR 0004](../../docs/adrs/0004-use-ruff-for-linting-and-formatting.md) —
  Ruff for linting and formatting.
- [ADR 0005](../../docs/adrs/0005-separate-table-models-from-api-schemas.md) —
  separating SQLModel table models from API schemas.
- [ADR 0006](../../docs/adrs/0006-use-dependency-injection-for-sessions.md) —
  FastAPI dependency injection for database sessions.
- [ADR 0007](../../docs/adrs/0007-test-against-throwaway-databases.md) —
  testing against isolated, throwaway databases.

## Example of Proper Documentation

```python
import math


def calculate_area(radius: float) -> float:
    """Calculate the area of a circle.

    Args:
        radius: The radius of the circle.

    Returns:
        The area of the circle, calculated as pi * radius**2.
    """
    return math.pi * radius**2
```
