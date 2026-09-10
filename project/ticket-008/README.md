# Ticket 008: Require a deployed unit to attest the revision it is running

- **ID**: ticket-008
- **Owner**: founder
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-09-09

## Goal and scope

The contract already binds the source exactly, verifies content at apply time
and records receipts. None of that answers a later question: is the thing
running still the thing that was merged?

That question has no owner today, and the gap is not theoretical. Measured
across one day of operation in `subactor` on 2026-09-09:

- a service ran four hours on a command a merged change had superseded, and the
  degradation it caused was diagnosed twice before anyone compared the running
  container's command to the repository;
- an executor ran a revision two merges behind while its own fix sat in the
  default branch, so a defect that was already fixed stayed live;
- a session hit a bug that had been fixed five minutes earlier and reported it
  as current.

Deployment receipts were produced and parsed — this is not a missing-writer
problem. No consumer compared them to the merged head, so every drift was
rediscovered as a fresh defect.

Three separate investigations that day diagnosed problems that no longer
existed. In each case a source artifact was read instead of the running one: an
adopter's stale copy of a hook, an older package in an unrelated virtualenv, a
failure log written before its fix landed. The cost is not only wasted work; it
is confident, wrong conclusions about a system that had already healed.

## The invariant

`deploy-running-attestable` states that a deployed unit must be able to name the
exact revision it runs, that the statement must be comparable to the merged
revision, and that an executor must not report a merged change as delivered
until the running revision is observed to contain it.

The sentence carrying the weight is: a receipt that is written and never read
back is not attestation. Every failure above had its evidence produced correctly
and consumed by nobody.

## Non-goals

This ticket adds the invariant and its provenance to the contract. It does not
add a schema field, a checker or an executor capability: the invariant has to
exist before an implementation can claim to satisfy it, and adopting projects
differ too much for one mechanism to be prescribed here yet.

It also does not weaken `deploy-verify-content`. Apply-time verification stays
exactly as it is; this covers the interval after it, which nothing covered.

## Acceptance criteria

- [x] AC-01: `deploy-running-attestable` is a core invariant alongside the
      existing ones, phrased in the same normative style.
- [x] AC-02: Its provenance records the measured evidence, so a future reader
      can tell an observed failure class from a speculative one.
- [x] AC-03: No existing invariant changes meaning, and the invariants remain
      documentation-only — they are not enumerated in a schema or script that
      would drift from this text.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-antigravity.md](ai-antigravity.md)
