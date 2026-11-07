# ProofBox — Zero-Blast-Radius Agent Execution & Cryptographic Verification Platform on Vultr

> **Official Entry for Vultr: Agent Rush Hackathon 2026 — Challenge 01: Blast Radius Zero**  
> **Live Public Deployment on Vultr Cloud Compute**: `http://45.32.110.141`  
> **HTTPS Edge Ingress Mirror (Vercel -> Vultr VM Proxy)**: `https://vultr-gamma.vercel.app`  
> **Architecture**: Vultr Cloud Compute (`vc2-4c-8gb`, Singapore `sgp`) + Vultr Serverless Inference (`nemotron-3.5-content-safety`, `deepseek-v4.1-flash-1017`, `glm-5.3-flash`, `qwen3.8-27b`) + Ephemeral Unprivileged Docker Sandboxes (`cgroupv2` + `netns` + `HMAC-SHA256` Execution Proof Receipts)

---

## 1. What ProofBox Solves

Most AI agent demos stop at a chat bubble claiming *"I ran the analysis"* or *"I checked the website"*—or worse, they execute LLM-generated Python and browser scripts directly on the application host where a single prompt injection can exfiltrate `os.environ` API keys, probe cloud instance metadata (`http://169.254.169.254/v1.json`), tamper with host files, or crash the server with a fork/memory bomb.

**ProofBox** is a **containment-first agent execution control plane** built natively on **Vultr**. Every task dispatches into a fresh, unprivileged, ephemeral container and returns a cryptographically signed **Execution Proof Receipt (`ProofReceipt`)** alongside real executed outputs (charts, JSON summaries, DOM audits, and security telemetry).

---

## 2. How Vultr Powers ProofBox

ProofBox integrates **three core Vultr products** into a unified control plane:

1. **Vultr Cloud Compute (`vc2-4c-8gb`, Ubuntu 24.04 LTS, Singapore `sgp` — `45.32.110.141`)**
   - Provisioned and managed via the **Vultr API v2 (`https://api.vultr.com/v2/instances`)**.
   - Hosts the FastAPI Orchestrator, Nginx ingress proxy, ProofBox Web Workbench, and the Docker Engine (`cgroupv2` + Linux network namespaces) that spawns and destroys per-task ephemeral sandboxes.
2. **Vultr Serverless Inference (`https://api.vultrinference.com/v1`)**
   - ProofBox orchestrates **three specialized models** on Vultr Serverless Inference across a 6-stage verification pipeline:
     - **Stage 1 — Pre-Flight Safety Gate (`nemotron-3.5-content-safety`)**: Audits incoming user prompts and agent plans for credential harvesting, SSRF, or destructive intent before any container is spawned.
     - **Stage 2 & 4 — Agent Task Planner & Self-Healing Code Synthesizer (`deepseek-v4.1-flash-1017` & `glm-5.3-flash`)**: Synthesizes Python 3.12 data analysis scripts (**Pattern A**) or isolated web inspection scripts (**Pattern B**). If Attempt 1 throws a runtime error (such as malformed currency strings in a CSV ledger), ProofBox feeds `stderr` back to the model to auto-patch and re-run in a clean container.
     - **Stage 5 — Multimodal & Output Verifier (`qwen3.8-27b`)**: Audits the executed `stdout`, DOM landmarks, HTTP security headers, and generated SVG visual artifacts against the user's original goal.
3. **Vultr API v2 Infrastructure Automation**
   - Automated SSH key registration (`/v2/ssh-keys`), instance provisioning (`/v2/instances`), and live infrastructure health monitoring.

---

## 3. Architecture & The 4 Pillars of Containment

