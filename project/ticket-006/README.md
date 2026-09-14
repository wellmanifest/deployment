# Ticket 006: Prevent runtime activation provenance regressions

- **ID**: ticket-006
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-08-30

## Goal and scope

Prevent a verified candidate from being reported as deployed while a different
checkout, entrypoint, symlink target or process image remains active. Extend the
neutral deployment contract with activation identity and behavior probes; do
not prescribe a process manager, filesystem layout or adapter.

## Acceptance criteria

- [ ] AC-01: Verification cannot be `verified` without proving the active
  revision and active entrypoint against the selected source.
- [ ] AC-02: A behavior smoke runs through the same public/operator entrypoint
  used after activation, not directly against a build checkout.
- [ ] AC-03: Activation mismatch maps to `applied_unverified` and remains
  visible in the deployment receipt.
- [ ] AC-04: Schema, DSL conformance, Docker and governance checks pass.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)
