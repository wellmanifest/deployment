# Ticket 011: Standardize zero-trust control bastion and safe upgrades

- **ID**: ticket-011
- **Owner**: human
- **Status**: DONE
- **Workflow state**: DONE
- **Created**: 2026-09-26

## Goal and scope

Standardize zero-trust asymmetric bastion control plane architecture, 5-step zero-downtime safe upgrade pipeline, real-time Koru autonomous remediation, and urirun-mail fail-closed notification patterns in `wellmanifest/deployment`.

## Acceptance criteria

- [x] AC-01: Update `docs/DEPLOYMENT.md` with safe upgrade and zero-trust bastion standards.
- [x] AC-02: Create `docs/ZERO_TRUST_BASTION_AND_KORU_REMEDIATION.md`.
- [x] AC-03: Passes `./project/governance-check.sh`.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.
