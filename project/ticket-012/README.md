# Ticket 012: Firmware flashing backup policy by deployment lifecycle

- **ID**: ticket-012
- **Owner**: codex (session authorized by repository owner)
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-10-01

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: the owner requested a shared standard forbidding
flash backups on development rigs and requiring them in production, with adoption
by the connected firmware and fleet projects. This slice delivers the canonical
machine-readable policy and its admission schema; hardware flashing is excluded.

## Acceptance criteria

- [ ] AC-01: Development cannot request or create a pre-flash device backup.
- [ ] AC-02: Production cannot proceed without verified, exact-target recovery evidence.
- [ ] AC-03: Unknown lifecycle fails closed; image hashes and post-flash checks remain mandatory.
- [ ] AC-04: Schema positive/negative canaries pass; product adoption is reported separately.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
