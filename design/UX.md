# UX Contract — ProofBox (Zero-Blast-Radius Agent Execution & Verification Platform)

> Fill this before writing UI code. It is the acceptance contract for the
> frontend: if the implementation does not match this file, the implementation
> is wrong. Keep it short and specific.

## 1. Product

- **One-liner**: Containment-first cloud agent workspace on Vultr that executes untrusted Python code and Playwright browser workflows inside ephemeral isolated sandboxes and issues cryptographic Execution Proof Receipts.
- **Primary user**: AI/Platform Engineers, Data Analysts, and Security Reviewers who need AI agents to execute real code, analyze datasets, or inspect live websites without exposing host credentials, internal networks, or system stability.
- **Job to be done**: Submit a real data analysis, code verification, web inspection, or adversarial red-team task; let Vultr Serverless Inference plan, gate, execute inside an isolated Docker container, self-heal errors, and verify outputs; inspect and export a tamper-evident **Execution Proof Receipt (`ProofReceipt`)**.
- **Core success action**: Click **"Dispatch to Isolated Sandbox"** (or 1-click preset scenario) -> observe the live 6-stage containment pipeline -> inspect the verified artifacts (charts/tables/Playwright screenshots) alongside the cryptographic **Execution Proof Receipt** (Container ID, SHA-256 hashes, cgroup resource telemetry, blocked security events, and verified container destruction).
- **What the user should never have to guess**:
  1. Whether the output was genuinely executed vs. hallucinated by an LLM (proven via Container ID, exit code, stdout/stderr, and SHA-256 artifact hashes).
  2. Whether host secrets or internal networks were exposed (shown explicitly in the Sandbox Policy & Security Event log).
  3. Whether the sandbox container was cleaned up after the run (`DESTROYED` lifecycle badge with exact teardown timestamp).

## 2. Core flow

| # | Step | User action | System feedback | Next step is obvious? |
|---|---|---|---|---|
| 1 | **Select or Author Task** | Choose Execution Engine (`Pattern A: Air-Gapped Python Sandbox`, `Pattern B: Contained Playwright Browser`, or `Pattern C: Red-Team Containment Probe`), optionally attach/select dataset or target URL, or click a 1-click verified scenario preset. | Input composer populates task prompt, sandbox isolation policy badges (`--network=none`, `--cap-drop=ALL`, `Memory: 512MB`, `Zero Secrets`), and active Vultr Serverless Inference models (`nemotron-3.5-content-safety`, `deepseek-v4.1-flash-1017`, `qwen3.8-27b`). | Yes — prominent primary CTA **"Dispatch to Isolated Sandbox (⌘↵)"**. |
| 2 | **Live Contained Execution** | Click **"Dispatch to Isolated Sandbox"**. | The **6-Stage Containment Pipeline** lights up stage-by-stage (`1. Nemotron Safety Gate` → `2. DeepSeek/GLM Planner` → `3. Ephemeral Container Spawn` → `4. Sandboxed Execution & Self-Healing` → `5. Qwen Multimodal Verification` → `6. Container Teardown & Receipt Signing`) with live elapsed ms and container telemetry. | Yes — automatically focuses the Verified Output & Proof Receipt split workbench upon completion. |
| 3 | **Inspect Proof Receipt & Artifacts** | Review executed output (stdout, generated SVG/PNG chart, cleaned CSV, or Playwright browser screenshots) and inspect/download the **Execution Proof Receipt JSON**. | Displays cryptographic SHA-256 receipt fingerprint, cgroup CPU/RAM gauges, Security Events (allowed vs. blocked syscalls/network/env probes), and `Verify Receipt Integrity` button. | Yes — user can verify receipt hash, download signed JSON receipt, or run a Red-Team comparison. |

Target: **≤ 2 steps** and **≤ 15 seconds** from landing to a verified sandbox execution receipt.

## 3. Pages / Views

ProofBox uses a high-density single-screen **Forensic Command Workbench** with 3 focused workspace modes in the top rail (so each view has exactly **one primary action**):

| View | Purpose | Primary action | Secondary actions |
|---|---|---|---|
| **1. Sandbox Workbench (Default Landing)** | Author or pick a task (Python Code/CSV Analysis, Playwright Browser Inspection, or Red-Team Exploit Probe), configure sandbox containment policy, dispatch execution, and inspect the resulting Artifacts + Execution Proof Receipt side-by-side. | **Dispatch to Isolated Sandbox** | Load preset scenario, upload CSV/script, toggle strict air-gap (`--network=none`), inspect generated code/Playwright trace, download signed `ProofReceipt.json`. |
| **2. Red-Team Containment Matrix** | Run or batch-verify adversarial security probes (Secret Exfiltration, Cloud Metadata SSRF `169.254.169.254`, Filesystem Tampering, Memory/Fork Bomb) to prove Blast Radius Zero containment. | **Run Containment Stress Suite** | Inspect individual blocked attack payloads, compare Pre-Flight Gate (`nemotron-3.5-content-safety`) vs. Runtime Kernel Block (`seccomp`/`cgroups`/`netns`). |
| **3. Audit Ledger & Vultr Telemetry** | Inspect historical Execution Proof Receipts, verify SHA-256 receipt signatures, and view live Vultr Cloud Compute VM & Vultr Serverless Inference latency/model health. | **Verify Selected Receipt Signature** | Filter by status (`VERIFIED`, `CONTAINED_BLOCK`, `SELF_HEALED`), export full audit log JSON, refresh live Vultr infrastructure health. |

