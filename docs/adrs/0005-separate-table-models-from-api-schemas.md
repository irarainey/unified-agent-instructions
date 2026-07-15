---
title: Separate SQLModel table models from API schemas
status: Accepted
date: 2026-07-15
deciders: Ira Rainey
---

## Context

SQLModel allows a single class to serve as both the database table model and
the Pydantic schema used at the API boundary. Convenient as that is, it
couples the persisted storage shape directly to the public API contract, so a
change to one is silently a change to the other.

## Decision

We will define **table models** (declared with `table=True`) separately from
the **request and response schemas** used by the API.

- Table models describe how data is stored.
- Dedicated `*Create`, `*Update`, and `*Read` schemas describe the public
  contract for each operation.
- Handlers convert between the two explicitly (for example with
  `model_validate`).

## Consequences

- The API contract can evolve independently of the database layout, and fields
  can be hidden, added, or reshaped at the boundary without a migration.
- There is a small amount of apparent duplication between models and schemas,
  which is an accepted trade for the clearer boundary and safer evolution.
- The rule is captured here rather than in the Python instruction file.
