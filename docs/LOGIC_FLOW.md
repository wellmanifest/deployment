# Deployment DSL logic flow

## Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Discover
    Discover --> Preflight: source binding capabilities resolved
    Discover --> PreflightFailed: unresolved or stale input
    Preflight --> Plan: every required check evaluable and green
    Preflight --> PreflightFailed: red refusal or unknown
    Plan --> Authorize: exact inputHash and planHash emitted
    Authorize --> Denied: missing stale or mismatched grant
    Authorize --> Apply: fresh single-use exact grant
    Apply --> VerifyOrigin: candidate activated
    Apply --> Rollback: apply failed and rollback policy active
    VerifyOrigin --> VerifyPublic: origin evidence green
    VerifyOrigin --> Rollback: origin evidence red
    VerifyPublic --> Verified: public and content evidence green
    VerifyPublic --> AppliedUnverified: public or content evidence red
    AppliedUnverified --> Rollback: rollback policy active
    Rollback --> RolledBack: previous release verified
    Rollback --> RollbackFailed: previous release not restored or not verified
    RollbackFailed --> NeedsHuman
    PreflightFailed --> [*]
    Denied --> [*]
    Verified --> Receipt
    RolledBack --> Receipt
    NeedsHuman --> Receipt
    Receipt --> [*]
```

Only `Verified` is successful. `RolledBack` means compensation succeeded, not
that the requested deployment succeeded.

## Exact-plan authorization

```mermaid
sequenceDiagram
    participant P as Project
    participant R as Resolver
    participant T as Twin and Planner
    participant A as External Authority
    participant E as Executor Adapter
    participant V as Verifier

    P->>R: definition with logical refs and exact digests
    R->>R: resolve source and binding independently
    R->>T: normalized non-secret input
    T->>T: isolated preflight and dry-run
    T-->>P: plan plus inputHash plus planHash
    P->>A: request grant for exact planHash
    A-->>E: single-use grant
    E->>R: re-resolve source binding capabilities
    E->>E: recompute inputHash and planHash
    alt exact and current
        E->>E: create and activate immutable candidate
        E->>V: candidate and source evidence
        V-->>E: origin public content result
    else stale or mismatched
        E-->>P: denied receipt without mutation
    end
```

An executor that repairs, heals, expands, or otherwise changes the plan must
return to `Plan`. The old grant cannot authorize the new candidate.

## Rollout strategies

```mermaid
flowchart TD
    Candidate[Immutable candidate release] --> Strategy{Strategy}
    Strategy -->|atomic| Atomic[Verify candidate then switch once]
    Strategy -->|blue-green| BG[Verify inactive color then switch route]
    Strategy -->|canary| Canary[Promote through declared stages]
    Strategy -->|rolling| Rolling[Replace bounded portions]
    Atomic --> Common[Common origin public content verification]
    BG --> Common
    Canary --> StageVerify[Verify every stage]
    StageVerify --> Common
    Rolling --> StageVerify
    Common -->|green| Verified[verified receipt]
    Common -->|red| Compensate[Activate previous release]
    Compensate -->|verified| RolledBack[rolled_back receipt]
    Compensate -->|failed| Escalate[rollback_failed or needs_human]
```

### Canary invariants

Canary stages are strictly increasing, unique percentages ending at `100`.
Every stage waits at least `minimumHealthySeconds` and runs its declared checks.
A red or unevaluable stage stops promotion and follows `strategy.onFailure`.

### Verification ladder

1. Confirm the exact source and target-binding digests are still current.
2. Confirm the executor exposes every declared capability.
3. Verify the candidate at the origin without relying on public DNS.
4. Verify the public endpoint, TLS where relevant, and service health.
5. Hash the selected public entrypoint and compare it with the source artifact.
6. Emit `verified` only when every required rung is green.

HTTP 200 can satisfy one health assertion; it cannot satisfy content identity.

## Failure routing

```mermaid
flowchart LR
    Failure[Failure or unknown evidence] --> Mutated{Mutation occurred}
    Mutated -->|no| Before[denied or preflight_failed]
    Mutated -->|yes| VerifiedNow{Required verify green}
    VerifiedNow -->|yes| Success[verified]
    VerifiedNow -->|no| Unverified[applied_unverified]
    Unverified --> RollbackAllowed{Rollback configured}
    RollbackAllowed -->|no| Human[needs_human]
    RollbackAllowed -->|yes| Restore[Activate previous release]
    Restore --> RestoreVerify{Rollback verify green}
    RestoreVerify -->|yes| Back[rolled_back]
    RestoreVerify -->|no| Failed[rollback_failed]
    Failed --> Human
```

All terminal paths create a redacted receipt bound to the exact input and plan.
No branch silently converts unknown, refusal, compensation, or partial success
into `verified`.
