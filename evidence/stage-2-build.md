# Stage 2 Build & Competitive Engineering Report — ProofBox on Vultr

## 1. Competitive Product Analysis & Verified Sources

We analyzed 5 direct and indirect competitors in the AI agent sandboxing and browser/code execution space:

| Product | URL | Strengths (What they do well) | Verified Shortcomings | How ProofBox Improves on It |
|---|---|---|---|---|
| **E2B** | [github.com/e2b-dev/e2b](https://github.com/e2b-dev/e2b) | Fast cloud Firecracker microVM SDK (`@e2b/code-interpreter`, `@e2b/desktop`). | Self-hosting requires complex AWS/GCP Terraform + Nomad/Consul cluster orchestration; no built-in pre-flight safety model or signed Execution Proof Receipt UI. | Deploys on a single Vultr Cloud Compute VM (`vc2-4c-8gb`) in 1 command; integrates Vultr `nemotron-3.5-content-safety` pre-flight gate + HMAC-SHA256 `ProofReceipt`. |
| **OpenSandbox** | [github.com/opensandbox-group/OpenSandbox](https://github.com/opensandbox-group/OpenSandbox) | Unified Docker/Kubernetes sandbox API with egress controls. | CLI/SDK developer primitive; umbrella releases have a tracked provenance/signing gap ([Issue #2463](https://github.com/opensandbox-group/OpenSandbox/issues/2463)). | End-to-end visual workbench with per-task SHA-256 input/code/stdout/artifact hashing and verified container teardown stamps (`cleanupVerified: true`). |
| **Microsandbox** | [github.com/superradcompany/microsandbox](https://github.com/superradcompany/microsandbox) | Local-first microVM CLI (`msb`). | Beta software requiring nested KVM (`/dev/kvm`); no web control plane or multimodal output verifier. | Uses portable unprivileged Docker containers (`--cap-drop=ALL`, `--security-opt=no-new-privileges`, `uid=65534`, `cgroupv2`, `netns`) + `qwen3.8-27b` output verification. |
| **Browser Use** | [github.com/browser-use/browser-use](https://github.com/browser-use/browser-use) | 120k+ star browser automation library. | Standard local/SDK mode runs Bash on the SDK host and lacks built-in RFC1918 / `169.254.169.254` SSRF guard receipts. | Enforces strict pre-flight + runtime SSRF guard blocking `169.254.0.0/16` and private subnets before and during browser container execution. |
| **OpenHands** | [github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | Feature-rich coding agent canvas. | Default local quickstarts mount host workspaces; chat-centric UI rather than zero-trust task receipts. | Zero-secret ephemeral container per task (`secretsInjected: 0`) with interactive Red-Team Containment Matrix. |

---

## 2. Prioritized Product & Engineering Plan Executed

1. **P0 — Multi-Model Vultr Serverless Inference Pipeline (`backend/server.py`)**:
   - **Stage 1 (Pre-Flight Safety Gate)**: Live calls to `nemotron-3.5-content-safety` (`https://api.vultrinference.com/v1/chat/completions`) combined with static AST/policy scanning.
   - **Stage 2 & 4 (Planner & Self-Healing Loop)**: Live calls to `deepseek-v4.1-flash-1017` / `glm-5.3-flash` with automatic error-feedback self-healing.
   - **Stage 5 (Output & Visual Verifier)**: Live calls to `qwen3.8-27b` (`max_tokens=700`, filtering out internal reasoning tokens so only clean final verification verdicts are displayed).
2. **P0 — Hardened Ephemeral Docker Sandbox Engine (`run_in_ephemeral_docker`)**:
   - Enforces `--network=none` (Pattern A & C), `--cap-drop=ALL`, `--security-opt=no-new-privileges`, `--read-only` rootfs with `64m` `noexec,nosuid` `/tmp` tmpfs, `--pids-limit=64`, `--memory=256m/512m`, `--cpus=1.0`, and `--user=65534:65534` (`nobody`).
   - Passes zero host secret environment variables (`secretsInjected: 0`).
   - Always executes `docker rm -f <container_id>` followed by `docker inspect <container_id>` to verify `cleanupVerified == True`.
3. **P0 — Forensic Containment Workbench UX (`design/UX.md`, `src/App.tsx`, `src/styles.css`)**:
   - High-density clean-room telemetry aesthetic (`#090B0E` carbon obsidian + `#10141B` instrument slate + `#10B981` forensic emerald + `#F59E0B` containment amber).
   - 3 focused views (`1. Sandbox Workbench`, `2. Red-Team Containment Matrix`, `3. Audit Ledger`), each with a single primary action.
   - All required states implemented and screenshot-verified at 1440px desktop and 390px mobile.

---

## 3. Before vs. After Optimization Metrics & Verification Results

| Metric / Capability | Baseline (Before Optimization / Typical Agent Demo) | After ProofBox Implementation (Verified) | Evidence |
|---|---|---|---|
| **Steps from Landing to Verified Execution Receipt** | 5+ steps (configure env, write script, run CLI, inspect logs manually) | **1–2 clicks** (Select preset or type prompt → Click `Dispatch to Isolated Sandbox`) | `evidence/stage-2-build/frontend/01-desktop-workbench-verified.png` |
| **Host Secret Exposure Inside Container (`os.environ`)** | Full host `.env` exposed in standard agent runners | **0 secrets exposed** (`VULTR_API_KEY present: False` verified in live container) | `backend/test_backend.py::test_redteam_containment_probe` (PASSED) |
| **Cloud Metadata SSRF Protection (`169.254.169.254`)** | Vulnerable to SSRF credential theft | **100% Blocked** (HTTP 400 SSRF Guard in Browser Mode + `Errno 101 Network is unreachable` in `--network=none` Code Mode) | `backend/test_backend.py::test_browser_sandbox_ssrf_guard_blocks_metadata_and_loopback` (PASSED) |
| **Container Teardown & Lifecycle Verification** | Lingering containers or unverified cleanup | **100% Verified Teardown** (`docker rm -f` + `docker inspect != 0` sealed into HMAC-SHA256 receipt) | `evidence/stage-2-build/frontend/07-deployed-vultr-live-execution.png` |
| **Mobile 390px Horizontal Overflow** | Stage cards clipped in 2-col narrow grid | **0px horizontal overflow** (`scrollWidth <= clientWidth` verified) | `evidence/stage-2-build/frontend/06-mobile-390px.png` |
| **Qwen 3.8 27B Verifier Output Quality** | Raw reasoning chain leaked when `max_tokens=160` | **Crisp 2-sentence verification summary** (`max_tokens=700` + `content`-only extraction) | `evidence/stage-2-build/frontend/07-deployed-vultr-live-execution.png` |

---

## 4. Build, Typecheck & Test Results

- **Frontend Build (`npm run build`)**: Passed (`tsc -b && vite build`, built in `640ms`, 0 errors).
- **Backend Automated Test Suite (`PYTHONPATH=. .venv/bin/pytest backend/test_backend.py -v`)**: **5/5 PASSED**:
  - `test_health_endpoint` — PASSED
  - `test_code_sandbox_execution_and_receipt_verification` — PASSED
  - `test_redteam_containment_probe` — PASSED
  - `test_browser_sandbox_ssrf_guard_blocks_metadata_and_loopback` — PASSED
  - `test_browser_sandbox_public_url_inspection` — PASSED

---

## 5. Deployment & Repository Links

- **Live Public Deployment on Vultr Cloud Compute**: `http://45.32.110.141`
  - **Vultr Instance ID**: `c6a71904-3636-4699-9cf5-0d52beb32d8b`
  - **Plan & Region**: `vc2-4c-8gb` (4 vCPU, 8GB RAM, Ubuntu 24.04 LTS x64), Singapore (`sgp`)
  - **Health Endpoint**: `http://45.32.110.141/api/health` (Verified HTTP 200 OK)
- **Public GitHub Repository**: `https://github.com/Georgefifth/proofbox-vultr`

---

## 6. Known Limitations

- The Browser Sandbox mode uses a lightweight isolated Python DOM & HTTP security header inspector inside the ephemeral container by default for `<1.5s` sub-second container execution and deterministic SSRF filtering, while rendering a structured visual viewport SVG snapshot. Full Chromium GUI streaming is omitted to keep memory footprint under `512MB` per concurrent sandbox run.
