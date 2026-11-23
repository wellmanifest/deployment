# Ticket 015: Document adoption of Forge Dockuri and UrtLog deployment operations

- **ID**: ticket-015
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-23

## Goal and scope

Document the optional deployment operation profile based on the live Orin pilot, Forge file snapshots, Dockuri URI dispatch and UrtLog records. Map the profile to the existing redeploy plan/apply boundary.

## Acceptance criteria

- [ ] AC-01: Describe plan, authority, artifact, read-back and receipt binding without making new tools mandatory.
- [ ] AC-02: Identify the exact semcod/redeploy integration points and the first acceptance cases.

## Tracking boundary

This directory contains the minimal reviewed intent. Optional participant prose
and raw command logs are not required delivery output.

<!-- ticket-radar:start -->
## Ticket Radar

Initial planned-scope estimate; advisory only, not execution or merge approval.

| Measure | Initial assessment |
| --- | --- |
| Impact score | 56/100 |
| Complexity | M |
| Estimated effort | 52 min |
| Planning budget | 30 min |
| Split recommended | yes |

Diagnostics: RADAR-ACCEPTANCE-MISSING, RADAR-BUDGET-EXCEEDED.
<!-- ticket-radar:end -->

SESSION_EXECUTION_AUTHORIZATION: The operator requested reuse guidance in the deployment standard explicitly.

The existing DSL manifest pins the documentation bytes. The bounded scope includes refreshing that one documentation digest.
