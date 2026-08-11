# wellmanifest/deployment

Reusable guidance and a strict DSL contract for describing safe deployments
without coupling projects to one deployment engine.

The contract standardizes source identity, target bindings, planning,
authorization, rollout, verification, rollback, and receipts. It incorporates
operational lessons from Subactor and maps proven `semcod/redeploy` patterns
without granting an executor, an LLM, or a DSL document authority to deploy.

## Status

The governed `0.1.0-dev` contract is tracked by
[`project/ticket-001`](project/ticket-001/README.md). Product files are delivered
through its reviewable branch; the default branch contains the governance and
CI bootstrap required to review that change.

## Intended use

1. Read [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for the language and adoption
   rules.
2. Create a `deployment.json` in the adopting project.
3. Validate it against [`schemas/deployment.schema.json`](schemas/deployment.schema.json).
4. Resolve `source.ref` and `target.bindingRef` in the executor's trusted
   inventory; keep credentials outside the document.
5. Run preflight and dry-run, authorize the exact `planHash`, apply, verify, and
   retain a non-secret receipt.

The repository conforms to `wellmanifest/dsl` at immutable revision
`550e5f441c709e15f2679c1af151352d1eba2f1e`. Local development uses the sibling
checkout at `../dsl`; CI and Docker fetch the same byte-exact validator revision.

## Local checks

```bash
../dsl/src/dsl_check.py validate --root . dsl-manifest.json
docker compose run --rm conformance
./project/governance-check.sh --actor agent
```

No production deployment is performed by this repository.
