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
- **Some features are tool-specific and do not port**: not everything has an
  equivalent in every tool. A shared `AGENTS.md` keeps *instructions* aligned,
  but capabilities layered on top of it — custom agents, prompt files, chat
  modes, and similar — are usually defined in a tool's own proprietary format
  and are simply invisible to the others. Using GitHub Copilot as a *provider*
  for another tool does not carry these features across. See
  [Tool-specific features that don't port](#tool-specific-features-that-dont-port).

## AGENTS.md

`AGENTS.md` is a simple, open Markdown format for guiding coding agents.
Think of it as a README for agents: a predictable place to put project context
such as setup commands, test commands, code style, and repo conventions.

This is about helping existing agents work better in your repository, not about
creating or implementing agents themselves.

One `AGENTS.md` can be shared across multiple tools (for example, GitHub
Copilot, OpenCode, and Crush), so you can keep one source of truth for agent
guidance instead of duplicating tool-specific instruction files.

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

The same instructions files and options apply whether you use GitHub Copilot
through the CLI or the Visual Studio Code chat extension — both discover and
load the repository, personal, and `AGENTS.md` instructions in the same way.

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

## Crush

Crush is [Charmbracelet's](https://github.com/charmbracelet/crush) open-source,
terminal-first AI coding agent — a polished TUI written in Go. Like OpenCode, it
is not tied to a single vendor and can be pointed at many model providers,
including GitHub Copilot, so you can drive it with your existing Copilot
subscription while it still reads its instructions from a plain `AGENTS.md`.

Because Crush discovers repository conventions from `AGENTS.md` natively — the
same file OpenCode reads — it needs no Copilot-specific link file. Keeping the
shared rules in `AGENTS.md` means Crush follows the same standards as GitHub
Copilot, OpenCode, and Claude Code without any extra wiring.

Connecting Copilot as Crush's model provider changes which model answers your
prompts, but not which instruction files Crush reads — the same caveat as for
OpenCode, described in
[Using GitHub Copilot as an OpenCode provider](#using-github-copilot-as-an-opencode-provider).
`AGENTS.md` remains the link that keeps
its guidance consistent with the other tools.

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

This repository ships a `CLAUDE.md` at its root that takes a third, simpler
approach: a short note explaining that Claude Code does not support
`AGENTS.md`, directing it to read and follow [AGENTS.md](AGENTS.md) in full, so
the rules live in one place instead of being duplicated.

Either way, `AGENTS.md` stays the single source of truth, and GitHub Copilot,
OpenCode, and Claude Code all end up following the same repository
conventions.

### Allowing Claude Code to read personal Copilot instructions

Like OpenCode, Claude Code restricts file access to the current project
directory by default and will not read files outside of it, even when a
linked-in file such as `AGENTS.md` points to a personal instructions file at
`~/.copilot/copilot-instructions.md`.

To allow Claude Code to read this file, grant it permission to access the
directory by adding a `Read` allow rule to `.claude/settings.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Read(~/.copilot/**)"
    ]
  }
}
```

Without this permission, Claude Code prompts the user to approve access to
`~/.copilot/` the first time it needs to read from it. Configuring the
permission in `.claude/settings.json` makes the access persistent and, since
this file is checked into source control, shares it with every collaborator
on the repository — the same effect that `opencode.json` has for OpenCode.

## Tool-specific features that don't port

A shared `AGENTS.md` (plus the linked `CLAUDE.md`) keeps *instructions*
consistent across tools, but it only covers plain guidance. Several tools layer
richer capabilities on top of their instruction files, and those extras are
defined in tool-specific formats that the other tools neither read nor
understand. As covered in
[Using GitHub Copilot as an OpenCode provider](#using-github-copilot-as-an-opencode-provider),
connecting GitHub Copilot to another tool as a *model provider* only changes
which model answers prompts — it does not carry these extra features across.

The clearest example is **GitHub Copilot's custom agents**, defined as Markdown
files under `.github/agents/`. Each file describes a named, specialized agent —
its purpose, the tools it may use, and the model it runs on — that Copilot can
delegate work to. This is a Copilot convention:

- **OpenCode** and **Crush** read `AGENTS.md`, but they do not read
  `.github/agents/`. They have their own, differently shaped mechanisms for
  subagents, so a Copilot custom agent is invisible to them even when they are
  driven by Copilot as a provider.
- **Claude Code** has its own subagents (under `.claude/agents/`) with a
  different schema, so Copilot's definitions do not transfer either.

The same portability gap applies to other Copilot-specific assets that live
outside `AGENTS.md`, such as:

- **Prompt files** (`.github/prompts/*.prompt.md`) — reusable, parameterized
  prompts.
- **Chat modes** (`*.chatmode.md`) — curated tool-and-instruction bundles for a
  session.
- **`applyTo`-scoped instructions** (`.github/instructions/*.instructions.md`) —
  only GitHub Copilot honors the `applyTo` glob scoping; other tools ignore
  these files entirely unless their rules are also present in `AGENTS.md`.

The practical takeaway: put anything that must apply everywhere into
`AGENTS.md` (and link it into each tool). Treat custom agents, prompt files,
chat modes, and other proprietary extras as **tool-specific enhancements** that
only work in the tool that defines them — do not assume they carry over just
because another tool is using Copilot as its provider.

## Installing the CLI Tools

GitHub Copilot CLI, OpenCode, Crush, and Claude Code all run in the terminal,
so you can try this repository's shared instructions with any of them.

### GitHub Copilot CLI

GitHub Copilot CLI requires an active GitHub Copilot subscription. Install it
with one of the following, then run `copilot` and authenticate with `/login`
on first launch.

```bash
# npm (all platforms, requires Node.js 22 or later)
npm install -g @github/copilot

# Homebrew (macOS and Linux)
brew install --cask copilot-cli

# Install script (macOS and Linux)
curl -fsSL https://gh.io/copilot-install | bash
```

On Windows you can also use WinGet: `winget install GitHub.Copilot`.

### OpenCode CLI

OpenCode CLI needs an API key for the model provider you want to use; run
`/connect` inside the TUI to configure one (this can be GitHub Copilot, as
described above). Install it with one of the following, then run `opencode`.

```bash
# Install script (macOS and Linux)
curl -fsSL https://opencode.ai/install | bash

# npm (all platforms)
npm install -g opencode-ai

# Homebrew (macOS and Linux)
brew install anomalyco/tap/opencode
```

### Crush

Crush also needs a model provider configured (GitHub Copilot or otherwise)
before its first run. Install it with one of the following, then run `crush`.

```bash
# npm (all platforms)
npm install -g @charmland/crush

# Homebrew (macOS and Linux)
brew install charmbracelet/tap/crush
```

### Claude Code

Claude Code requires a Claude subscription or API key. Install it with one of
the following, then run `claude` and authenticate on first launch.

```bash
# npm (all platforms, requires Node.js 18 or later)
npm install -g @anthropic-ai/claude-code

# Install script (macOS, Linux, and WSL)
curl -fsSL https://claude.ai/install.sh | bash
```

## Creating a Personal Instructions File

Personal instructions live outside the repository, in your home directory, and
apply across all of your projects. GitHub Copilot reads them from
`~/.copilot/copilot-instructions.md`. They are the place for preferences that
are about *you*, not the project — so they are never committed and never shared
with the team.

Create the file and add a small amount of information about yourself. The
example below matches the personal instructions used while building this
repository:

```markdown
# Personal Information

- My name is Steve Austin
- My email address is steve.austin@bionic-man.com
```

You can add more over time — for example, a preferred tone for explanations or
a default commit-message style — but keep it to genuine personal preferences.
Anything that should apply to everyone on the team belongs in `AGENTS.md` or
the `.github/instructions/` files instead.

For OpenCode to read this file as well, grant it access to the `~/.copilot/`
directory as shown in
[Allowing OpenCode to read personal Copilot instructions](#allowing-opencode-to-read-personal-copilot-instructions).
For Claude Code to read this file as well, grant it access to the
`~/.copilot/` directory as shown in
[Allowing Claude Code to read personal Copilot instructions](#allowing-claude-code-to-read-personal-copilot-instructions).

## Trying It Out: Questions Only the Context Can Answer

Once the context files (`CONTEXT.md`, `ARCHITECTURE.md`, `DECISIONS.md`), the
`.github/instructions/` files, and your personal instructions file are in
place, every tool can answer questions that have no answer in the code alone.
Run the same prompt in GitHub Copilot CLI, OpenCode, Crush, and Claude Code
and you should get consistent answers, because each tool loads the same
shared context.

To make each test a fair check of what the tools load from context — rather
than something they remember from earlier in the conversation — start each one
from a clean session:

- **GitHub Copilot CLI**: run `/clear` to abandon the current session and start
  fresh (or `/new` to start a new conversation).
- **OpenCode**: run `/new` to clear the current session and start a new one.
- **Crush**: run `/new` (or start it with `crush -y` in a fresh terminal) to
  start a new session.
- **Claude Code**: run `/clear` to reset context while keeping the same
  session, or exit and restart `claude` for a fully clean start.

### Reading facts from the layered context

- **"What is my email address (not read from Git)?"** — The answer comes from your
  personal instructions file, not from your Git configuration. This shows the personal
  layer is being applied.
- **"What is the line length for Markdown files in this project?"** — Answered
  from `.github/instructions/markdown.instructions.md`, which caps Markdown
  lines at 400 characters (with a soft-wrap guideline around 80).
- **"What formatter and line length apply to Python code, and why?"** —
  Answered from the Python instructions and
  [ADR 0004](docs/adrs/0004-use-ruff-for-linting-and-formatting.md): Ruff, with
  a line length of 100.
- **"How many active loans can a book have, and why?"** — Answered from the
  `CRITICAL` constraint in `CONTEXT.md` and
  [ADR 0009](docs/adrs/0009-loan-lifecycle-invariants.md): one, because the
  library holds a single physical copy of every book.

### Validating a change against the decisions

The same context lets a tool check a proposed action against the project's
rules, rather than just doing what it is asked:

- **"I want to lend the same book to two people at once — is that allowed?"** —
  It should flag this as contradicting a `CRITICAL` constraint (ADR 0009)
  rather than implementing it.
- **"Can I add `from __future__ import annotations` to `models.py`?"** — It
  should say no: this is a `CRITICAL` rule because it breaks SQLModel
  relationship resolution (ADR 0002).
- **"Should I run `pip install` to add a dependency?"** — It should point you
  to uv instead, per
  [ADR 0003](docs/adrs/0003-use-uv-python-and-src-layout.md).

If a tool cannot answer these, or gives an answer that disagrees with the
others, that is a signal its context is not wired up correctly — for example a
missing `AGENTS.md` hook, or, for OpenCode or Claude Code, missing permission
to read `~/.copilot/`.

## Context Engineering and Human-First Engineering

The context files this repository leans on — `CONTEXT.md`, `ARCHITECTURE.md`,
`DECISIONS.md`, and the ADRs under `docs/adrs/` — are a deliberate example of
**context engineering**, a practice described in the
[Human-First Engineering](https://humanfirstengineering.dev/) toolkit.

Context engineering is the deliberate practice of capturing, curating, and
preserving the engineering knowledge that humans *and* AI need to reason
correctly about a system over time. It is distinct from prompt engineering:
prompt engineering optimises a single request, while context engineering builds
durable knowledge that is reused across sessions, tools, and people. A model's
context window is finite, and long-running, multi-tool, multi-agent work
quietly compacts it — the first thing lost is usually the expensive part: *why*
a decision was made, what was rejected, and the constraints the code does not
show.

This repository preserves exactly that knowledge instead of letting it scroll
away in a chat history:

- **`CONTEXT.md`** — the always-on core context, including the `CRITICAL`
  constraints that must never be worked around.
- **`ARCHITECTURE.md`** — the shape, boundaries, and component map, loaded on
  demand.
- **`DECISIONS.md`** and **`docs/adrs/`** — the recorded rationale behind each
  decision, so any human or agent can see not just *what* the rules are but
  *why* they exist.

Because that reasoning lives in files every tool can load, GitHub Copilot,
OpenCode, Crush, and Claude Code all reason from the same durable context — and
so does the next engineer who joins. For the full practice, templates, and
guidance, see
[Context Engineering](https://humanfirstengineering.dev/toolkit/context-engineering)
in the Human-First Engineering toolkit.

## Why This Matters for Quality with AI Tools

An AI coding tool is only as consistent as the context it loads. Without shared
instruction and context files, each tool — and each team member — works from
whatever it can infer from the code in front of it, so the same request can
produce different results depending on who ran it and with which tool. Over
time that drift erodes coding standards and makes reviews harder.

Putting the standards in files that every tool reads keeps behaviour consistent
across a repository, a project, and a team:

- **Shared conventions** in `AGENTS.md` and `.github/instructions/` mean every
  tool formats, structures, and documents code the same way.
- **Recorded decisions** in `DECISIONS.md` and the ADRs mean a tool can explain
  *why* a rule exists and check a change against it, instead of silently
  working around it.
- **`CRITICAL` constraints** give the tool a hard stop: if a change would break
  an irreversible or architectural rule, it flags the conflict rather than
  producing plausible-looking code that violates it.
- **Personal instructions** layer individual preferences on top without
  polluting the shared, committed context.

The result is that AI assistance raises code quality instead of undermining it:
the tools accelerate work while staying inside the same guardrails a careful
human reviewer would enforce.

