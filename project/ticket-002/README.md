# Ticket 002: Restore Deployment DSL manifest conformance

- **ID**: ticket-002
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-14

## Goal and scope

Migrate the existing deployment profile to the current published DSL manifest
contract without changing the Deployment DSL schema or effect semantics. Add
the missing document vocabulary, proportional controlled-effects publication
policy, and an immutable lock to the exact shared DSL schema revision.

## Acceptance criteria

- [x] AC-01: The ticket binds the user's execution instruction to exact
  `main@852f3f9`, one implementation file and zero runtime dependencies.
- [x] AC-02: The manifest declares `vocabularyKind=commands` and the complete
  controlled publication policy required by its effect model.
- [x] AC-03: DSL mapping, schema URL and standards lock all use immutable
  revision `b7d0595...` with the published schema digest.
- [ ] AC-04: Current manifest/standards checks, repository governance and the
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
- Docker conformance on this branch: BLOCKED because its base image still
  embeds DSL checker revision `550e5f…`, which rejects the current v1 fields.
- Coordinated infrastructure candidate
  `ticket/003-dsl-checker-migration@6acf9f3` validates both this manifest and
  the old `main` manifest with networking disabled. It must pass protected
  review and land first; ticket-002 can then rebase and run its own AC-04
  without combining two implementation tickets in one diff.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)
