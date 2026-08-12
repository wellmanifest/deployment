# DEPLOYMENT

## Purpose

`DEPLOYMENT` describes how a project may be deployed without embedding a
machine-specific path, raw target coordinates, credentials, or an authorization
decision in the project repository. The canonical representation is a JSON
document conforming to `wellmanifest.deployment/v1`.

The language standardizes the boundary between a project and any executor. It
does not implement SSH, Plesk, Kubernetes, Docker Compose, a cloud API, or DNS.
Those operations belong to adapters such as `semcod/redeploy`, URI-run
connectors, or platform-native deployment controllers.

Normative terms MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY have their
usual RFC 2119 meaning.

## Syntax

The canonical document is a closed JSON AST. Unknown fields are invalid. This
compact notation is an explanatory projection; JSON remains authoritative:

```deployment
DEPLOYMENT {
  schema: wellmanifest.deployment/v1
  id: docs.production
  version: 1.0.0
  environment: production

  source: exact repository + revision + artifactDigest + entrypoint
  target: exact bindingRef + bindingDigest
  strategy: immutable release + atomic | blue-green | canary | rolling
  preflight: capability checks + isolated twin + dry-run + planHash
  authority: external single-use grant bound to exact planHash
  apply: executor adapter + capabilities + idempotency + attempt budget
  verify: origin + public + source content digest
  rollback: activate previous release + verify + escalate on failure
  secrets: opaque executor-vault references only
  receipt: exact input hash + redacted evidence + typed outcome
}
```

The authoritative field constraints are in
[`../schemas/deployment.schema.json`](../schemas/deployment.schema.json). The
schema includes canonical atomic and canary examples.

### Core invariants

`deploy-source-exact`
: `source.revision` is a full immutable Git revision and `artifactDigest` binds
  the bytes selected by `source.ref`. An executor MUST resolve the logical ref
  in a trusted local inventory and MUST reject another physical source path.

`deploy-target-exact`
: `target.bindingRef` and `bindingDigest` form one atomic source-to-destination
  decision. A project MUST NOT replace them with a free-form host, domain,
  docroot, namespace, or username. The executor independently loads the same
  binding and compares its digest before planning and again before apply.

`deploy-plan-current`
: Dry-run produces a canonical plan and SHA-256 `planHash`. A change to the
  source revision/digest, binding ref/digest, strategy, checks, secret scope, or
  executor capability set invalidates the plan, grant, and prior approval.

`deploy-authority-external`
: The definition, an LLM, a planner, and an executor cannot mint deployment
  authority. Apply requires a single-use external grant bound to the exact
  current `planHash`. A dry-run, form submission, pull-request merge, or healthy
  credential integration is not that grant unless the external authority
  contract explicitly says so.

`deploy-release-based`
: Mutable synchronization directly into the active destination is not a
  conforming production strategy. Upload or construct an immutable release,
  verify it, and activate it atomically or through an explicit rollout strategy.

`deploy-verify-content`
: HTTP 200 or process liveness alone MUST NOT produce `verified`. Origin and
  public checks run separately, and the selected entrypoint must match the
  source SHA-256. A successful apply followed by failed or stale verification
  yields `applied_unverified`.

`deploy-rollback-honest`
: Content rollback activates the previous release and is itself verified.
  Success yields `rolled_back`, never `verified`. Exhausted or failed rollback
  yields `rollback_failed` or `needs_human`; it MUST NOT be rewritten as a
  successful deployment. DNS/boundary rollback remains a separate human-only
  decision.

`deploy-secrets-opaque`
: Only opaque names, references, and scopes may appear in the document. Secret
  values are resolved in executor-owned Vault and redacted from plans, logs,
  findings, and receipts.

## Inputs

A conforming definition supplies:

| Input | Required meaning |
| --- | --- |
| `id`, `version`, `environment` | Stable identity, SemVer contract version, and explicit lifecycle environment. |
| `source` | Logical source ref plus repository, exact revision, byte digest, and repository-relative verification entrypoint. |
| `target` | Logical deployment binding and SHA-256 of its exact versioned record. |
| `strategy` | Immutable-release rollout type, health stabilization, availability bound, and failure behavior. |
| `preflight` | Named deterministic checks, isolated Digital Twin posture, fail-closed dry-run, and SHA-256 plan hashing. |
| `authority` | External issuer and mandatory exact, fresh, single-use plan binding. |
| `apply` | Adapter identity, required capabilities, idempotency policy, timeout, and retry budget. |
| `verify` | Origin and public probes plus source-content identity; HTTP status alone is explicitly insufficient. |
| `rollback` | Previous-release activation, triggers, retry budget, post-rollback verification, and human escalation. |
| `secrets` | Executor-Vault resolution and optional opaque scoped references; values are forbidden. |
| `receipt` | Required non-secret result contract and complete typed outcome vocabulary. |

