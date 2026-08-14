# Project roadmap

- [ ] [`ticket-003`](project/ticket-003/README.md) — make the required Docker
  conformance checker migration-safe for the exact old and new DSL revisions.
  State: `IN_PROGRESS / EDIT`; workstream: `infrastructure`; coordinates
  ticket-002 without taking ownership of its manifest.

- [x] [`ticket-001`](project/ticket-001/README.md) — define and locally validate the initial deployment
  DSL, strict schema, adoption guidance, architecture, and conformance binding.
  `ifuri-validator-agent` approved and merged
  `0da06a6dd7bb7e4934c39ef492f1fafba16969b6`.
- [ ] Add executor-specific mapping profiles only after the neutral contract is
  reviewed; adapters must not redefine authority or outcome semantics.
- [ ] Add a stable release after the first contract PR is independently
  approved and merged.
