# Ticket 002: Restore Deployment DSL manifest conformance

- **ID**: ticket-002
- **Owner**: unresolved:human
- **Status**: DONE
- **Workflow state**: DONE
- **Created**: 2026-08-14

## Goal and scope

Migrate the existing deployment profile to the current published DSL manifest
contract without changing the Deployment DSL schema or effect semantics. Add
the missing document vocabulary, proportional controlled-effects publication
policy, and an immutable lock to the exact shared DSL schema revision.

## Acceptance criteria

- [x] AC-01: The ticket binds the original execution instruction to exact
  `main@852f3f9` and the final post-dependency continuation to exact
  `main@4f211e8`, with one implementation file and zero runtime dependencies.
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
- Ticket-005's exact-schema hosted workflow is merged on protected `main`, so
  CI now selects checker `b7d059…` for this manifest without a mutable ref.
- Hosted `test` and `windows-governance` passed on implementation head
  `d830a7abb7f5d52ec5768962eb2730e30ca50078`; the test included the
  networkless Docker conformance run with the current checker.
- Both required hosted checks passed again on final exact head
  `af3ee4ef65fdacb6c557c0b0db4a431d76e9b84e`.
- Validator run `31840312229` completed successfully and App review
  `4941150838` approved that exact head.
- The Validator App explicitly merged PR #6 as
  `a13b6442545f5db3a6b1790a831641a1b888c7b2`; protected `main` read-back
  returned the merge and the source branch was deleted.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)
