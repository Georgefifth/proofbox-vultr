# Submission Fields — ProofBox (Vultr: Agent Rush Hackathon 2026)

## Project name

ProofBox — Zero-Blast-Radius Agent Sandbox on Vultr

## Elevator pitch / Short description (176 characters)

Containment-first agent execution platform on Vultr Cloud Compute & Serverless Inference that runs untrusted code and web tasks in ephemeral sandboxes with Ed25519 receipts.

## Thumbnail / Cover Image

- **3:2 Thumbnail (1500x1000 PNG, 91 KB)**: `submission/assets/thumbnail.png`
- **16:9 Widescreen Cover (1920x1080 PNG, 836 KB)**: `submission/assets/cover-16x9.png`

## About the project / Long description

```md
## Inspiration

As AI agents transition from passive chatbots to autonomous operators that write Python scripts and inspect live websites, two critical failure modes block real-world adoption:

1. **Unverified Execution Claims**: Many agent demos output a chat message claiming *"I analyzed the CSV"* or *"I audited the page"* without providing cryptographic proof that a real process ran or that its output matched deterministic checks.
2. **Host Blast Radius**: Running LLM-generated code or headless browser sessions directly on the application host exposes environment secrets (`os.environ`), sensitive files (`/etc/shadow`), and cloud instance metadata (`http://169.254.169.254/v1.json`) to prompt injection or resource exhaustion.

We built **ProofBox** (`v1.0-submission`) for **Challenge 01: Blast Radius Zero** to make isolated execution and verifiable receipts first-class primitives on **Vultr**.

## What it does

**ProofBox** is a containment-first agent execution workspace deployed on **Vultr Cloud Compute (`vc2-4c-8gb`, Singapore `sgp` — `https://45-32-110-141.sslip.io`)** and powered by a 3-model **Vultr Serverless Inference** pipeline:

1. **Pattern A — Air-Gapped Python & Data Analyst Sandbox (`--network=none`)**:
   - Mounts user-uploaded CSV/JSON files read-only at `/workspace/`, synthesizes Python 3.12 (`pandas`, `numpy`, `matplotlib`) scripts via `deepseek-v4.1-flash-1017`, executes them inside an unprivileged container (`uid=65534:65534`), self-heals runtime exceptions with a full unified code diff (`attempt_1` → `attempt_2`), harvests generated `/output/*` charts, and runs independent deterministic host checks.
2. **Pattern B — Contained Chromium Browser Inspector**:
   - Validates target URLs against an SSRF Guard that blocks `169.254.0.0/16` (cloud metadata), `127.0.0.0/8`, `file://`, and RFC1918 private subnets in `41ms`, then launches headless Chromium 156 via Playwright inside an isolated container to capture a `1280x720` PNG screenshot (`/output/viewport.png`) and audit HTTP security headers.
3. **Pattern C — Red-Team Attack Lab (The Containment Moment)**:
   - Executes real adversarial probes—secret harvesting (`VULTR_API_KEY`), `/etc/shadow` reads, metadata SSRF (`169.254.169.254`), and `4GB` memory bombs—demonstrating how `nemotron-3.5-content-safety` + Linux kernel boundaries (`uid=65534`, `--cap-drop=ALL`, `--read-only`, `--network=none`, `cgroupv2`) block all tested vectors inside the disposable container.
4. **Ed25519 Asymmetric Digital Signatures (`RFC 8032`)**:
   - After `docker rm -f` teardown is verified, the Orchestrator on the Vultr host signs a canonical JSON receipt (`receiptId`, `containerId`, `inputSha256`, `codeSha256`, `stdoutSha256`, `exitCode`, `spawnedAt`, `destroyedAt`) using its host-only Ed25519 private key. Judges can verify signatures in the UI, test 1-byte payload tampering, or verify downloaded receipts offline using `scripts/verify_receipt.py`.

## How we built it

- **Vultr Cloud Compute (`vc2-4c-8gb`, Ubuntu 24.04 LTS, Singapore `sgp` — `https://45-32-110-141.sslip.io`)**: Provisioned via **Vultr API v2 (`/v2/ssh-keys` and `/v2/instances`)** with Let's Encrypt TLS termination, FastAPI Orchestrator, Ed25519 Notary, and Docker Engine (`proofbox/runtime:latest`).
- **End-to-End HTTPS Proxy (`https://vultr-gamma.vercel.app`)**: Configured to forward `/api/:path*` over HTTPS to `https://45-32-110-141.sslip.io/api/:path*` so both the LabLab `Vercel` platform option and direct Vultr VM access are encrypted end-to-end.
- **Vultr Serverless Inference (`https://api.vultrinference.com/v1`)**:
  - **Stage 1 (Pre-Flight Safety Gate)**: `nemotron-3.5-content-safety`
  - **Stage 2 & 4 (Planner & Self-Healing Synthesizer)**: `deepseek-v4.1-flash-1017` and `glm-5.3-flash`
  - **Stage 5 (Output Verifier)**: `qwen3.8-27b` (paired with independent host deterministic checks)

