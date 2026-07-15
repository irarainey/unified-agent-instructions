---
title: Adopt defensive shell scripting standards
status: Accepted
date: 2026-07-15
deciders: Ira Rainey
---

## Context

Shell scripts fail quietly by default: unset variables expand to nothing,
failing commands in a pipeline are ignored, and temporary files are left
behind. In a repository where multiple tools and agents may generate or edit
scripts, a shared safety baseline is needed so those failure modes are
designed out rather than rediscovered each time.

## Decision

All shell scripts in this repository will follow a **defensive scripting
standard**. Its core pillars are:

- Fail fast with `set -euo pipefail`.
- Clean up temporary resources with a `trap ... EXIT` handler and create them
  with `mktemp`.
- Quote all variable expansions and avoid `eval`.
- Parse structured data with dedicated tools (`jq` for JSON, `yq` for YAML)
  instead of ad-hoc text processing, and fail clearly if they are missing.
- Validate required parameters before doing any work.

The full, detailed ruleset and a reference template live in
`.github/instructions/shell.instructions.md`; this ADR records the decision to
adopt that standard and why.

## Consequences

- Scripts surface errors immediately instead of continuing in a broken state,
  and they clean up after themselves.
- Scripts are slightly more verbose, which is an accepted trade for safety and
  predictability.
- The instruction file remains the single detailed source of the rules, with
  no decision rationale duplicated across files.
