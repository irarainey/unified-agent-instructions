---
title: Record architecture decisions
status: Accepted
date: 2026-07-15
deciders: Ira Rainey
---

## Context

This repository is an example project used to demonstrate how agent
instruction files, agents, and context files can guide AI coding tools such
as GitHub Copilot, OpenCode, and Claude Code. As the example grows, the
reasoning behind its structure and tooling choices needs to be captured
somewhere durable so that both humans and agents can understand *why* the
code looks the way it does, not just *what* it does.

Architecture Decision Records (ADRs) are a lightweight, well-established way
to capture significant decisions alongside the code they affect. They double
as high-signal context files: an agent that reads the ADRs inherits the
project's conventions and constraints without having to infer them.

## Decision

We will record architecturally significant decisions as ADRs stored under
`docs/adrs/`. Each record is a Markdown file named with a zero-padded
sequence number and a short slug, for example
`0001-record-architecture-decisions.md`.

Each ADR includes:

- Front matter with a `title`, `status`, `date`, and `deciders`.
- A **Context** section describing the forces at play.
- A **Decision** section stating the choice made.
- A **Consequences** section describing the resulting trade-offs.

The `status` field moves through `Proposed`, `Accepted`, `Superseded`, or
`Deprecated`. Superseded records are kept in place and link to the record
that replaces them, so the history stays intact.

## Consequences

- New contributors and AI agents have a single, discoverable place to learn
  the reasoning behind the project's structure.
- Decisions must be written down when they are made, which adds a small
  amount of overhead but avoids repeated re-litigation of settled choices.
- The ADR set becomes a curated context source that agents can be pointed at
  through instruction files.
