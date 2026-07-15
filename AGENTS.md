# Agent Instructions

## Required: Instruction File Mapping

Before modifying or creating any file in this repository, you **must** check `.github/instructions/` for a matching instructions file and follow its rules.

- Each file in `.github/instructions/` has an `applyTo` glob pattern in its front matter (e.g. `applyTo: "**/*.md"`).
- If the file(s) you are about to change match an `applyTo` pattern, read that instructions file first and comply with it.
- This applies to all tools and agents reading this file, not only GitHub-specific tooling.
- If no matching instructions file exists, proceed with standard best practices.

## Required: Personal Copilot Instructions

Always read `~/.copilot/copilot-instructions.md` (the user's personal Copilot instructions file), if it exists, and apply its guidance alongside the rules in this file.
