# Ticket 001: Define reusable deployment DSL

- **ID**: ticket-001
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-08-11

## Goal and scope

Create the first reusable deployment contract conforming to
`wellmanifest.dsl/manifest/v1`. The result is guidance plus a strict JSON DSL
that projects can adopt independently of their executor.

The contract incorporates two complementary bodies of experience:

- Subactor's exact source-to-binding boundary, stale-plan invalidation,
  external grants, content fingerprints, Digital Twin isolation, and explicit
  rollback failure states;
- `semcod/redeploy`'s detect/plan/apply flow and its atomic, blue/green, canary,
  and rollback-on-failure rollout patterns.

The language remains neutral: `redeploy`, an orchestrator, a connector, or a
CI system may implement an adapter, but none may replace the external authority
contract or weaken verification and outcome semantics.

Implementation is limited to five files: a strict canonical schema, its DSL
manifest, the required command page, and two visual architecture documents.

## Acceptance criteria

- [ ] AC-01: `wellmanifest.deployment/v1` is a closed Draft 2020-12 schema with
  at least one schema-valid canonical example.
- [ ] AC-02: Source revision/digest and target binding/digest are exact,
  credential values and raw target coordinates are excluded, and unknown
  fields fail closed.
- [ ] AC-03: The lifecycle separates discover, preflight, plan, authorize,
  apply, verify, rollback, and receipt, binding authority to the exact plan and
  invalidating stale approvals.
- [ ] AC-04: Strategies cover atomic release, blue/green, canary, and rolling
  behavior while preserving common verification and rollback invariants.
- [ ] AC-05: Outcomes distinguish verified success, applied-but-unverified,
  rollback, rollback failure, denial, and human escalation; HTTP 200 alone is
  not sufficient verification.
- [ ] AC-06: `docs/DEPLOYMENT.md` is both an adoption guide and a complete
  command help page; architecture and logic-flow documents contain Mermaid
  diagrams.
- [ ] AC-07: `dsl-manifest.json`, the local `../dsl` validator, Draft 2020-12
  metaschema, governance, Docker build, and networkless conformance all pass.

## Participants

- Human participant: unresolved; no user-* file was created by this script.
- Agent participant: [ai-codex.md](ai-codex.md)

## Non-goals

- Implementing or replacing a deployment engine.
- Storing hostnames, docroots, usernames, passwords, tokens, or private keys in
  the deployment definition.
- Granting an LLM or executor authority through the DSL document.
- Running a production deployment or merging without independent current-head
  approval.
