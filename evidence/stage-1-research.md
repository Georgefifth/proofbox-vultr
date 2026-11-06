# Stage 1 Research — Vultr: Agent Rush Hackathon 2026

## 0. Hackathon Context & Verified Technical Baseline

### Official Challenge Rules (Facts)
- **Event**: [Vultr: Agent Rush Hackathon](https://lablab.ai/ai-hackathons/vultr-hackathon) (Nov 3–8, 2026; $14,000 competition prize pool + onsite raffle).
- **Two Official Tracks**:
  1. **Challenge 01 — Blast Radius Zero (Containment-First Agent Execution)**:
     - Build a web-based agent that performs real work—writing/running code (**Pattern A**) and/or operating a real browser with Playwright (**Pattern B**)—while every action stays inside an isolated sandbox running on Vultr.
     - **Mandatory Stack**: Vultr Cloud Compute VM backend + Web App deployed on Vultr + **Vultr Serverless Inference (`https://api.vultrinference.com/v1`)** + Isolated Sandbox execution.
     - **Mandatory Security & Containment Controls**:
       1. *Process isolation*: Execution never touches the host or app runtime.
       2. *Secret hygiene*: No API keys or credentials inside the sandbox.
       3. *Resource limits*: Apply time, CPU, and memory caps to every run.
       4. *Lifecycle discipline*: Reset or destroy the sandbox environment after each task.
       5. *Mandatory Demo Moment*: At least one **containment moment** (blocking or containing a dangerous/unauthorized action while preserving host integrity) must be demonstrated in the video.
  2. **Challenge 02 — Powering the Future of Work**:
     - Enterprise multi-step AI workflow platform (Sales Ops, Finance, HR, Support, Procurement) deployed on Vultr Cloud Compute.

### Live Vultr API & Serverless Inference Verification (Measured Facts, Nov 6, 2026)
- **`GET https://api.vultrinference.com/v1/models`**: Verified live, returning **35 active models**, including:
  - **Reasoning / Coding / Multimodal Models**:
    - `deepseek-v4.1-flash-1017` (text, image, file -> text; measured latency **1.31s**, native `reasoning` trace + OpenAI Function/Tool Calling verified).
    - `glm-5.3-flash` (text, image, file, video -> text; measured latency **1.34s**, clean JSON + OpenAI Tool Calling verified).
    - `qwen3.8-27b` & `qwen3.8-flash-next` (text, image, file, video -> text; measured latency **1.64s–1.80s**, native `reasoning` + OpenAI Tool Calling + visual inspection verified).
    - `mimo-v2.6-flash` / `mimo-v2.6-pro` (multimodal text/image/audio/video -> text; measured latency **1.25s**).
  - **Native Security & Decision Models**:
    - `nemotron-3.5-content-safety` (text, image, file -> safety classification; measured latency **1.40s**, outputs structured safety verdicts).
    - `clef`, `clef-flash`, `d3`, `pplx-decider-v1.2` (decision models).
- **Vultr Cloud API v2 (`https://api.vultr.com/v2`)**:
  - Account API key present; requires adding current egress IPv4 (`219.92.205.86/32`) or enabling `Allow All IPv4` in Vultr Console (`Account -> API -> Access Control`) so our automation can provision and manage the Vultr VM directly via API.

---

## 1. Phase 1 — Market Exploration & Existing Solutions Analysis

We investigated current developer tools, open-source agent sandboxes, browser automation platforms, and user pain points across GitHub Issues and developer communities:

1. **[E2B (`e2b-dev/E2B`)](https://github.com/e2b-dev/e2b)** (14.7k GitHub stars, Apache-2.0)
   - **What it does**: Cloud Firecracker microVM SDK (`@e2b/code-interpreter`, `@e2b/desktop`) for running AI-generated code.
   - **Real Limitations & User Pain**:
     - Primarily an infrastructure SDK (`Sandbox.create()`), not an end-user verifiable workspace.
     - Self-hosting (`e2b-dev/runtime`) requires complex Terraform + Nomad/Consul cluster orchestration on AWS/GCP, making single-VM self-hosting on independent cloud providers like Vultr notoriously difficult (see GitHub issues around single-node deployment and custom image build latency).
     - Does not provide built-in **Execution Proof Receipts** (cryptographic hashes of inputs/outputs, blocked syscall/network telemetry, or pre-flight LLM safety gating).

2. **[OpenSandbox (`opensandbox-group/OpenSandbox`)](https://github.com/opensandbox-group/OpenSandbox)** (16.5k GitHub stars, Apache-2.0)
   - **What it does**: AAIF sandbox runtime supporting Docker locally and Kubernetes in clusters, with a Credential Vault and egress policy controls.
   - **Real Limitations & User Pain**:
     - Focused on low-level runtime APIs (`osb` CLI / SDK) rather than a task-level verification workflow.
     - As noted in their own README ([Issue #2463](https://github.com/opensandbox-group/OpenSandbox/issues/2463)), umbrella releases currently have a tracked signing and provenance gap for verification evidence.

3. **[Microsandbox (`superradcompany/microsandbox`)](https://github.com/superradcompany/microsandbox)** (9.0k GitHub stars, Apache-2.0)
   - **What it does**: Local-first `msb` CLI and SDK for spawning microVMs with KVM.
   - **Real Limitations & User Pain**:
     - Explicitly warns in its README that it is beta software requiring nested KVM (`/dev/kvm`), which is often restricted or slower on standard cloud compute VMs compared to hardened rootless/unprivileged Docker containers with seccomp/network namespaces.
     - No web control plane, no visual browser verification pipeline, and no audit receipts for non-infrastructure users.

4. **[Browser Use (`browser-use/browser-use`)](https://github.com/browser-use/browser-use)** (120.2k GitHub stars, MIT)
   - **What it does**: Python library and hosted cloud for LLM browser automation via Playwright/CDP.
   - **Real Limitations & User Pain**:
     - In standard self-hosted setups (`uv run agent.py`), the agent drives a local browser or runs `Bash` directly on the SDK host (`Bash runs on the SDK host` per their architecture diagram), exposing host files and environment variables if prompt-injected by a malicious webpage.
     - Lacks deterministic network/secret containment reporting and unified code + browser execution receipts.

5. **[OpenHands (`OpenHands/OpenHands`)](https://github.com/OpenHands/OpenHands)** (92.8k GitHub stars, MIT)
   - **What it does**: Self-hosted coding agent control center (Agent Canvas) with optional Docker conversation runtime.
   - **Real Limitations & User Pain**:
     - Quickstart Option 1 & Option 4 run directly on the host with full filesystem access; even with Docker runtime, containers mount host workspaces and focus on interactive chat rather than zero-trust ephemeral task execution with tamper-evident execution proofs and containment telemetry.

---

## 2. Phase 2 — Candidate Directions (6 Distinct Product Concepts)

We evaluate 6 distinct candidate directions tailored to the hackathon tracks, separating **Verified Facts**, **Reasonable Inferences**, and **Unverified Assumptions**.

---

### Candidate 1: **ProofBox (AegisZero)** — Containment-First Dual-Engine Agent Workspace with Cryptographic Execution Receipts (Track 01: Blast Radius Zero)

- **Target Users & Specific Pain Point**:
  - AI engineers, data analysts, and security-conscious teams who want an AI agent to analyze untrusted files (CSVs, logs, scripts), build charts, or scrape/inspect live websites via Playwright, **without** risking host compromise, credential exfiltration (`os.environ`, `~/.ssh`, cloud metadata `169.254.169.254`), runaway CPU/RAM loops, or hallucinated "I ran it" claims.
- **How Users Currently Solve This**:
  - Either run coding/browser agents directly on their machine/server (high blast radius), pay for hosted black-box sandboxes (E2B Cloud / Browser Use Cloud), or manually write `docker run --rm --network none` scripts without agentic retry loops or visual verification.
- **Related Existing Products**:
  - [E2B (`e2b-dev/E2B`)](https://github.com/e2b-dev/e2b)
  - [OpenHands (`OpenHands/OpenHands`)](https://github.com/OpenHands/OpenHands)
  - [Browser Use (`browser-use/browser-use`)](https://github.com/browser-use/browser-use)
- **Shortcomings of Existing Solutions & Evidence**:
  - Existing agent UIs show a chat bubble claiming a task succeeded, but provide **no verifiable execution proof** (container ID, cgroup peak memory/CPU, exit code, SHA-256 artifact hashes, step-by-step Playwright screenshots, and blocked security events) and rarely combine **Pattern A (Sandboxed Python Code Execution)** and **Pattern B (Sandboxed Playwright Browser Automation)** under a single containment-first control plane on a standard cloud VM.
- **Our Concrete Improvements**:
  1. **Dual-Engine Ephemeral Sandboxes (Code + Browser)**: Every task spawns a fresh, unprivileged Docker container (`--cap-drop=ALL`, `--security-opt=no-new-privileges`, `--read-only` rootfs with bounded `/tmp` tmpfs, `--pids-limit 64`, `--memory 512m`, `--cpus 1.0`, zero host env/secret passthrough, and strict network/SSRF firewall blocking RFC1918 + `169.254.169.254`) and destroys it immediately after execution (`cleanup_verified: true`).
  2. **Multi-Model Vultr Serverless Inference Pipeline**:
     - **Pre-Flight Security Gate**: Uses `nemotron-3.5-content-safety` + deterministic AST/syscall policy scanner before container dispatch.
     - **Task Planner & Self-HealingCoder/Browser Driver**: Uses `deepseek-v4.1-flash-1017` / `glm-5.3-flash` with automatic error-feedback retry if code throws an exception.
     - **Visual & Output Verifier**: Uses multimodal `qwen3.8-27b` to verify Playwright screenshots and generated charts/CSV outputs against the user's goal.
  3. **Verifiable Execution Proof Receipt (`ProofReceipt`)**: Every task generates an inspectable, downloadable JSON/visual receipt containing Container ID, lifecycle timestamps (`spawned_at` -> `destroyed_at`), CPU/Memory telemetry, SHA-256 hashes of all inputs/outputs/screenshots, Security Events (blocked secret reads, blocked SSRF, killed fork bombs/timeouts), and LLM verification verdict.
  4. **Interactive "Blast Radius Simulator / Red-Team Lab"**: Built-in 1-click benign + adversarial test scenarios (e.g., *CSV Revenue & Cohort Chart Generator*, *Live Web QA & Price Extractor*, vs. *Secret Exfiltration Attempt*, *Cloud Metadata SSRF Probe*, *Memory/Fork Bomb*) so users and judges can immediately witness real execution AND real containment in action.
- **Why Users Would Switch**:
  - Deploys on a single $24–$48/mo Vultr VM via one command, requires zero Kubernetes/Nomad complexity, proves every output with cryptographic & visual receipts, and guarantees zero secret leakage.
- **Development Difficulty, Risks & Feasibility**:
  - **Difficulty**: Medium-High.
  - **Risks**: Playwright inside locked-down Docker needs proper `/dev/shm` sizing (`--shm-size=256m`) and seccomp compatibility so Chromium doesn't crash while still remaining unprivileged.
  - **Feasibility**: Very High — we can build and verify the hardened Python + Playwright sandbox images directly on the Vultr VM.
- **MVP & Verification Method**:
  - Web workspace deployed on Vultr VM with: (1) Custom & preset task runner (CSV upload / Python analysis / Playwright web inspection), (2) Real-time 6-stage containment pipeline monitor, (3) Execution Proof Receipt inspector with artifacts/screenshots/SHA-256 hashes, and (4) Live Containment Red-Team Demo suite.
- **Fact / Inference / Assumption Breakdown**:
  - *Fact*: Challenge 01 explicitly asks for Pattern A (Code) and/or Pattern B (Browser), Vultr Serverless Inference, process isolation, secret hygiene, resource limits, lifecycle cleanup, and a containment moment in the video.
  - *Inference*: Combining both Pattern A and Pattern B with an explicit Execution Proof Receipt and live Red-Team Containment Simulator directly hits every judging criterion at maximum depth.
  - *Assumption*: Judges will test both normal analytical/browser tasks and adversarial containment scenarios on the live URL.

---

### Candidate 2: **VultrQA Sentinel** — Sandboxed Autonomous Web QA & Visual Regression Sweeper (Track 01: Blast Radius Zero, Pattern B Focus)

- **Target Users & Specific Pain Point**:
  - Frontend developers and QA engineers who want an AI agent to crawl a staging/production URL, test interactive flows (forms, navigation, responsive layouts), and catch broken links/console errors without running untrusted third-party site scripts on their internal CI runner.
- **How Users Currently Solve This**:
  - Write manual Playwright tests or use hosted SaaS like Checkly / Momentic.
- **Related Existing Products**:
  - [Checkly](https://www.checklyhq.com/)
  - [Browser Use (`browser-use/browser-use`)](https://github.com/browser-use/browser-use)
- **Shortcomings of Existing Solutions & Evidence**:
  - Writing Playwright assertions manually is tedious; hosted AI QA tools cost $200+/mo and don't show container-level isolation proofs when testing untrusted URLs.
- **Our Concrete Improvements**:
  - Ephemeral Playwright container per QA sweep on Vultr + multimodal `qwen3.8-27b` visual bug detection + HAR/console/screenshot proof bundle.
- **Why Users Would Switch**:
  - Zero-config URL sweep with visual AI verification and full network isolation from internal networks.
- **Development Difficulty, Risks & Feasibility**:
  - Medium difficulty; high feasibility.
- **MVP & Verification Method**:
  - Enter any public URL + test goal -> isolated Playwright container runs multi-step inspection -> returns annotated screenshots, console/network errors, and containment proof.
- **Fact / Inference / Assumption Breakdown**:
  - *Fact*: "Site QA Sweep" is listed as an example direction in Challenge 01.
  - *Inference*: Narrowing solely to Pattern B (Browser) is simpler than dual-engine, but showcases less of Pattern A (code execution/data analysis).
  - *Assumption*: Target websites tested by judges won't block datacenter IPs with Cloudflare CAPTCHAs.

---

### Candidate 3: **DataVault Analyst** — Zero-Trust Sandboxed CSV/Parquet Forensic Analyst & Chart Studio (Track 01: Blast Radius Zero, Pattern A Focus)

- **Target Users & Specific Pain Point**:
  - Operations, finance, and data analysts who need Python/Pandas/Matplotlib analysis on messy CSV/Excel/JSON datasets with self-healing code retries, while guaranteeing that the execution container has **zero outbound internet access** (`--network=none`) so sensitive tabular data can never be exfiltrated.
- **How Users Currently Solve This**:
  - Upload spreadsheets to ChatGPT Data Analysis (sending data to OpenAI's cloud) or write Python scripts locally.
- **Related Existing Products**:
  - [OpenAI Code Interpreter / Data Analysis](https://openai.com/)
  - [Julius AI](https://julius.ai/)
- **Shortcomings of Existing Solutions & Evidence**:
  - SaaS data analysts require uploading proprietary files to third-party SaaS without verifiable `--network=none` air-gapped container proofs.
- **Our Concrete Improvements**:
  - Air-gapped ephemeral Docker execution (`--network=none`) on the user's own Vultr VM + automatic self-healing code loop via `deepseek-v4.1-flash-1017` + cryptographic proof that zero bytes left the container over the network.
- **Why Users Would Switch**:
  - Provable air-gapped execution (`network_egress_bytes: 0`) for sensitive datasets.
- **Development Difficulty, Risks & Feasibility**:
  - Low-Medium difficulty; very high feasibility.
- **MVP & Verification Method**:
  - Upload CSV/JSON -> LLM plans & runs Pandas/Matplotlib script in `--network=none` sandbox -> self-heals on schema errors -> outputs downloadable charts, cleaned CSV, and air-gap proof receipt.
- **Fact / Inference / Assumption Breakdown**:
  - *Fact*: "CSV Analyst", "Chart Anything", and "Self-Healing Runner" are official Challenge 01 examples.
  - *Inference*: Very reliable, but a pure CSV tool feels narrower than ProofBox (where air-gapped CSV/Python analysis is already one of the core execution modes).

---

### Candidate 4: **PatchProve** — Self-Healing Code Reviewer & Exploit-Proof Test Runner (Track 01: Blast Radius Zero, Pattern A Focus)

- **Target Users & Specific Pain Point**:
  - Open-source maintainers and backend engineers reviewing untrusted PRs or snippets who want an agent to not just *read* code, but *write unit/fuzz tests, execute the untrusted code in a sandbox, reproduce bugs, and verify the patch*.
- **How Users Currently Solve This**:
  - Static LLM PR reviewers (CodeRabbit, GitHub Copilot) that only comment on diffs without running them.
- **Related Existing Products**:
  - [CodeRabbit](https://www.coderabbit.ai/)
  - [SWE-agent](https://github.com/SWE-agent/SWE-agent)
- **Shortcomings of Existing Solutions & Evidence**:
  - Static LLM code reviewers hallucinate bugs or miss runtime crashes because they never execute the code ("Prove-It Code Reviewer" in the hackathon brief).
- **Our Concrete Improvements**:
  - Runs untrusted code + LLM-generated property/edge-case tests inside a resource-capped container, catches real stack traces, generates a verified patch, and re-runs tests to prove the fix passes.
- **Why Users Would Switch**:
  - Every code review comment comes with an executed stack trace and a verified passing diff.
- **Development Difficulty, Risks & Feasibility**:
  - Medium difficulty; high feasibility for single-file/multi-file Python/JS modules.
- **MVP & Verification Method**:
  - Paste code or repo snippet -> agent generates adversarial/edge tests -> runs in isolated sandbox -> proves failure -> patches code -> proves 100% test pass.

---

### Candidate 5: **ReceiptScout** — Sandboxed Live Research & Price/Vendor Intelligence with Verifiable Web Receipts (Track 01: Blast Radius Zero, Pattern B + A)

- **Target Users & Specific Pain Point**:
  - Procurement analysts and market researchers tired of AI search tools hallucinating prices, specs, or citations without visual proof from the actual webpage.
- **How Users Currently Solve This**:
  - Perplexity / ChatGPT Search, or manual tab-switching and screenshotting.
- **Related Existing Products**:
  - [Perplexity](https://www.perplexity.ai/)
  - [Skyvern (`Skyvern-AI/skyvern`)](https://github.com/Skyvern-AI/skyvern)
- **Shortcomings of Existing Solutions & Evidence**:
  - LLM search summaries frequently cite outdated cached text or hallucinate pricing tiers without timestamped visual screenshots and DOM extraction proofs.
- **Our Concrete Improvements**:
  - Dispatches headless Playwright in a sandbox to target URLs, captures full-page/element screenshots + DOM snapshots, normalizes data via sandboxed Python, and attaches a visual receipt to every table cell.
- **Why Users Would Switch**:
  - Every extracted number/claim is backed by a timestamped Playwright screenshot and DOM selector proof.
- **Development Difficulty, Risks & Feasibility**:
  - Medium difficulty; moderate risk of anti-bot blocks on certain retail sites.

---

### Candidate 6: **ProcureFlow Ledger** — Autonomous Invoice & Vendor Reconciliation Operations Hub (Track 02: Powering the Future of Work)

- **Target Users & Specific Pain Point**:
  - SMB finance & procurement teams manually reconciling PDF/CSV vendor invoices against purchase orders and flagging anomalies or duplicate charges.
- **How Users Currently Solve This**:
  - Spreadsheets, ERP manual entry, or heavyweight enterprise AP tools (Bill.com, Ramp).
- **Related Existing Products**:
  - [Ramp](https://ramp.com/)
  - [Dify (`langgenius/dify`)](https://github.com/langgenius/dify)
- **Shortcomings of Existing Solutions & Evidence**:
  - Generic AI workflow builders lack deterministic math verification and three-way match audit logs.
- **Our Concrete Improvements**:
  - Multi-step agent workflow on Vultr using vision/file models (`glm-5.3` / `qwen3.8-27b`) + Python reconciliation engine.
- **Why Users Would Switch**:
  - Automated three-way match with human-in-the-loop escalation.
- **Development Difficulty, Risks & Feasibility**:
  - Medium difficulty, high feasibility, **but** Track 02 lacks the dramatic technical differentiation of Track 01 ("Blast Radius Zero").

---

## 3. Phase 3 — Critical Review & Elimination (Strict Product Reviewer)

We challenge each candidate against the 6 strict product review questions from `prompts/01-research.md`:

| Candidate | 1. Does it truly need to exist? | 2. Why can't existing tools solve it? | 3. Simpler / non-AI alternative? | 4. Will users try once and abandon? | 5. Evidence our approach is better? | 6. Fatal assumption if wrong? | Reviewer Verdict |
|---|---|---|---|---|---|---|---|
| **1. ProofBox (AegisZero)** | **Yes.** Running AI-generated code & browser actions safely with verifiable execution proofs is the #1 bottleneck in deploying real agents. | E2B/OpenSandbox are low-level SDKs; OpenHands/Browser-Use lack cryptographic execution receipts + built-in pre-flight safety model + containment telemetry UI. | Static Docker scripts can't plan multi-step tasks, self-heal code errors, or visually verify web pages. | **Low abandonment risk**: covers daily tasks (CSV/data analysis, code verification, live web extraction, security auditing) in one workspace. | Uses 3 specialized Vultr Inference models (`nemotron-3.5-content-safety` + `deepseek-v4.1-flash-1017` + `qwen3.8-27b`) + hardened Docker cgroups/network isolation + verifiable SHA-256 receipts. | If container startup + LLM latency exceeds ~15s per run, UX feels sluggish (mitigated via pre-warmed base images & ~1.3s Vultr Flash models). | **KEEP — Top Recommendation** |
| **2. VultrQA Sentinel** | Yes, for staging QA. | Existing AI QA tools are expensive SaaS. | Plain Playwright scripts without AI work for fixed selectors. | Moderate risk if only used for occasional QA sweeps. | Visual verification via `qwen3.8-27b` + isolated browser container. | Many third-party sites block headless browsers with CAPTCHA. | **MERGE** core browser verification capability into ProofBox Pattern B. |
| **3. DataVault Analyst** | Yes, for air-gapped CSV analysis. | Cloud chatbots require uploading data to third-party servers without `--network=none` proof. | Jupyter Notebook locally (if user knows Python). | Low risk for analysts, but narrow for hackathon judges wanting browser + containment demos. | Provable `--network=none` zero-egress container execution + self-healing code loop. | Pure CSV analysis alone doesn't show browser containment. | **MERGE** air-gapped CSV/Chart engine into ProofBox Pattern A. |
| **4. PatchProve** | Yes, for runtime PR verification. | Static AI reviewers don't execute code. | CI pipelines (GitHub Actions) already run existing tests. | Moderate risk unless integrated into GitHub webhooks. | Self-healing test generation + execution proof. | Single-snippet scope is narrow as a standalone web product. | **MERGE** self-healing code runner into ProofBox Pattern A. |
| **5. ReceiptScout** | Partially. | Search engines summarize without visual DOM proof. | Manual browsing. | High risk if target e-commerce sites block datacenter IPs. | Screenshot + DOM receipt per claim. | Anti-bot blocks on retail sites can break live demos. | **ELIMINATE** as standalone; keep verifiable web extraction inside ProofBox. |
| **6. ProcureFlow Ledger** | Yes, in enterprise AP. | ERP systems are rigid. | Deterministic Python/SQL scripts handle 80% of tabular invoice matching. | Judges see dozens of generic "Enterprise AI Dashboards" in Track 02. | Multi-step workflow. | Hard to prove technical superiority over other Track 02 CRUD apps in a 3-minute demo. | **ELIMINATE** — Track 01 has far stronger technical differentiation. |

---

## 4. Phase 4 — Scoring & Comparison Table

Scores (1–10) are grounded in concrete technical and market evidence:

| Candidate Direction | Track | Practical Value (1–10) | Innovation (1–10) | Competitive Edge (1–10) | User Experience (1–10) | Feasibility on Vultr (1–10) | Total (/50) | Recommendation |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **1. ProofBox (AegisZero)** — Dual-Engine Sandboxed Agent Workspace + Execution Proof Receipts + Containment Lab | **01: Blast Radius Zero** | **9.5** (Solves real data/code/web tasks safely) | **9.0** (Multi-model safety gate + cryptographic/visual `ProofReceipt` + live containment red-team lab) | **9.5** (Covers Pattern A + Pattern B + all 4 containment pillars in one cohesive product) | **9.0** (Live 6-stage pipeline + side-by-side output & security proof receipt) | **9.5** (Verified 1.3s Vultr models + hardened Docker sandboxes on Vultr VM) | **46.5** | ⭐ **#1 Strongly Recommended** |
| **3. DataVault Analyst** — Air-Gapped CSV & Chart Studio | 01 (Pattern A) | 8.5 | 7.5 | 8.0 | 8.5 | 9.5 | 42.0 | #2 Backup (or built-in mode of ProofBox) |
| **4. PatchProve** — Prove-It Code Reviewer & Runner | 01 (Pattern A) | 8.5 | 8.0 | 8.0 | 8.0 | 9.0 | 41.5 | #3 Backup (or built-in mode of ProofBox) |
| **2. VultrQA Sentinel** — Sandboxed Browser QA Sweeper | 01 (Pattern B) | 8.0 | 7.5 | 7.5 | 8.0 | 8.5 | 39.5 | #4 Backup (or built-in mode of ProofBox) |
| **5. ReceiptScout** — Web Research with Receipts | 01 (Pattern B) | 7.5 | 7.5 | 7.0 | 7.5 | 7.0 | 36.5 | Eliminate standalone |
| **6. ProcureFlow Ledger** — Enterprise Invoice Ops | 02: Future of Work | 8.0 | 6.5 | 6.0 | 7.5 | 8.5 | 36.5 | Eliminate standalone |

---

## 5. Recommended Direction & Risk Mitigation Plan

### Recommended Product: **ProofBox** (*"Zero-Blast-Radius Agent Execution & Verification Platform on Vultr"*)

Instead of building a narrow single-trick demo, **ProofBox** unifies the three strongest Track 01 workflows under one high-trust execution engine and audit UI:
1. **Mode A — Air-Gapped Code & Data Analyst (`--network=none`)**: Upload CSV/JSON or give a coding/charting/review task -> `deepseek-v4.1-flash-1017` plans & writes Python -> executes in an unprivileged, network-disabled, memory/CPU-capped container -> self-heals on runtime errors -> outputs charts, downloadable artifacts, and a SHA-256 execution receipt.
2. **Mode B — Contained Browser Inspector & QA Agent (`Playwright Sandbox`)**: Give a URL and inspection/extraction goal -> headless Chromium runs inside an isolated container with SSRF/private-IP firewalling -> captures step-by-step screenshots & DOM telemetry -> `qwen3.8-27b` vision model verifies the visual outcome.
3. **Mode C — Live Containment & Red-Team Verification Lab (The Mandatory "Containment Moment")**: Interactive adversarial testbench where users/judges can trigger real agent threat scenarios—*(a) Secret/Env Exfiltration attempt (`os.environ`, `/proc/self/environ`), (b) Cloud Metadata & Internal Network SSRF (`169.254.169.254`), (c) Filesystem Tampering (`rm -rf /etc`), and (d) Resource Exhaustion (Memory/Fork Bomb)*—and watch the **2-Layer Defense** (`nemotron-3.5-content-safety` Pre-Flight Gate + Kernel/Container Runtime Hardening) intercept, contain, log, and cleanly destroy the container with zero impact on the Vultr host.

### Key Risks & Mitigations
1. **Risk**: Vultr Account API v2 rejects requests until the caller IP is whitelisted.
   - *Mitigation*: Whitelist `219.92.205.86/32` (or `Allow All IPv4`) in Vultr Console -> API Access Control so we can provision the Vultr VM via API, or connect via SSH to a user-created Vultr VM.
2. **Risk**: Container cold-start latency during live demos.
   - *Mitigation*: Pre-build and cache the hardened `proofbox-python-sandbox` and `proofbox-playwright-sandbox` Docker images on the Vultr VM so per-task container spawn + teardown takes `< 400ms`.
3. **Risk**: LLM token limit on reasoning models (`deepseek-v4.1-flash-1017` uses reasoning tokens).
   - *Mitigation*: Set `max_tokens >= 1024` for reasoning models and pair with `glm-5.3-flash` / `qwen3.8-27b` with automatic fallback so every step completes in `1.3s–3.5s`.
