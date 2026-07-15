# Consistent AI Coding Standards Across Multiple Tools

This repo explores how a team can use different AI coding tools — GitHub
Copilot, OpenCode, Claude Code, and others — on the same codebase while
keeping coding standards consistent, documenting each tool's instruction
conventions, the caveats that come with mixing them, and the approach used to
bridge them together. It also includes a small example project — a Bookshelf
API — for those instructions, agents, and context files to act on.

## Goal

A team can use different AI coding tools — GitHub Copilot, OpenCode, Claude
Code, and others — on the same repository, but doing so is not automatic.
Each tool has its own conventions for where it looks for instructions, so
without a deliberate strategy, engineers on the same team can end up with
inconsistent coding standards depending on which tool they happen to use.

This repo documents those differences and the caveats they introduce, and
captures the approach we're using to bridge them — a shared `AGENTS.md` as
the single source of truth, linked into each tool's own convention — so every
engineer gets the same guidance no matter which tool sits in their harness.

## Example Project: Bookshelf API

To make these ideas concrete, the repository includes a small but real
codebase for the instructions, agents, and context files to act on: a
**Bookshelf API**, a REST service for managing library books, their authors,
and loans.

The API itself is deliberately unremarkable — the point is not the domain,
but having a genuine project where you can watch different tools follow (or
ignore) the shared conventions. It gives instruction files something to
constrain, agents something to build against, and context files (such as the
ADRs under `docs/adrs/`) somewhere real to draw project knowledge from.

### What it does

The service is built with **FastAPI** and persists data with **SQLModel** on
top of SQLite. It exposes CRUD endpoints for three related entities:

- **Authors** — create, list, fetch, update, and delete authors.
- **Books** — the same operations, each book linked to an existing author,
  with optional filtering by author.
- **Loans** — borrow and return books, enforcing that a book can only be on
  one active loan at a time.

Interactive OpenAPI documentation is available at `/docs` once the app is
running, and a `/health` endpoint provides a simple liveness check.

### Project layout

The code uses a `src/` layout so the package is imported exactly as it would
be when installed, rather than relying on the repository root being on the
path:

```text
src/bookshelf/
  main.py            # FastAPI app factory and app instance
  database.py        # SQLModel engine and session management
  models.py          # Table models and request/response schemas
  seed.py            # Seed script that creates and populates the database
  routers/           # Route handlers for authors, books, and loans
  data/              # JSON seed fixture
docs/adrs/           # Architecture Decision Records
```

### Running it