## 4. Required states

For every view and interactive component:

- [x] **Empty / first visit**: Actionable starter state in the Receipt panel showing the 4-Pillar Containment Architecture diagram and 1-click quick-start buttons ("Run Air-Gapped CSV Cohort Analysis", "Run Contained Playwright Web QA", "Trigger Secret Exfiltration Block").
- [x] **Loading**: Live 6-stage step tracker with active stage pulse, elapsed millisecond counter, active Vultr model badge, and ephemeral container short-ID.
- [x] **Success (`VERIFIED_EXECUTION` / `CONTAINED_THREAT`)**: Distinct high-contrast status banner; for benign tasks shows verified output + artifacts + green `CONTAINER DESTROYED` badge; for adversarial tasks shows amber/red `THREAT CONTAINED — HOST UNTOUCHED` banner with exact blocked vector.
- [x] **Error**: Explicit error card showing stage of failure, raw stderr/HTTP error code, self-healing retry log, and 1-click **"Retry in Fresh Sandbox"** button.
- [x] **Invalid input**: Inline field validation (e.g., empty prompt, invalid URL format in Browser Mode, or unsupported file size) highlighting the exact field in `#F59E0B` / `#EF4444` with recovery instructions.
- [x] **No permission / Security Policy Blocked**: Explicit **Containment Intervention Notice** when `nemotron-3.5-content-safety` or the sandbox runtime blocks a forbidden action, detailing the policy rule triggered.
- [x] **Mobile 390px layout**: Stacked single-column forensic layout with sticky bottom/inline primary CTA, horizontal scrollable pipeline pills, and zero horizontal page overflow.

## 5. Design tokens

- **Font family and scale**:
  - Sans / UI: `'Space Grotesk', 'IBM Plex Sans', system-ui, sans-serif`
  - Monospace / Telemetry / Receipts: `'JetBrains Mono', 'IBM Plex Mono', monospace`
  - Scale:
    - Display / Workspace Title: `20px` (`1.25rem`), weight `700`, tracking `-0.02em`
    - Section Header: `14px` (`0.875rem`), weight `600`, uppercase tracking `0.06em`
    - Body / Prompt: `14px` (`0.875rem`), line-height `1.5`
    - Technical Telemetry / Code / Hashes: `12px` (`0.75rem`), monospace, tabular-nums
- **Spacing scale**: `4px`, `8px`, `12px`, `16px`, `20px`, `24px`, `32px` (high-density 1px structural hairline grid).
- **Colors (Industrial Clean-Room / Forensic Telemetry Dark Palette)**:
  - Background Primary (Canvas): `#090B0E` (Deep Obsidian Carbon)
  - Background Secondary (Panel Surface): `#10141B` (Instrument Slate)
  - Background Elevated / Code Surface: `#151B24`
  - Structural Hairline Border: `#212936` (1px exposed technical grid)
  - Text Primary: `#F1F5F9` (Crisp Alabaster)
  - Text Muted / Secondary: `#94A3B8` (Slate Technical Label)
  - Accent Primary (Verified / Safe / Active Telemetry): `#10B981` (Forensic Emerald)
  - Accent Secondary (Vultr Infrastructure / Compute): `#0EA5E9` (Cyan Telemetry)
  - Warning / Containment Intercepted: `#F59E0B` (Hazard Amber)
  - Danger / Attack Blocked: `#EF4444` (Containment Crimson)
- **Radius and borders**:
  - Sharp precision radius: `4px` for cards/inputs/buttons, `2px` for status pills.
  - `1px solid #212936` structural borders; active/focused panels use `1px solid #10B981` or `#0EA5E9`. Zero fuzzy drop-shadows.
- **Button and input height**:
  - Primary interactive buttons & inputs: `min-height: 44px` (`padding: 10px 16px`) for accessible touch targets on both desktop and 390px mobile.
- **Icon style and stroke**:
  - Crisp inline SVG geometric icons, `1.75px` stroke width, zero emoji icons anywhere in the UI.

## 6. References

