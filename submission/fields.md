# Submission Fields — ProofBox (Vultr: Agent Rush Hackathon 2026)

## Project name

ProofBox — Zero-Blast-Radius Agent Sandbox on Vultr

## Elevator pitch / Short description (178 characters)

Containment-first agent execution platform on Vultr Cloud Compute & Serverless Inference that runs untrusted code and web tasks in ephemeral sandboxes with HMAC-SHA256 receipts.

## Thumbnail / Cover Image

- **3:2 Thumbnail (1500x1000 PNG, 91 KB)**: `submission/assets/thumbnail.png`
- **16:9 Widescreen Cover (1920x1080 PNG, 836 KB)**: `submission/assets/cover-16x9.png`

## About the project / Long description

```md
## Inspiration

As AI agents transition from passive chatbots to autonomous operators that write Python scripts and inspect live websites, two critical failure modes block enterprise adoption:

1. **Unverified Hallucinations**: Many agent demos output a chat message claiming *"I analyzed the CSV"* or *"I audited the page"* without providing cryptographic proof that a real process ran.
2. **Catastrophic Host Blast Radius**: Running LLM-generated code or headless browser sessions directly on the application host exposes environment secrets (`os.environ`), internal network services, and cloud instance metadata (`http://169.254.169.254/v1.json`) to a single prompt injection or runaway fork/memory bomb.

We built **ProofBox** for **Challenge 01: Blast Radius Zero** to turn containment and verification into first-class primitives on **Vultr**.

## What it does

**ProofBox** is a zero-blast-radius agent execution workbench deployed on **Vultr Cloud Compute (`vc2-4c-8gb`, Singapore)** and powered by a 3-model **Vultr Serverless Inference** pipeline:

1. **Pattern A — Air-Gapped Python & Data Analyst Sandbox (`--network=none`)**:
   - Synthesizes Python 3.12 data analysis and charting scripts using `deepseek-v4.1-flash-1017` / `glm-5.3-flash`, executes them inside an unprivileged, read-only, zero-secret container (`uid=65534:65534`), automatically self-heals runtime exceptions (such as malformed currency strings in financial ledgers), and renders forensic SVG breakdown charts.
2. **Pattern B — Contained Browser & DOM Security Inspector**:
   - Validates target URLs against an SSRF Guard that blocks `169.254.0.0/16` (cloud metadata), `127.0.0.0/8`, `file://`, and RFC1918 private subnets in `41ms`, then launches an isolated web inspection container to audit DOM landmarks, links, and missing HTTP security headers (`Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security`).
3. **Pattern C — Interactive Red-Team Containment Matrix (The Containment Moment)**:
   - Lets users and judges fire real adversarial probes—secret exfiltration (`VULTR_API_KEY`, `/proc/1/environ`), `/etc/shadow` reads, metadata SSRF (`169.254.169.254`), and `4GB` memory bombs—and proves that the 2-Layer Defense (`nemotron-3.5-content-safety` Pre-Flight Gate + Linux kernel `cgroupv2` / `netns` / `DAC`) neutralizes every vector while leaving the Vultr host 100% untouched.
4. **Cryptographic Execution Proof Receipts (`ProofReceipt`)**:
   - Every run computes `SHA-256` digests of the input prompt, executed code, stdout stream, and output artifacts, verifies container destruction (`docker rm -f` + `docker inspect != 0`), and seals the receipt with an `HMAC-SHA256` signature verified by `qwen3.8-27b`.

## How we built it

- **Vultr Cloud Compute (`vc2-4c-8gb`, Ubuntu 24.04 LTS, Singapore `sgp` — `http://45.32.110.141`)**: Provisioned via the **Vultr API v2 (`/v2/ssh-keys` and `/v2/instances`)** to run our FastAPI Orchestrator, Nginx reverse proxy, and Docker Engine (`cgroupv2` + network namespaces).
- **Vultr Serverless Inference (`https://api.vultrinference.com/v1`)**:
  - **Stage 1 (Pre-Flight Safety Gate)**: `nemotron-3.5-content-safety` audits incoming tasks for adversarial intent before any container is created.
  - **Stage 2 & 4 (Planner & Self-Healing Synthesizer)**: `deepseek-v4.1-flash-1017` and `glm-5.3-flash` synthesize executable Python/web inspection scripts and auto-patch errors on retry.
  - **Stage 5 (Output Verifier)**: `qwen3.8-27b` audits the sandbox `stdout` and generated SVG artifacts against the user's goal.
- **Hardened Ephemeral Container Runtime**: Every container runs with `--cap-drop=ALL`, `--security-opt=no-new-privileges`, `--read-only`, `--tmpfs=/tmp:rw,noexec,nosuid,size=64m`, `--pids-limit=64`, `--memory=256m/512m`, `--cpus=1.0`, `--user=65534:65534`, and zero host environment variables (`secretsInjected: 0`).
- **Frontend Workbench**: Built with React 18, TypeScript, and Vite using a high-density forensic clean-room design system.