Target bindings SHOULD be stored in a separate, versioned, non-secret registry.
A binding may contain provider-specific domain, webspace, namespace, remote path,
or credential references, but project deployment definitions address the whole
record only through `bindingRef` plus `bindingDigest`.

### Strategy rules

- `atomic` switches from the previous immutable release to the candidate as one
  activation step and requires `maxUnavailablePercent: 0`.
- `blue-green` prepares the inactive color, verifies it, switches routing, and
  retains the previous color as rollback target.
- `canary` requires strictly increasing, unique `stages` ending at `100`. Every
  stage must satisfy the same stabilization and verification policy before the
  next stage.
- `rolling` replaces bounded portions while honoring
  `maxUnavailablePercent`; it does not waive exact source identity or rollback.

The schema validates range and structural requirements. A deterministic adapter
MUST additionally check semantic ordering of canary stages and declared
capability availability.

## Outputs

Planning produces a canonical non-secret plan with an exact `inputHash` and
`planHash`. Execution produces a receipt conforming to
`wellmanifest.deployment-receipt/v1`. The receipt SHOULD include the definition
ID/version, source and binding digests, plan hash, external grant identity,
executor/adapter version, per-stage evidence, activated release, previous
release, verification evidence digests, timestamps, and final outcome.

The only allowed final outcomes are:

| Outcome | Meaning |
| --- | --- |
| `verified` | Apply completed and every required origin, public, and content check passed for the exact candidate. |
| `denied` | External authority or exact-plan binding rejected apply before mutation. |
| `preflight_failed` | Required binding, source, capability, twin, or dry-run evidence was absent or red. |
| `applied_unverified` | Mutation happened, but required verification did not prove the candidate. |
| `rolled_back` | Previous release was restored and rollback verification passed; overall deployment remains unsuccessful. |
| `rollback_failed` | Compensation was attempted but could not be completed or verified. |
| `needs_human` | Safe automated progress ended and an authorized human must decide the next action. |

The receipt MUST retain `ok: false` semantics for every outcome except
`verified`, even if rollback itself succeeded.

## Errors

Implementations SHOULD expose stable adapter-specific error codes while mapping
them to the outcomes above. At minimum they must distinguish invalid schema,
unknown fields, stale source, stale binding, missing capability, unevaluable
preflight, stale plan hash, missing/invalid grant, apply failure, origin/public
verification failure, content mismatch, rollback failure, and secret leakage.

An unevaluable required check fails closed. Errors MUST include a non-secret
reason and evidence reference; they MUST NOT copy credential values or local
absolute paths. No ordinary error code is currently part of the language's
stable public catalog; adapters own their codes and document their mapping.

## Examples

### Project definition

The first `examples` entry in the schema is an atomic production website
release. It demonstrates the important distinction between a logical source and
binding versus environment-specific details:

```json
{
  "$schema": "https://wellmanifest.dev/schemas/deployment/v1",
  "schema": "wellmanifest.deployment/v1",
  "id": "docs.production",
  "version": "1.0.0",
  "environment": "production",
  "source": {
    "ref": "workspace:docs",
    "repository": "https://github.com/example/docs",
    "revision": "1111111111111111111111111111111111111111",
    "artifactDigest": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "entrypoint": "public/index.html"
  },
  "target": {
    "bindingRef": "docs-production",
    "bindingDigest": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
  }
}
```

The shortened fragment is intentionally not a standalone valid document; use
the complete schema example as the copyable baseline.

### Mapping to `redeploy`

A `redeploy` adapter may map `strategy.type` to its existing patterns:

| Deployment DSL | `redeploy` experience reused | Required strengthening at the adapter boundary |
| --- | --- | --- |
| `atomic` | plan/apply plus release activation | Resolve exact binding and activate immutable release, not mutable active-dir sync. |
| `blue-green` | `blue_green` | Bind routing switch and both colors to the plan hash; verify content before and after switch. |
| `canary` | `canary` stages | Require ordered stages, per-stage receipts, and stop/rollback on any red verification. |
| rollback policy | `rollback_on_failure` and step rollback commands | Prefer previous-release activation; report `rolled_back`/`rollback_failed` honestly. |

The adapter MAY consume existing `detect → plan → apply` capabilities, health
checks, timeouts, and retry limits. It MUST NOT accept a raw host from the
project definition, silently enable LLM self-healing during an authorized plan,
or change the plan after the grant. A healed or regenerated plan requires a new
hash and fresh external grant.

### Design provenance

The contract follows the immutable
[`wellmanifest/dsl` kernel](https://github.com/wellmanifest/dsl/tree/550e5f441c709e15f2679c1af151352d1eba2f1e),
reuses rollout patterns from
[`semcod/redeploy`](https://github.com/semcod/redeploy/tree/d9c7dd873cd2cedb6bb082bf2757661f4f3f3da9),
and incorporates the exact-binding and rollback lessons recorded in
[`subactor/platform`](https://github.com/subactor/platform/tree/272fab648a9fb55e54e280fdd895e3f53521dbe2).

