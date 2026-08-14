---
participant-id: agent:codex
participant: codex
role: agent
ticket: ticket-005
---
# Participant: codex (AI agent)

## Understanding

Hosted CI still checks out only DSL revision `550e5f…`, while ticket-002 moves
the manifest to the immutable `b7d059…` contract. The same exact-schema
dispatch boundary already used by the Docker image must exist before checkout
in CI, otherwise the required `test` check can never validate the migration.

## Execution plan

1. Commit the exact intent before implementation.
2. Resolve the manifest schema through a two-entry SHA allowlist.
3. Feed only the resolved exact commit to `actions/checkout`.
4. Validate syntax, governance and both supported resolution cases.

## Actual changes

- Initialized the bounded ticket and recorded SESSION_EXECUTION_AUTHORIZATION
  from the request to execute this work.
- Added a pre-checkout resolver that maps the two supported immutable schema
  URIs to exact DSL commits and rejects every other value.
- Passed only the allowlisted output to the external `actions/checkout` ref.
- Parsed the workflow and exercised the actual resolver block against both
  coordinated manifests.

## Blockers

- None inside the recorded intent; proceed without a second confirmation.
- New authority remains required for destructive action, secret access, new
  external coordination, material objective expansion and trusted merge.
