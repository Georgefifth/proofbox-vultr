# ProofBox — Zero-Blast-Radius Agent Execution & Ed25519 Verification Platform on Vultr

> **Official Entry for Vultr: Agent Rush Hackathon 2026 — Challenge 01: Blast Radius Zero**  
> **Release Version**: `v1.0-submission` (Deployed & Verified on **2026-11-08 UTC**)  
> **Direct Vultr Cloud Compute HTTPS Web App**: [`https://45-32-110-141.sslip.io`](https://45-32-110-141.sslip.io) (`45.32.110.141`, Singapore `sgp`, `vc2-4c-8gb`, Instance ID `c6a71904-3636-4699-9cf5-0d52beb32d8b`)  
> **Vercel HTTPS Edge Mirror (End-to-End TLS -> Vultr VM)**: [`https://vultr-gamma.vercel.app`](https://vultr-gamma.vercel.app)  
> **Core Stack**: Vultr Cloud Compute + Vultr Serverless Inference (`nemotron-3.5-content-safety`, `deepseek-v4.1-flash-1017`, `glm-5.3-flash`, `qwen3.8-27b`) + Ephemeral Unprivileged Docker Sandboxes (`uid=65534`, `cgroupv2`, `netns`) + **Ed25519 Asymmetric Digital Signatures (`RFC 8032`)**

---

## 1. 60-Second Evaluator Quick-Start (3-Step Live Walkthrough)

Open either the **Direct Vultr VM HTTPS URL** ([`https://45-32-110-141.sslip.io`](https://45-32-110-141.sslip.io)) or the **Vercel HTTPS Proxy** ([`https://vultr-gamma.vercel.app`](https://vultr-gamma.vercel.app)) and click the 3 buttons in the top guided bar:

1. **Step 1 — Run Normal Task Live (`Scenario 1: Clean CSV Spend Analysis & Chart`)**:
   - Spawns a fresh air-gapped container (`--network=none`, `uid=65534`) on our Vultr VM, mounts `/workspace/dataset.csv` read-only, runs `pandas` + `matplotlib` to sanitize malformed currency strings and render `/output/chart.svg`, executes 4 deterministic host checks, destroys the container, and signs a new `ProofReceipt`.
2. **Step 2 — Run Malicious Attack Live (`Scenario 2: Secret Theft + /etc/shadow + SSRF`)**:
   - Executes an adversarial script attempting to read `os.environ["VULTR_API_KEY"]`, open `/etc/shadow`, and probe `http://169.254.169.254/v1.json`. All 3 tested vectors are blocked inside the disposable container (`VULTR_API_KEY present: False`, `PermissionError [Errno 13]`, `Network is unreachable [Errno 101]`), and the container is destroyed.
3. **Step 3 — Verify Live Vultr VM & Ed25519 Signature (`2. Vultr Architecture & Live Proof` + `3. Security & Ed25519 Receipt`)**:
   - Triggers a live probe (`GET /api/vultr-proof`) returning the Vultr VM’s kernel, uptime, and a freshly generated `chatcmpl-...` completion ID from `https://api.vultrinference.com/v1/chat/completions`.
   - In the **`3. Security & Ed25519 Receipt`** tab, click **`Verify Receipt Signature`** (passes) and **`Simulate Payload Tampering (Flip 1 Byte)`** (fails with `TAMPER DETECTED — SIGNATURE INVALID`).

---

## 2. Architecture & End-to-End TLS Topology

```text
+---------------------------------------------------------------------------------------------------+
| USER / JUDGE BROWSER                                                                              |
|   • Direct Vultr VM HTTPS   : https://45-32-110-141.sslip.io (Let's Encrypt TLS on Vultr VM)      |
|   • Vercel HTTPS Proxy      : https://vultr-gamma.vercel.app (TLS Rewrite -> 45-32-110-141.sslip) |
+-------------------------------------------------+-------------------------------------------------+
                                                  | HTTPS TLS 1.3 (/api/execute, /api/vultr-proof)
                                                  v
+---------------------------------------------------------------------------------------------------+
| VULTR CLOUD COMPUTE VM — 45.32.110.141 (Singapore sgp · vc2-4c-8gb · Ubuntu 24.04 · Kernel 6.8)   |
|                                                                                                   |
|  [FastAPI Orchestrator & Ed25519 Notary]  <===(HTTPS)===>  [Vultr Serverless Inference API]       |
|   • Holds Ed25519 Private Key on Host                      https://api.vultrinference.com/v1      |
|   • Runs Deterministic Host Checks                         • nemotron-3.5-content-safety          |
|   • Spawns & Destroys Docker Containers                    • deepseek-v4.1-flash-1017 / glm-5.3   |
|                                                            • qwen3.8-27b                          |
|                         |                                                                         |
|                         v  docker run --rm --user=65534:65534 --cap-drop=ALL --read-only          |
|  +---------------------------------------------------------------------------------------------+  |
|  | EPHEMERAL DOCKER CONTAINER (sbx-py-... / sbx-pw-... / sbx-rt-...)                           |  |
|  |  • 0 Host Secrets Mounted (VULTR_API_KEY absent)   • /workspace (ro) & /output (rw)         |  |
|  |  • --network=none (Code/Attack) or SSRF-Filtered   • Destroyed via docker rm -f on exit     |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

### UI Navigation Structure (4 Views)
- **`1. Agent Workspace`**: Submit tasks (or write direct Python/Playwright scripts), upload CSV/JSON files into `/workspace/`, and inspect outcomes across 3 focused tabs (`1. Overview & Timeline`, `2. Execution & Code (Self-Healed Diff)`, `3. Security & Ed25519 Receipt`).
- **`2. Vultr Architecture & Live Proof`**: Inspect the deployment topology, tested security scope, and trigger live `/api/vultr-proof` probes.
- **`3. Red-Team Attack Lab`**: Interactive adversarial containment matrix and historical receipt audit ledger.
- **`4. Developer SDK`**: Programmatic REST API (`POST /api/v1/sandboxes/exec`) and Python/JS SDK documentation.

---

## 3. Ed25519 Asymmetric Digital Signatures & Offline Verification

### How Signing Works
1. **Key Separation**: The FastAPI Orchestrator on the Vultr host holds an **Ed25519 private signing key** (`cryptography.hazmat.primitives.asymmetric.ed25519`). Unprivileged containers (`uid=65534`) never have access to the signing key or host environment variables.
2. **Canonical Signed Payload**: After a container exits and `docker rm -f <container_id>` is confirmed via `docker inspect != 0`, the Orchestrator computes `SHA-256` digests of `prompt` (`inputSha256`), `generatedCode` (`codeSha256`), and `stdout` (`stdoutSha256`), and serializes a canonical JSON object with sorted keys (`sort_keys=True, separators=(",", ":")`):
   ```json
   {
     "codeSha256": "<64-hex>",
     "containerId": "sbx-py-...",
     "destroyedAt": "2026-11-08T...",
     "exitCode": 0,
     "inputSha256": "<64-hex>",
     "receiptId": "rcpt-...",
     "spawnedAt": "2026-11-08T...",
     "stdoutSha256": "<64-hex>"
   }
   ```
3. **Public Key**: The Orchestrator’s Ed25519 public key is published in every receipt (`ed25519PublicKeyHex`: `ec5b7757873c502b0a4455c9108777a24b99d79efbbfd12354935cabd81bf1d0`).

### Verify Any Exported Receipt Offline (Zero Network Required)

We include a standalone offline verifier (`scripts/verify_receipt.py`) and a real exported live receipt (`examples/sample_live_receipt.json`):

```bash
# 1. Verify an unmodified live receipt completely offline
python3 scripts/verify_receipt.py examples/sample_live_receipt.json

# Output:
#   ✓ SHA-256 digests verified for prompt, generatedCode, and stdout.
#   ✓ Canonical JSON payload matches receipt lifecycle & digest fields.
#   ✓ Ed25519 signature verified against public key ec5b7757873c502b0a4455c9...
# VERDICT: VALID ED25519 RECEIPT

# 2. Simulate tampering (flips 1 character in memory -> verification fails)
python3 scripts/verify_receipt.py examples/sample_live_receipt.json --tamper-test
```

---

## 4. Tested Security Scope & Residual Risk Disclosure

- **Empirically Tested Scope (`12/12` in `validation/run_validation.py`)**:
  1. **Secret Hygiene**: `env={"PATH": ...}` passed to `docker run`; `VULTR_API_KEY` and `VULTR_INFERENCE_API_KEY` are verified absent inside `os.environ`.
  2. **Filesystem & Privilege Isolation**: Containers run as `uid=65534:65534` (`nobody`) with `--cap-drop=ALL`, `--security-opt=no-new-privileges`, and `--read-only` root filesystem (`PermissionError [Errno 13]` on `/etc/shadow`).
  3. **Network & SSRF Isolation**: Python and Attack modes run with `--network=none` (`Errno 101 Network is unreachable` on `http://169.254.169.254/v1.json`). Browser mode enforces a pre-flight DNS/IP SSRF filter blocking `169.254.0.0/16`, `127.0.0.0/8`, `file://`, and RFC1918 private subnets.
  4. **Resource Limits & Lifecycle**: Containers are capped via `cgroupv2` (`--memory=256m/512m`, `--pids-limit=64`) and forcefully removed via `docker rm -f` after every run.
- **Known Boundaries & Residual Risks**:
  - Containers share the host Linux kernel (`6.8.0-147-generic`); unlike hardware microVMs (Firecracker/Kata), kernel-level container escape vulnerabilities are outside the scope of standard Docker namespaces.
  - Browser mode allows outbound HTTPS to public non-RFC1918 IPs so Chromium can load public web pages.

---

## 5. Local Development & Reproducible Setup

```bash
# 1. Install frontend dependencies & build SPA
npm install
npm run build

# 2. Create Python virtualenv & install backend dependencies
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt

# 3. Run backend unit & integration test suite (verifies Code Sandbox, SSRF Guard, Red-Team Containment, and Ed25519 Signatures)
PYTHONPATH=. .venv/bin/pytest backend/test_backend.py -v

# 4. Verify offline Ed25519 receipt validation
.venv/bin/python3 scripts/verify_receipt.py examples/sample_live_receipt.json

# 5. Start ProofBox server on port 8000
PYTHONPATH=. .venv/bin/uvicorn backend.server:app --host 0.0.0.0 --port 8000
```

---

## 6. License

MIT License.
