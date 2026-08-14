# Ticket 002: Restore Deployment DSL manifest conformance

- **ID**: ticket-002
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-08-14

## Goal and scope

Migrate the existing deployment profile to the current published DSL manifest
contract without changing the Deployment DSL schema or effect semantics. Add
the missing document vocabulary, proportional controlled-effects publication
policy, and an immutable lock to the exact shared DSL schema revision.

## Acceptance criteria

- [x] AC-01: The ticket binds the original execution instruction to exact
  `main@852f3f9` and the post-dependency continuation to exact
  `main@8c601d8`, with one implementation file and zero runtime dependencies.
- [x] AC-02: The manifest declares `vocabularyKind=commands` and the complete
  controlled publication policy required by its effect model.
- [x] AC-03: DSL mapping, schema URL and standards lock all use immutable
  revision `b7d0595...` with the published schema digest.
- [x] AC-04: Current manifest/standards checks, repository governance and the
  required Docker build/conformance run pass.

## Risks

- This is a profile migration only; it must not grant deployment authority or
  alter the closed deployment document schema.
- Docker remains required by repository governance and is validation evidence,
  not an executor invocation.

## Validation state

- Current DSL manifest and standards lock: PASS.
- Repository governance: `GOV-PASS` with zero findings.
- Docker build: PASS.
- Docker Compose conformance on the rebased branch: `DSL-PASS` with networking
  disabled and exact-schema checker selection.
- Coordinated ticket-003 and the practice-derived ticket-004 repair are both
  `DONE` on protected `main`; this ticket remains a manifest-only migration.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)
