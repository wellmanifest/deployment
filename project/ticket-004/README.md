# Ticket 004: Route Compose conformance through exact-schema dispatcher

- **ID**: ticket-004
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-14

## Goal and scope

Remove the stale Compose command override so the required conformance service
uses the image's fail-closed, exact-schema dispatcher delivered by ticket-003.
This is an infrastructure-only repair and does not change Deployment DSL
documents, schemas or authority semantics.

## Acceptance criteria

- [x] AC-01: The ticket binds the observed Compose bypass to exact protected
  `main@932ce37`, one implementation file and zero runtime dependencies.
- [ ] AC-02: `docker compose run --rm conformance` uses the image dispatcher
  and validates the current immutable main manifest.
- [ ] AC-03: The same Compose service validates the ticket-002 manifest through
  its pinned checker while networking remains disabled.
- [ ] AC-04: Repository governance, Docker build and both regression runs pass.

## Risks

- Compose must not duplicate checker selection because it can drift from the
  image entry contract, as this defect demonstrated.
- The dispatcher remains fail-closed; this ticket does not introduce fallback
  after a checker reports a validation error.

## Participants

- Human participant: unresolved; no user-* file was created by this work.
- Agent participant: [ai-codex.md](ai-codex.md)
