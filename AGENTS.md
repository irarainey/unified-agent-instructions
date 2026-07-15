# Agent Instructions

## Required: Start From CONTEXT.md

- Read `CONTEXT.md` at the repository root first. Treat it as the always-on
  source of truth and do not ask for information it already contains.
- `CONTEXT.md` is the only context file loaded by default. Open
  `ARCHITECTURE.md`, `DECISIONS.md`, the ADRs under `docs/adrs/`, and any other
  linked document only when the current task needs it — never the whole set up
  front.
- Anything tagged `CRITICAL` in `CONTEXT.md` is binding. If a change would
  contradict a `CRITICAL` constraint, stop and flag it rather than working
  around it.

## Required: Instruction File Mapping

Before modifying or creating any file in this repository, you **must** check `.github/instructions/` for a matching instructions file and follow its rules.

- Each file in `.github/instructions/` has an `applyTo` glob pattern in its front matter (e.g. `applyTo: "**/*.md"`).
- If the file(s) you are about to change match an `applyTo` pattern, read that instructions file first and comply with it.
- This applies to all tools and agents reading this file, not only GitHub-specific tooling.
- If no matching instructions file exists, proceed with standard best practices.

## Required: Personal Copilot Instructions

Always read `~/.copilot/copilot-instructions.md` (the user's personal Copilot instructions file), if it exists, and apply its guidance alongside the rules in this file.
