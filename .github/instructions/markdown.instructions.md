---
description: "Documentation and content creation standards"
applyTo: "**/*.md"
---

## Markdown Content Rules

1. **Headings**: Start each file with a single H1 as its title, then use H2 and
   H3 to structure the rest of the content. Avoid H4 and deeper; restructure
   the content instead.
2. **Lists**: Use bullet points or numbered lists for lists. Ensure proper
   indentation and spacing.
3. **Code Blocks**: Use fenced code blocks for code snippets. Specify the
   language for syntax highlighting.
4. **Links**: Use proper markdown syntax for links. Ensure that links are
   valid and accessible.
5. **Images**: Use proper markdown syntax for images. Include alt text for
   accessibility.
6. **Tables**: Use markdown tables for tabular data. Ensure proper formatting
   and alignment.
7. **Line Length**: Wrap prose at around 80 characters for readability, and
   never exceed 400 characters on a single line.
8. **Whitespace**: Use appropriate whitespace to separate sections and
   improve readability.
9. **Front Matter**: Not every file needs YAML front matter. Include it only
   when the file's own convention calls for it (see **Front Matter
   Conventions** below), and match the fields that convention already uses.

## Formatting and Structure

Follow these guidelines for formatting and structuring your markdown content:

- **Headings**: Use a single `#` for the file's H1 title, `##` for H2, and
  `###` for H3. Keep headings hierarchical — don't skip a level.
- **Lists**: Use `-` for bullet points and `1.` for numbered lists. Indent
  nested lists with two spaces.
- **Code Blocks**: Use triple backticks to create fenced code blocks. Specify
  the language after the opening backticks for syntax highlighting (e.g.,
  `bash).
- **Links**: Use `[link text](URL)` for links. Ensure that the link text is
  descriptive and the URL is valid.
- **Images**: Use `![alt text](image URL)` for images. Include a brief
  description of the image in the alt text.
- **Tables**: Use `|` to create tables. Ensure that columns are properly
  aligned and headers are included.
- **Line Length**: Treat 80 characters as the soft wrap target for prose and
  400 characters as the hard limit — the same rule as item 7 above, not a
  separate one.
- **Whitespace**: Use blank lines to separate sections and improve
  readability. Avoid excessive whitespace.

## Front Matter Conventions

This repository uses different, purpose-built front matter per file type —
there is no single required schema:

- **Instruction files** (`.github/instructions/*.instructions.md`): a
  `description` and an `applyTo` glob pattern, as in this file.
- **ADRs** (`docs/adrs/*.md`): `title`, `status`, `date`, and `deciders`, per
  [ADR 0001](../../docs/adrs/0001-record-architecture-decisions.md).
- **Everything else** (README, `AGENTS.md`, `CONTEXT.md`, `ARCHITECTURE.md`,
  `DECISIONS.md`, `CLAUDE.md`): no front matter. The H1 title is enough.

When creating a new Markdown file, match whichever of these conventions
applies rather than inventing new front matter fields.