## Challenges we ran into

1. **Kernel OOM-Kill Buffering (`SIGKILL 137`)**: During our initial Stage 3.5 validation run against a `4GB` `bytearray` memory bomb inside a `256MB` container, the Linux kernel `cgroupv2` OOM killer terminated Python before buffered `stdout` flushed (`11/12` initial pass rate). Passing `-u` (`PYTHONUNBUFFERED=1`) and enforcing `RLIMIT_AS` + exit-code `137` telemetry resolved this, bringing validation to `12/12 (100%)`.
2. **Reasoning Token Allocation on Vultr Inference Models**: Initially, `deepseek-v4.1-flash-1017` and `glm-5.3-flash` consumed token budgets on internal chain-of-thought (`reasoning_tokens`). Discovering `"chat_template_kwargs": {"enable_thinking": false}` on `api.vultrinference.com/v1` reduced code-generation latency from `3.98s` to `1.67s` with zero token truncation.

## Accomplishments that we're proud of

- **100% (12/12) Real-World & OWASP Adversarial Validation Pass Rate** on our live Vultr Cloud Compute instance (`http://45.32.110.141`) with a **3.29s mean end-to-end latency**.
- **Zero Secrets Exposed (`secretsInjected: 0`)** and **100% Verified Container Teardown (`cleanupVerified: true`)** across every test run.
- **Sub-50ms SSRF Protection (`41ms`)** blocking `http://169.254.169.254/v1.json`, `http://127.0.0.1:8000`, and `file:///etc/passwd`.

## What we learned

- Combining a fast pre-flight content safety model (`nemotron-3.5-content-safety`) with kernel-enforced container isolation (`cgroupv2`, `netns`, non-root `uid=65534`) provides true defense-in-depth: even if an adversarial prompt bypasses semantic filters, the operating system boundary guarantees zero host impact.

## What's next for ProofBox

- Adding ephemeral per-task microVM snapshot forks on Vultr Bare Metal and supporting multi-step human-in-the-loop approval gates for authenticated browser mutations.
```

## Built with / Technology & Category Tags

`vultr`, `vultr-cloud-compute`, `vultr-serverless-inference`, `docker`, `python`, `fastapi`, `react`, `typescript`, `playwright`, `ai-agents`, `cybersecurity`, `sandboxing`

## "Try it out" / Application & Repository Links

- **Live Application URL (Deployed on Vultr Cloud Compute)**: `http://45.32.110.141`
- **Demo Application Platform**: `Vultr Cloud Compute (vc2-4c-8gb, Singapore sgp)`
- **Public GitHub Repository**: `https://github.com/Georgefifth/proofbox-vultr`

## Video & Slide Presentation Assets

- **Demo Video File (1080p30 MP4, 55.4s, 8.3 MB)**: `submission/assets/demo.mp4`
- **Video URL (if external link required by form)**: `TODO(human): Upload submission/assets/demo.mp4 to YouTube/Loom/LabLab video uploader and paste the video URL here`
- **Slide Presentation Deck (7-Slide 16:9 PDF, 5.6 MB)**: `submission/assets/ProofBox-Presentation-Slides.pdf`

## Image Gallery & Captions (<= 150 characters each)

1. **`submission/assets/gallery-01-workbench.png`** (`1500x1000`, `406 KB`)
   - **Caption**: `Live Vultr Workbench: 6-stage Serverless Inference pipeline, self-healing CSV audit, and HMAC-SHA256 Execution Proof Receipt.` (126 chars)
2. **`submission/assets/gallery-02-containment-moment.png`** (`1500x1000`, `485 KB`)
   - **Caption**: `Mandatory Containment Moment: Secret theft (VULTR_API_KEY), /etc/shadow read, and 169.254.169.254 SSRF blocked in sandbox.` (122 chars)
3. **`submission/assets/gallery-03-architecture.png`** (`1500x1000`, `748 KB`)
   - **Caption**: `Four-layer containment stack linking Nemotron 3.5, DeepSeek V4.1, ephemeral Docker cgroupv2 sandboxes, and Qwen 3.8 notary.` (123 chars)
4. **`submission/assets/gallery-04-audit-ledger.png`** (`1500x1000`, `395 KB`)
   - **Caption**: `Cryptographic Execution Audit Ledger verifying HMAC-SHA256 payload signatures and confirmed container teardown across runs.` (123 chars)
5. **`submission/assets/gallery-05-validation-benchmark.png`** (`1500x1000`, `569 KB`)
   - **Caption**: `Stage 3.5 Validation Benchmark: 100% (12/12) pass rate, 3.29s mean dispatch latency, 41ms SSRF block, and 0 leaked secrets.` (123 chars)
