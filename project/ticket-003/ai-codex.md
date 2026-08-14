---
participant-id: agent:codex
participant: codex
role: agent
ticket: ticket-003
---
# Participant: codex (AI agent)

## Understanding

The old Deployment image is internally reproducible but coupled to DSL checker
revision `550e5f…`; ticket-002 correctly adopts `b7d059…`. Replacing the old
checker immediately would make current main invalid. A two-revision selector
is safe only when it keys on exact immutable schema URIs and never retries an
older checker after failure.

## Execution plan

1. Record the exact one-file infrastructure migration and coordination link.
2. Package both checker revisions with verified SHA-256 ADD checksums.
3. Add fail-closed exact-schema dispatch in the container command.
4. Validate old and new manifests independently, then run governance/Docker.

## Actual changes

- Initialized the bounded ticket and recorded SESSION_EXECUTION_AUTHORIZATION
  from the request to execute this work.
- Separated infrastructure ownership from ticket-002's integration-owned
  manifest change instead of widening either write scope.
- Kept `integrationTicket` null because ticket-002 is not yet present on the
  target branch; governance correctly forbids a cross-branch phantom link.
- Added the current `b7d059…` checker beside the compatibility checker, with
  immutable source URLs and exact Docker `ADD --checksum` bindings.
- Added fail-closed dispatch keyed only by the manifest's exact `$schema` URI;
  validation failure is never retried with another checker.
- Preserved the historical checker path used explicitly by `compose.yml`, so
  the infrastructure slice remains independently valid on `main`.
- Verified the old manifest through Compose and the ticket-002 candidate
  through the image dispatcher with networking disabled.
- Verified negative dispatch with an existing third-profile manifest; the
  image rejects its unlisted schema URI with `DSL-MANIFEST-001`.

## Blockers

- None inside the recorded intent; implementation is ready for publication
  review.
- New authority remains required for destructive action, secret access, new
  external coordination, material objective expansion and trusted merge.
