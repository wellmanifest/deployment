# Ticket 003: Make Deployment DSL Docker checker migration-safe

- **ID**: ticket-003
- **Owner**: unresolved:human
- **Status**: DONE
- **Workflow state**: DONE
- **Created**: 2026-08-14

## Goal and scope

Make the required conformance container migration-safe across the immutable DSL
manifest revisions used before and after ticket-002. Package both exact
checkers and dispatch only from the manifest's exact `$schema` URI; unknown
revisions fail closed.

## Acceptance criteria

- [x] AC-01: The ticket binds explicit execution authorization to
  `main@852f3f9`, one infrastructure file and zero runtime dependencies.
- [x] AC-02: Docker downloads the existing `550e5f…` and current `b7d059…`
  checkers with exact ADD checksums.
- [x] AC-03: Runtime selects a checker only for the two exact raw schema URIs
  and rejects every unknown or mutable schema reference.
- [x] AC-04: The image validates both the current main manifest and the
  ticket-002 candidate; governance and Docker build/run checks pass.

## Validation state

- Repository governance: `GOV-PASS` with zero findings.
- Docker build: PASS with both checker downloads verified by SHA-256.
- Current `main` manifest through the compatibility service command: PASS.
- Ticket-002 manifest through the image's exact-schema dispatcher: PASS with
  networking disabled and the candidate manifest mounted read-only.
- Existing manifest with a third, unlisted schema URI: rejected before checker
  execution with `DSL-MANIFEST-001` as required.
- Hosted `test` and `windows-governance` checks passed on exact head
  `6be23a215b41ba1966858450f5920c150a3aa3d1`.
- Validator run `31837653093` completed successfully and App review
  `4940927243` approved that exact head.
- The Validator App explicitly merged PR #2 as
  `0f53c3e9541daa70ec7319bd0b36337a1a6b3646`; protected `main` read-back
  returned that commit and the source branch was deleted.

## Risks

- A fallback from new to old validation would mask contract failures and is
  forbidden; dispatch happens before validation from an exact allowlist.
- This ticket owns no DSL manifest or domain schema and cannot change their
  semantics.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)
