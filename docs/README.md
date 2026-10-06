# Deployment contracts

- [Deployment DSL](DEPLOYMENT.md) — executor-neutral deployment contract.
- [Firmware flash backup policy](firmware-flash-policy.json) — canonical rules:
  development flashing forbids device backups; production requires verified
  recovery before any write. Unknown target lifecycle is rejected.
- [Flash admission schema](../schemas/firmware-flash-policy.schema.json) —
  structural checks for independently verified executor observations.
- [Admission canaries](../schemas/firmware-flash-policy.cases.json) — positive
  and negative cases shared by product adapters; no hardware access.

The firmware policy is a candidate, not a published or deployed fleet standard.
Product adapters must pin its published revision and enforce its rules in their
USB and OTA entrypoints. A valid receipt alone does not prove those entrypoints
are wired, and does not authorize flashing.
