# Ticket 009: Adopt published governance for atomic delivery

- **ID**: ticket-009
- **Owner**: agent:codex
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-09-14

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: the user requested continued implementation,
testing and publication of standards that support fast delivery. This disjoint
governance ticket adopts published new-project 0.20.29 through Goal to replace
the obsolete plan-only-commit requirement blocking ticket-006. Preserve Linux,
Windows, Docker and independent Validator gates; do not rewrite existing history.
The repository's reusable workflow pin and required-checks instance are part of
this adoption. No deployment schema or normative deployment semantics change.

## Acceptance criteria

- [x] AC-01: The immutable published governance package is adopted without manual hash edits.
- [x] AC-02: Required Linux/Windows/Docker checks remain, and workflow uses the same immutable standard.
- [ ] AC-03: Managed gate and independent publication pass; intent may join material delivery atomically.

Local validation: managed gate, required-checks names, host hook, Worktrees v5,
the pinned DSL checker, two canonical schema examples and networkless Docker
conformance passed. The broader standard-pack baseline remains audit-only and
reports seven unadopted packs; no claim of full pack enforcement is made.
The published package supplies tiered budgets. Under the user's authorization
to adjust nonconflicting limits, this ticket uses class M (at most nine
non-managed files, still two components and no runtime dependencies). CI exposed
missing DSL ownership for adopted schemas. The target-owned projection renderer
binds all managed package files directly to the verified lock; its regression
tests and CI check keep later adoptions reproducible without weakening DSL gates.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)