## Challenges we ran into

1. **Kernel OOM-Kill Buffering (`SIGKILL 137`)**: During initial validation against a `4GB` `bytearray` allocation inside a `256MB` container, the kernel `cgroupv2` OOM killer terminated Python before buffered `stdout` flushed (`11/12` initial pass rate). Enabling `-u` (`PYTHONUNBUFFERED=1`) and `RLIMIT_AS` + exit-code `137` telemetry brought validation to `12/12 (100%)`.
2. **Headless Chromium Process Limits in Rootless Containers**: Running Chromium 156 as `uid=65534` with `--cap-drop=ALL` required tuning `--pids-limit=256`, `--shm-size=256m`, and `--no-zygote` so browser pages render reliably without host privilege escalation.

## Accomplishments that we're proud of

- **100% (12/12) Validation Pass Rate** across external datasets, IANA domains, and OWASP adversarial containment probes with a **3.29s mean latency**.
- **True Ed25519 Asymmetric Receipts** with interactive 1-byte tamper detection and a zero-network offline verifier (`scripts/verify_receipt.py`).
- **End-to-End TLS Encryption** between Browser, Vercel Edge Proxy, and Vultr Cloud Compute VM (`https://45-32-110-141.sslip.io`).

## What we learned

- Combining pre-flight LLM safety screening (`nemotron-3.5-content-safety`), OS kernel isolation (`cgroupv2`, `netns`, `uid=65534`), and deterministic host assertions provides defense-in-depth where neither model hallucinations nor prompt injections compromise the host.

## What's next for ProofBox

- Adding Firecracker/Kata hardware microVM isolation on Vultr Bare Metal to mitigate shared-kernel risks and adding human-in-the-loop approval gates for authenticated browser workflows.
```

## Built with / Technology & Category Tags

`vultr`, `vultr-cloud-compute`, `vultr-serverless-inference`, `docker`, `python`, `fastapi`, `react`, `typescript`, `playwright`, `ed25519`, `ai-agents`, `cybersecurity`

## "Try it out" / Application & Repository Links

- **Application URL (HTTPS Vercel Edge -> HTTPS Vultr VM Proxy, select `Vercel` in LabLab dropdown)**: `https://vultr-gamma.vercel.app`
- **Direct Vultr Cloud Compute VM HTTPS URL**: `https://45-32-110-141.sslip.io`
- **Public GitHub Repository (`v1.0-submission`)**: `https://github.com/Georgefifth/proofbox-vultr`

## Video & Slide Presentation Assets

- **Demo Video File (1080p30 MP4, 55.4s, 8.3 MB)**: `submission/assets/demo.mp4`
- **Slide Presentation Deck (7-Slide 16:9 PDF, 5.6 MB)**: `submission/assets/ProofBox-Presentation-Slides.pdf`

## Image Gallery & Captions (<= 150 characters each)

1. **`submission/assets/gallery-01-workbench.png`** (`1500x1000`)
   - **Caption**: `Guided 3-Step Workspace on Vultr: Normal task execution, malicious attack containment, and collapsible 6-stage timeline.` (120 chars)
2. **`submission/assets/gallery-02-containment-moment.png`** (`1500x1000`)
   - **Caption**: `Self-healing execution audit showing Attempt 1 traceback and unified code diff generated by deepseek-v4.1-flash-1017.` (117 chars)
3. **`submission/assets/gallery-03-architecture.png`** (`1500x1000`)
   - **Caption**: `Ed25519 asymmetric digital signature inspector with interactive 1-byte payload tamper detection and offline verifier.` (117 chars)
4. **`submission/assets/gallery-04-audit-ledger.png`** (`1500x1000`)
   - **Caption**: `Standalone Developer SDK & REST API documentation (/api/v1/sandboxes/exec) for Python and TypeScript agents.` (108 chars)
5. **`submission/assets/gallery-05-validation-benchmark.png`** (`1500x1000`)
   - **Caption**: `Stage 3.5 Validation Benchmark: 100% (12/12) pass rate, 3.29s mean dispatch latency, 41ms SSRF block, and 0 leaked secrets.` (123 chars)
