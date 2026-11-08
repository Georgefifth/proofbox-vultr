# UX Contract — ProofBox v3 (Focused Containment Workspace)

## 1. Product Positioning
- **One-liner**: A containment-first AI Agent Execution Workspace on Vultr that runs untrusted agent tasks inside disposable sandboxes, blocks host-level attacks, and issues Ed25519-signed Execution Receipts.
- **Three Questions the First Screen Answers Immediately**:
  1. **What can I do?** Run an agent task (or test a malicious prompt-injected agent) inside an isolated Vultr container.
  2. **What did my agent do?** A clean, collapsible **6-Step Execution Timeline** showing each step's status and millisecond duration (`Total: 1.84s`).
  3. **Did it finish safely?** A prominent outcome banner (`ATTACK DETECTED — HOST UNTOUCHED` or `VERIFIED EXECUTION — CONTAINER DESTROYED`) with a 3-tab inspector (**Overview**, **Execution & Diff**, **Security & Ed25519 Proof**).

## 2. Information Architecture (De-Cluttered Layout)

### Top Navigation (3 Clear Destinations)
1. **Workspace** (Default): Run tasks and inspect outcomes without infrastructure clutter.
2. **Red-Team Lab**: Interactive attack testbench (Secret Theft, `/etc/shadow`, Metadata SSRF `169.254.169.254`, 4GB Memory Bomb) with live Host Canary verification.
3. **Developer SDK**: Standalone documentation page (Quick Start, REST API Reference, Python/JS SDKs, Sandbox Lifecycle, Error Handling).

### Workspace Right-Column (3 Focused Tabs — Never Stacked All at Once)
- **Tab 1: Overview (Default)**
  - High-impact Verdict Banner (`ATTACK DETECTED · HOST UNTOUCHED` or `TASK COMPLETED · VERIFIED`)
  - Primary Visual Output (Blocked Attack Evidence Summary, Rendered Chart, or Real Chromium Screenshot)
  - **Deterministic Verification Checks** (Independent math/schema/file assertions — not just LLM claims)
  - Compact **Execution Timeline** (6 steps with status + ms + Total Execution Time; click any step to expand details)
- **Tab 2: Execution & Diff**
  - Executed Sandbox Code (`Edit & Re-Run` supported)
  - **Self-Healing Code Diff** (When Attempt 1 fails: shows Attempt 1 full stderr stack trace, Model Input/Output provenance, and a unified `+/-` diff between Attempt 1 and Attempt 2)
  - Real Container `stdout` / `stderr` terminal output
- **Tab 3: Security & Ed25519 Proof**
  - **Host vs. Sandbox Isolation Proof** (Host Canary Hash before/after, `os.environ` secret check, cgroup peak memory/PIDs, verified container destruction timestamp)
  - **Asymmetric Ed25519 Digital Signature**: Shows the canonical signed payload, the Orchestrator's **Ed25519 Public Key**, the **Ed25519 Signature**, a 1-click signature verifier, and a copyable Python/OpenSSL offline verification snippet.
