# Ticket 014: Add slot-manifest, activation-journal, attempt-singleflight and update-status schemas

- **ID**: ticket-014
- **Owner**: agent:antigravity (`SESSION_EXECUTION_AUTHORIZATION`)
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-19

## Goal and scope

Extend `wellmanifest/deployment` (`ADOPT` contract for `semcod/slotkit`, `heyasa/heyasa`, `heyasa/heyasa-lab`, and `maskservice/bootloader`) with four Draft 2020-12 JSON Schemas, positive/negative canary cases, documentation in `docs/DEPLOYMENT.md`, and exact SHA-256 bindings in `dsl-manifest.json`:
1. `schemas/slot-manifest.schema.json` (`wellmanifest.slot-manifest/v1`)
2. `schemas/activation-journal.schema.json` (`wellmanifest.activation-journal/v1`)
3. `schemas/attempt-singleflight.schema.json` (`wellmanifest.attempt-singleflight/v1`)
4. `schemas/update-status.schema.json` (`wellmanifest.update-status/v1`)

## Acceptance criteria

- [x] AC-01: All four JSON Schemas validate under `Draft202012Validator`, enforce honest rollback (`ok: false` on `rolled-back`), exact 64-hex digests, process startup attestation, and credential-free status fields, and pass all positive/negative cases in `schemas/slotkit.cases.json`.
- [x] AC-02: `dsl-manifest.json` binds exact `sha256:` digests for all owned schema/example/doc artifacts and passes `dsl_check.py validate`, `dsl_check.py changes`, and `./project/governance-check.sh`.