| Reference (URL or screenshot) | What to borrow | What not to copy |
|---|---|---|
| [E2B Sandbox Docs & Dashboard](https://e2b.dev/docs) | Monospace sandbox ID lifecycle tags, stdout/stderr split stream layout | Brand logo, marketing hero layout |
| [OpenSandbox Architecture](https://github.com/opensandbox-group/OpenSandbox) | Egress policy & credential isolation mental model | CLI-only UX |
| Cloudflare Radar / Datadog Security Trace Inspector | Forensic trace waterfall, security rule trigger badges, tabular-nums telemetry strips | Proprietary branding or cluttered multi-level sidebars |

## 7. Mobile (390px)

- **390px layout**:
  - Top bar compacts into a two-row header: Brand + Live Vultr Status badge on row 1; 3-view switcher tabs (`Workbench` / `Red-Team Matrix` / `Audit Ledger`) at full width (`min-height: 44px`) on row 2.
  - Main Workbench stacks vertically:
    1. **Task & Containment Composer** (Mode selector + Scenario quick-chips + Prompt + Policy badges + Full-width `48px`-tall **"Dispatch to Isolated Sandbox"** CTA).
    2. **6-Stage Containment Pipeline Strip** (compact 2x3 grid of stage cards with status icons and ms timings).
    3. **Verified Output & Cryptographic Proof Receipt** (tabbed or collapsible accordion sections so users can inspect Output/Visuals vs. Security Receipt without endless scrolling).
- **Primary action reachable without horizontal scroll**: Yes (`overflow-x: hidden` on root, `100%` width CTA button above fold).
- **What is collapsed or hidden**: Secondary raw JSON payload and verbose container cgroup breakdown collapse into an expandable `"Inspect Raw Signed Receipt JSON"` drawer on `< 768px`.
- **Keyboard behavior**: `⌘+Enter` / `Ctrl+Enter` submits the task; `Esc` resets active modal/inspector.

## 8. Visual direction

- **Three adjectives**: **Forensic, Contained, High-Density**.
- **Product archetype**: **Terminal + Security Telemetry Workbench** (like a clean-room hardware/kernel isolation console combined with a cryptographic receipt inspector).
- **Palette and why it fits the domain**:
  - Carbon obsidian (`#090B0E`) + instrument slate (`#10141B`) with exposed `1px` structural borders (`#212936`), Forensic Emerald (`#10B981`) for verified isolated runs, Hazard Amber (`#F59E0B`) for intercepted threats, and Cyan (`#0EA5E9`) for Vultr Cloud & Inference telemetry. It immediately communicates *zero-trust containment and hardware-grade verification*, never a generic SaaS chatbot.
- **Type pairing (max 2 families)**:
  - `Space Grotesk` for crisp geometric headers and controls.
  - `JetBrains Mono` for container IDs, SHA-256 hashes, syscall policies, resource limits, and code/logs.
- **Density**: **High-density technical workbench** — zero marketing fluff hero section; lands directly inside the live **ProofBox Control Plane** so the user sees the Sandbox Dispatcher, 6-Stage Containment Pipeline, and Execution Proof Receipt immediately on screen 1.
- **Signature element (one thing this product owns)**:
  - **The Dual-Column "6-Stage Containment Pipeline + Cryptographic Execution Proof Receipt (`ProofReceipt`)"** featuring live Container Lifecycle stamps (`SPAWNED` → `ISOLATED` → `VERIFIED` → `DESTROYED`), real cgroup CPU/RAM gauges, blocked threat telemetry, and a verifiable SHA-256 signature seal.
- **Motion rules**:
  - Only functional state transitions animate: active pipeline stage pulse (`150ms`), progress bar fill, and receipt verification checkmark. Never animate background gradients or decorative floating shapes.
- **Rejected clichés**:
  - Explicitly banned: purple/blue background gradients, glassmorphism blur cards, centered 3-column marketing hero, generic sidebar KPI dashboard, emoji icons, and fake unverified metrics.

**Generic test:** Could this first screen be dropped into any other SaaS product without looking out of place? **No** — the exposed 1px containment chamber layout, kernel policy flags (`--cap-drop=ALL`, `--network=none`, `--pids-limit=64`), 6-stage Vultr model pipeline, and SHA-256 Execution Proof Receipt are unmistakable and specific to a zero-blast-radius agent sandbox.

## 9. UX acceptance

- [x] A first-time user can explain the product's purpose within 5 seconds
- [x] The core task is reachable from the landing page without reading docs
- [x] Every action produces visible feedback within 100ms, or a loading state
- [x] Every error says what happened and what to do next
- [x] Empty states are actionable, not blank
- [x] No dead ends; no unlabeled icon-only buttons
- [x] Desktop (1440px) and mobile (390px) screenshots reviewed side by side
- [x] The flow still works after connecting the real backend