The project targets **Python 3.12** and manages its environment and
dependencies with [uv](https://docs.astral.sh/uv/). From the repository root:

```bash
# Create the virtual environment and install dependencies
uv sync --extra dev

# Populate the database with sample data (6 authors, 15 books, 6 loans)
uv run bookshelf-seed

# Start the API with hot reload on http://127.0.0.1:8000
uv run bookshelf
```

The seed script reads `src/bookshelf/data/seed_data.json`, so the sample data
stays reviewable in diffs and the database file itself is never committed. A
VS Code launch configuration ("FastAPI: Uvicorn") is included so the API can
also be started and debugged with F5.

## Caveats and Challenges

- **Different discovery mechanisms**: GitHub Copilot, OpenCode, and Claude
  Code each look for instructions in different files and locations, so a
  file that works for one tool is invisible to the others unless it's linked
  in.
- **Provider vs. instructions are separate concerns**: connecting a tool to
  GitHub Copilot as a model provider (as OpenCode can) only changes which
  model answers prompts — it does not make that tool read Copilot's
  instruction files.
- **Scope layering differs per tool**: repository, personal/user, and
  organization-level instructions exist in each tool, but the file names,
  locations, and precedence rules are not the same, so layered guidance has
  to be reasoned about per tool.
- **No single native standard (yet)**: `AGENTS.md` is emerging as a common,
  open format, but not every tool reads it natively — some need a symlink or
  an import to pull it in, which has to be set up and maintained.

## AGENTS.md

`AGENTS.md` is a simple, open Markdown format for guiding coding agents.
Think of it as a README for agents: a predictable place to put project context
such as setup commands, test commands, code style, and repo conventions.

This is about helping existing agents work better in your repository, not about
creating or implementing agents themselves.

One `AGENTS.md` can be shared across multiple tools (for example, GitHub
Copilot and OpenCode), so you can keep one source of truth for agent guidance
instead of duplicating tool-specific instruction files.

This helps define better coding standards across a repository by giving every
AI tool the same rules to follow, regardless of which one a team member uses.
Rather than each tool drifting toward its own conventions, everyone works from
a shared source of truth, which keeps output consistent across the team and
makes it easier to onboard new tools without rewriting instructions.

## GitHub Copilot Instructions Files

GitHub Copilot is GitHub's AI pair programmer, available as an IDE extension,
a CLI, and a chat interface, and is tightly integrated with the GitHub
platform. It supports its own conventions for instructions files, in
addition to support for `AGENTS.md`.

- **Repository instructions**: A `.github/copilot-instructions.md` file
  applies to the whole repository. For more targeted guidance,
  `.github/instructions/*.instructions.md` files can each declare an
  `applyTo` glob pattern in their front matter, so the rules only apply when
  matching files are being created or modified.
- **Personal instructions**: A `~/.copilot/copilot-instructions.md` file on a
  user's own machine applies across all of that user's repositories,
  letting individuals layer personal preferences on top of shared,
  repository-level guidance.

## OpenCode

OpenCode is an open-source, terminal-first AI coding agent that is not tied
to any single vendor, and can be configured to use models from many
different providers, including GitHub Copilot.

Despite that flexibility, OpenCode does not recognize GitHub Copilot's
conventions — it does not read `.github/copilot-instructions.md`,
`.github/instructions/*.instructions.md`, or
`~/.copilot/copilot-instructions.md`. Instead, it looks for a plain
`AGENTS.md` file in the repository.

This is why `AGENTS.md` is used as the common link between the two tools: by
keeping the shared repo conventions in `AGENTS.md` and having the GitHub
Copilot instructions reference it, both Copilot and OpenCode end up following
the same rules, even though each tool discovers instructions in a different
way.

### Using GitHub Copilot as an OpenCode provider

OpenCode can connect to GitHub Copilot as a model provider, either by running
`/connect` inside the TUI or by adding it to `~/.config/opencode/opencode.json`.
This lets OpenCode send prompts through your existing Copilot subscription,
using Copilot's models to generate responses.

Connecting Copilot as a provider only changes which model answers your
prompts — it does not make OpenCode read any of GitHub Copilot's instruction
files. OpenCode still ignores `.github/copilot-instructions.md`,
`.github/instructions/*.instructions.md`, and `~/.copilot/copilot-instructions.md`
regardless of which provider it's using. It only ever loads instructions from
`AGENTS.md` (project-level) and `~/.config/opencode/AGENTS.md` (global), which
is why `AGENTS.md` remains the required link for keeping instructions
consistent between the two tools.

### Allowing OpenCode to read personal Copilot instructions

Some Copilot setups reference a personal instructions file at
`~/.copilot/copilot-instructions.md`, outside of the repository, for a
user's own preferences layered on top of shared guidance. By default,
OpenCode restricts file access to the current project directory and will
not read files outside of it, even when a linked-in file such as
`AGENTS.md` points to that location.

To allow OpenCode to read this file, grant it permission to access the
directory by adding an `external_directory` permission entry to
`opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "external_directory": {
      "~/.copilot/**": "allow"
    }
  }
}
```

Without this permission, OpenCode prompts the user to approve access to
`~/.copilot/` every time it needs to read from it, and that approval only
lasts for the current run — it resets the next time OpenCode starts.
Configuring the permission in `opencode.json` makes the access persistent,
so personal instructions are followed consistently without repeated
prompts.

## Claude Code

Claude Code is Anthropic's terminal-based coding agent. Like GitHub Copilot,
it does not natively read `AGENTS.md` — it uses its own `CLAUDE.md` file
instead, which can be scoped at the managed (org), user (`~/.claude/CLAUDE.md`),
project (`./CLAUDE.md`), or local (`./CLAUDE.local.md`) level.

To bring Claude Code into the same shared-instructions convention as GitHub
Copilot and OpenCode, keep the canonical rules in `AGENTS.md` and link
`CLAUDE.md` to it rather than duplicating content, using either approach:

- **Symlink**: Create `CLAUDE.md` as a symlink to `AGENTS.md`, so both files
  are always identical.
- **Import**: Keep `CLAUDE.md` as a thin file that pulls in `AGENTS.md` using
  Claude Code's `@path` import syntax (e.g. `@AGENTS.md`).

Either way, `AGENTS.md` stays the single source of truth, and GitHub Copilot,
OpenCode, and Claude Code all end up following the same repository
conventions.
