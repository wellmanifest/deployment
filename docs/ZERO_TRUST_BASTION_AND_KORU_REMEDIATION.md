# Zero-Trust Bastion Control Plane and Autonomous Koru Remediation Standard

## 1. Overview and Invariants

This standard defines the production invariants for hosting management control planes (e.g. cluster dashboards, orchestration runners, and deployment controllers) in zero-trust, multi-region environments.

Traditional deployment topologies where management planes share network visibility, bidirectional SSH tunnels, or symmetric API tokens with public edge workers violate fail-closed security. A compromise on any edge worker allows lateral movement directly to the control plane.

### Core Invariants:

1. `bastion-asymmetric-control-push`
   - The Management Control Bastion MUST NOT expose public inbound ports.
   - All management and deployment interactions MUST use outbound-only push vectors (SSH with dedicated, non-interactive Ed25519 keys, or mutual TLS).
   - Worker and edge nodes MUST NOT possess private keys, API tokens, or routable network access to the Bastion.

2. `zero-lateral-movement-boundary`
   - A complete compromise (root shell) on an edge worker node MUST NOT provide credentials or network capability to pivot to the control plane or to any other node in the fleet.

3. `pre-flight-twin-verification`
   - Production deployments MUST execute a pre-flight sandbox check on an isolated Digital Twin before touching live traffic.
   - Confidence score MUST exceed 80% across configuration parsing, database dry-run migration, resource headroom, and canary probe phases.

4. `atomic-dual-snapshot-safety-net`
   - Every stateful deployment MUST generate an atomic dual snapshot (relational PostgreSQL WAL + SQLite metadata) with cryptographic SHA-256 digest before initiating code or container mutations.

5. `post-deployment-synthetic-e2e`
   - Deployments MUST NOT be marked `SUCCESS` based solely on container start or HTTP 200 health checks.
   - Synthetic end-to-end verification MUST execute actual session auth, transactional read/write, and cleanup through live edge domains.

6. `realtime-autonomous-remediation-koru`
   - On confirmed intrusion or tripwire breach, the autonomous controller (Koru) MUST:
     - Shift legitimate traffic away from the compromised node to a twin or static bunker.
     - Isolate the node via firewall (`ufw default deny outgoing`) and freeze untrusted containers (`docker pause`).
     - Destroy poisoned Copy-on-Write (OverlayFS) layers and rebuild from trusted, signed git revisions.

7. `fail-closed-audit-notification`
   - Deployments and security alerts MUST dispatch notifications via `urirun connectors` (`email://approved-recipients/message/command/send`) with verified TLS SMTP fallback.
   - If network delivery fails, alerts MUST be spooled locally in structured JSON with SHA-256 payload integrity (`fail-closed audit spooling`).

---

## 2. Asymmetric Zero-Trust Topology

```
+-------------------------------------------------------------------------+
|                  MANAGEMENT CONTROL BASTION                             |
|                                                                         |
|  - Cluster Panel / Fleet Manager (localhost:8888)                       |
|  - Koru Autonomous Engine (guardian_service, event_bus)                 |
|  - urirun-mail Notification Dispatcher                                  |
|  - Inbound Access: WireGuard / Tailscale / mTLS only                    |
|  - Outbound Push Key: ~/.ssh/id_ed25519 (command-restricted)            |
+------------------------------------+------------------------------------+
                                     |
                Outbound-Only SSH / mTLS Push Control Vector
                                     |
               +---------------------+---------------------+
               |                                           |
               v                                           v
+-----------------------------+             +-----------------------------+
|  EDGE WORKER NODE A         |             |  EDGE WORKER NODE B         |
|  (e.g. Primary Spain)       |             |  (e.g. Secondary Standby)   |
|                             |             |                             |
|  - Reverse Proxy (Caddy)    |             |  - Reverse Proxy (Caddy)    |
|  - Containers (App, API)    |             |  - Containers (App, API)    |
|  - Twinerd Guard (Rust)     |             |  - Twinerd Guard (Rust)     |
|  - Honeypots & CIS Daemon   |             |  - Honeypots & CIS Daemon   |
|                             |             |                             |
|  [!] ZERO Bastion Keys      |             |  [!] ZERO Bastion Keys      |
|  [!] ZERO Lateral Access    |             |  [!] ZERO Lateral Access    |
+-----------------------------+             +-----------------------------+
```

---

## 3. Five-Step Zero-Downtime Safe Upgrade Pipeline

Conforming implementations MUST structure updates into five discrete sequential steps:

1. **Step 1: Digital Twin Pre-Flight Check**
   - Spins up ephemeral isolated container/overlay sandbox.
   - Validates compose environment variable interpolation and syntax.
   - Executes database migration dry-run.
   - Evaluates memory and CPU headroom.
   - Computes Confidence Score (threshold: >= 80%).

2. **Step 2: Pre-Upgrade Safety Net & Tenant WAL Replication**
   - Dumps transactional database states.
   - Archives SQLite state and PostgreSQL WAL logs.
   - Computes SHA-256 fingerprint for forensic and rollback guarantees.
   - Replicates WAL snapshot to secondary immutable offsite storage.

3. **Step 3: Rolling Container Deployment**
   - Synchronizes code assets excluding ephemeral caches (`.worktrees`, `.subactor`, `state/`, `build/`).
   - Builds or pulls immutable container images.
   - Applies rolling update with minimal service disruption.
   - Reloads edge ingress configuration (Caddy/TLS).

4. **Step 4: Post-Deployment Synthetic Live E2E Verification**
   - Probes public DNS resolution for all domain endpoints.
   - Performs synthetic user account creation, session token generation, authenticated API call, database mutation, and cleanup.
   - Verifies 100% pass rate before accepting deployment.

5. **Step 5: Final Cluster Health Assessment & Automated Rollback**
   - If synthetic E2E verification fails, automated rollback triggers:
     - Discards current container state.
     - Restores previous database snapshot and WAL stream.
     - Restarts verified previous containers.
   - Emits structured event and dispatches `urirun-mail` completion report.

---

## 4. Real-Time Attack Defense & Traffic Shifting

### Ingress Tarpits and Rate Limiting
Public ingress reverse proxies MUST inspect traffic patterns. Aggressive probing of administrative endpoints, hidden files (`.env`, `.git`), or known exploit signatures triggers:
- HTTP 429 / tarpit delay (30 seconds artificial response throttle).
- Automatic telemetry emission to the incident event bus.

### Real-Time Dynamic Traffic Shifting
When an intrusion is flagged:
1. `traffic_shifter` issues dynamic configuration change to Caddy/DNS routing.
2. Authenticated user sessions (possessing valid session cookies or Bearer tokens) are rerouted to healthy twin instances or to an unpolluted static maintenance bunker.
3. Attacker traffic is isolated to the quarantined container for observation and forensic capture.

---

## 5. Unified Node Updater Interface (`update-node-remote.sh`)

Standard node update tools MUST expose uniform CLI parameters:
- `--server <id|host>`: Target node identifier or IP.
- `--user <user>`: SSH username (default `root`).
- `--key <path>`: Non-interactive private key path.
- `--target-dir <path>`: Remote deployment directory.
- `--email <address>`: Recipient for status reports.
- `--skip-sync`: Skip file synchronization.
- `--skip-docker`: Skip container rebuild/restart.
- `--skip-doctor`: Skip diagnostics.
- `--dry-run`: Simulation mode.
