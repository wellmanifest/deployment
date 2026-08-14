# Ticket 004: Route Compose conformance through exact-schema dispatcher

- **ID**: ticket-004
- **Owner**: unresolved:human
- **Status**: DONE
- **Workflow state**: DONE
- **Created**: 2026-08-14

## Goal and scope

Remove the stale Compose command override so the required conformance service
uses the image's fail-closed, exact-schema dispatcher delivered by ticket-003.
This is an infrastructure-only repair and does not change Deployment DSL
documents, schemas or authority semantics.

## Acceptance criteria

- [x] AC-01: The ticket binds the observed Compose bypass to exact protected
  `main@932ce37`, one implementation file and zero runtime dependencies.
- [x] AC-02: `docker compose run --rm conformance` uses the image dispatcher
  and validates the current immutable main manifest.
- [x] AC-03: The same Compose service validates the ticket-002 manifest through
  its pinned checker while networking remains disabled.
- [x] AC-04: Repository governance, Docker build and both regression runs pass.

## Validation state

- Repository governance: `GOV-PASS` with zero findings.
- Resolved Compose config has no service command override and retains
  `network_mode: none`.
- Docker build: PASS with the checksum-bound dual-checker image.
- Current protected-main manifest through Compose: `DSL-PASS`.
- Ticket-002 current-checker manifest mounted read-only through the same
  Compose service: `DSL-PASS`.
- Hosted `test` and `windows-governance` checks passed on exact head
  `69db0da956cd5cb591f856957992127b3efe0a7b`.
- Validator run `31838822194` completed successfully and App review
  `4941028299` approved that exact head.
- The Validator App explicitly merged PR #4 as
  `15ea7b123e4d09c424b70d74064b1a7910ef4715`; protected `main` read-back
  returned the merge and the source branch was deleted.

## Risks

- Compose must not duplicate checker selection because it can drift from the
  image entry contract, as this defect demonstrated.
- The dispatcher remains fail-closed; this ticket does not introduce fallback
  after a checker reports a validation error.

## Participants

- Human participant: unresolved; no user-* file was created by this work.
- Agent participant: [ai-codex.md](ai-codex.md)
