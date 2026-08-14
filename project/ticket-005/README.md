# Ticket 005: Route hosted CI through exact-schema DSL revision

- **ID**: ticket-005
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-14

## Goal and scope

Make the hosted CI migration-safe across the two immutable Deployment DSL
manifest revisions. Resolve the checked-in manifest's exact `$schema` URI to a
hardcoded DSL commit allowlist before checkout; reject unknown or mutable
references without attempting validation.

## Acceptance criteria

- [x] AC-01: The ticket binds continuation authorization to exact protected
  `main@8c601d8`, one implementation file and zero runtime dependencies.
- [ ] AC-02: The old schema URI resolves only to checker `550e5f…` and the
  current schema URI resolves only to checker `b7d059…`.
- [ ] AC-03: Unknown or mutable schema references stop the workflow before an
  external repository checkout.
- [ ] AC-04: Range governance, workflow syntax and hosted old-profile checks
  pass; the ticket-002 PR passes after rebasing onto the repair.

## Risks

- A default revision or validation fallback would hide unsupported contracts
  and is forbidden.
- The manifest chooses only between hardcoded exact commits; it cannot inject
  an arbitrary checkout ref.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)
