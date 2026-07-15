---
title: Loan lifecycle invariants
status: Accepted
date: 2026-07-15
deciders: Ira Rainey
---

## Context

The loan endpoints enforce two rules that were previously expressed only in
code (`src/bookshelf/routers/loans.py`):

- Creating a loan for a book that already has an unreturned loan is rejected
  with HTTP 409.
- Returning a loan that has already been returned is rejected with HTTP 409.

The library holds a single physical copy of every book, so a book that is out
on loan cannot be lent to anyone else until it is returned.

## Decision

A book may have at most one active (unreturned) loan at a time, and a loan
return is one-way: once `returned_on` is set, the loan cannot be returned
again.

## Consequences

- Loan state is simple to reason about: a book is either available or on one
  loan, mirroring the single-copy holding.
- Callers must handle 409 responses for both a double loan and a double return.
- Supporting multiple copies of a title later would require introducing a
  separate copy or holdings concept and revisiting this invariant.
