# Ticket 005: Route hosted CI through exact-schema DSL revision

- **ID**: ticket-005
- **Owner**: unresolved:human
- **Status**: DONE
- **Workflow state**: DONE
- **Created**: 2026-08-14

## Goal and scope

Make the hosted CI migration-safe across the two immutable Deployment DSL
manifest revisions. Resolve the checked-in manifest's exact `$schema` URI to a
hardcoded DSL commit allowlist before checkout; reject unknown or mutable
references without attempting validation.

## Acceptance criteria

- [x] AC-01: The ticket binds continuation authorization to exact protected
  `main@8c601d8`, one implementation file and zero runtime dependencies.
- [x] AC-02: The old schema URI resolves only to checker `550e5f…` and the
  current schema URI resolves only to checker `b7d059…`.
- [x] AC-03: Unknown or mutable schema references stop the workflow before an
  external repository checkout.
- [x] AC-04: Range governance, workflow syntax, both supported resolver cases
  and the fail-closed branch pass before protected publication.

## Validation state

- Repository governance: `GOV-PASS` with zero findings.
- Workflow YAML parse: PASS.
- Protected-main schema resolves to exact DSL commit `550e5f…`: PASS.
- Ticket-002 schema resolves to exact DSL commit `b7d059…`: PASS.
- Static fail-closed assertion confirms no manifest-provided ref and an
  explicit error exit for every non-allowlisted URI: PASS.
- Hosted `test` and `windows-governance` passed on exact final head
  `daae501baa7bd242170f039341013a6ee943ff78`.
- Validator run `31839942567` completed successfully and App review
  `4941117996` approved that exact head.
- The Validator App explicitly merged PR #7 as
  `4f211e82bcbe3c1435b067c396cb7fe4d1c2d749`; protected `main` read-back
  returned the merge and the source branch was deleted.
- End-to-end proof: ticket-002 then passed the current-checker hosted path and
  was independently merged as `a13b6442545f5db3a6b1790a831641a1b888c7b2`;
  its DONE closure is now also on protected `main`.

## Risks

- A default revision or validation fallback would hide unsupported contracts
  and is forbidden.
- The manifest chooses only between hardcoded exact commits; it cannot inject
  an arbitrary checkout ref.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)
