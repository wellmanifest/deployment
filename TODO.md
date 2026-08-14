# Project roadmap

- [x] [`ticket-005`](project/ticket-005/README.md) — select the hosted CI DSL
  checkout from an exact schema-to-SHA allowlist. Published by exact-head
  Validator approval; ticket-002 subsequently passed the current-checker path
  and reached protected `main`.
- [x] [`ticket-004`](project/ticket-004/README.md) — route every Compose
  conformance run through the image's exact-schema dispatcher. Published by
  exact-head Validator App approval and protected merge; both coordinated
  immutable manifest revisions pass through the isolated Compose service.
- [x] [`ticket-003`](project/ticket-003/README.md) — make the required Docker
  conformance checker migration-safe for the exact old and new DSL revisions.
  Published through exact-head Validator App approval and protected merge;
  the slice coordinates ticket-002 without taking ownership of its manifest.
- [x] [`ticket-002`](project/ticket-002/README.md) — restore current DSL
  manifest conformance and immutable shared-standard provenance without
  changing deployment semantics. Published by exact-head Validator approval
  and protected merge after all DSL, governance and Docker gates passed.

- [x] [`ticket-001`](project/ticket-001/README.md) — define and locally validate the initial deployment
  DSL, strict schema, adoption guidance, architecture, and conformance binding.
  `ifuri-validator-agent` approved and merged
  `0da06a6dd7bb7e4934c39ef492f1fafba16969b6`.
- [ ] Add executor-specific mapping profiles only after the neutral contract is
  reviewed; adapters must not redefine authority or outcome semantics.
- [ ] Add a stable release after the first contract PR is independently
  approved and merged.