```text
+-----------------------------------------------------------------------------------+
|                           PROOFBOX WEB WORKBENCH (React + TS)                     |
|   [1. Sandbox Workbench]   [2. Red-Team Containment Matrix]   [3. Audit Ledger]   |
+-----------------------------------------+-----------------------------------------+
                                          | HTTPS / HTTP REST (/api/execute)
                                          v
+-----------------------------------------------------------------------------------+
|                 VULTR CLOUD COMPUTE VM ORCHESTRATOR (FastAPI, Host)               |
|                                                                                   |
|  Stage 1: Pre-Flight Safety Gate  ---> Vultr Inference (nemotron-3.5-content-safety)|
|  Stage 2: Planner & Synthesizer   ---> Vultr Inference (deepseek-v4.1 / glm-5.3)  |
|  Stage 3: Ephemeral Sandbox Spawn ---> Docker Engine (cgroupv2 + netns isolation) |
|  Stage 4: Contained Execution     ---> Unprivileged Container (uid=65534:65534)   |
|  Stage 5: Output Verification     ---> Vultr Inference (qwen3.8-27b)              |
|  Stage 6: Teardown & Notary Seal  ---> docker rm -f <id> + HMAC-SHA256 Receipt    |
+-----------------------------------------+-----------------------------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
        v                                 v                                 v
+-----------------------+       +-----------------------+       +-----------------------+
| PATTERN A: CODE       |       | PATTERN B: BROWSER    |       | PATTERN C: RED-TEAM   |
| Air-Gapped Python 3.12|       | Isolated Web Inspector|       | Adversarial Probe     |
| --network=none        |       | SSRF Guard (Blocks    |       | Proves 0 env secrets, |
| --cap-drop=ALL        |       | 169.254.169.254 &     |       | blocks /etc/shadow,   |
| --read-only rootfs    |       | RFC1918 private IPs)  |       | blocks metadata SSRF, |
| --memory=512m         |       | DOM + Header Audit    |       | clamps 4GB OOM / PIDs |
+-----------------------+       +-----------------------+       +-----------------------+
```

### Mandatory Containment Controls Implemented
1. **Process & Privilege Isolation**: Every run executes inside a dedicated container with `--cap-drop=ALL`, `--security-opt=no-new-privileges`, `--read-only` root filesystem (with a bounded `64m` `noexec,nosuid` `/tmp` tmpfs), and unprivileged user `65534:65534` (`nobody`).
2. **Secret Hygiene**: The orchestrator passes `env={"PATH": ...}` and mounts zero host environment variables or files into the sandbox (`secretsInjected: 0`). Even if untrusted code dumps `os.environ`, `VULTR_API_KEY` and `VULTR_INFERENCE_API_KEY` are physically absent.
3. **Resource & Network Limits**: Every container is capped with `--memory=256m/512m`, `--memory-swap=256m/512m`, `--cpus=1.0`, `--pids-limit=64`, and a strict wall-clock timeout (`12s`). Pattern A enforces `--network=none` (zero network egress); Pattern B enforces pre-flight and runtime DNS/IP SSRF filtering blocking `169.254.0.0/16` (cloud metadata), `127.0.0.0/8`, and RFC1918 private subnets.
4. **Lifecycle Discipline**: Every container is forcefully removed via `docker rm -f <container_id>` immediately upon task exit, and removal is verified via `docker inspect <container_id> != 0` (`cleanupVerified: true`) before signing the `ProofReceipt`.

---

## 4. Local Setup & Verification

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker Engine (`docker pull python:3.12-slim`)
- `VULTR_INFERENCE_API_KEY` exported in environment

### Run Locally
```bash
# 1. Install frontend dependencies & build SPA
npm install
npm run build

# 2. Create Python virtualenv & install backend dependencies
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt

# 3. Run backend test suite (verifies Code Sandbox, Browser SSRF Guard, Red-Team Containment, and HMAC Receipts)
PYTHONPATH=. .venv/bin/pytest backend/test_backend.py -v

# 4. Start ProofBox server on port 8000
PYTHONPATH=. .venv/bin/uvicorn backend.server:app --host 0.0.0.0 --port 8000
```

---

## 5. License

MIT License.
