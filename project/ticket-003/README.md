# Ticket 003: Make Deployment DSL Docker checker migration-safe

- **ID**: ticket-003
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-14

## Goal and scope

Make the required conformance container migration-safe across the immutable DSL
manifest revisions used before and after ticket-002. Package both exact
checkers and dispatch only from the manifest's exact `$schema` URI; unknown
revisions fail closed.

## Acceptance criteria

- [ ] AC-01: The ticket binds explicit execution authorization to
  `main@852f3f9`, one infrastructure file and zero runtime dependencies.
- [ ] AC-02: Docker downloads the existing `550e5f…` and current `b7d059…`
  checkers with exact ADD checksums.
- [ ] AC-03: Runtime selects a checker only for the two exact raw schema URIs
  and rejects every unknown or mutable schema reference.
- [ ] AC-04: The image validates both the current main manifest and the
  ticket-002 candidate; governance and Docker build/run checks pass.

## Risks

- A fallback from new to old validation would mask contract failures and is
  forbidden; dispatch happens before validation from an exact allowlist.
- This ticket owns no DSL manifest or domain schema and cannot change their
  semantics.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)
