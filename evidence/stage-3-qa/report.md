# Stage 3 QA Report — ProofBox on Vultr (2026-11-06T15:25:45.970Z)

- **Deployed Base URL Tested**: `http://45.32.110.141`
- **Local Build Tested**: `http://127.0.0.1:8000`
- **Browser**: chromium (headless)
- **Scenarios Executed**: 12 (12 passed, 0 failed, 0 blocked)

## Scenario Execution Matrix

| Viewport | Scenario | Title | Status | ms | Detail |
|---|---|---|---:|---:|---|
| desktop | `01-landing-telemetry` | Landing page renders forensic workbench, 6-stage pipeline, and zero overflow | **PASS** | 1076 | All assertions passed |
| desktop | `02-code-sandbox-e2e` | Pattern A: Air-Gapped Python Sandbox execution + HMAC-SHA256 receipt verification | **PASS** | 7292 | All assertions passed |
| desktop | `03-redteam-containment` | Pattern C: Mandatory Containment Moment blocks secret exfiltration, /etc/shadow, and metadata SSRF | **PASS** | 4585 | All assertions passed |
| desktop | `04-browser-sandbox-and-ssrf` | Pattern B: SSRF Guard blocks 169.254.169.254 and allows public URL DOM inspection | **PASS** | 6321 | All assertions passed |
| desktop | `05-empty-and-validation` | Empty state, inline invalid input validation, and preset recovery | **PASS** | 881 | All assertions passed |
| desktop | `06-navigation-and-ledger` | Navigate Red-Team Containment Matrix and verify Audit Ledger signatures | **PASS** | 930 | All assertions passed |
| mobile | `01-landing-telemetry` | Landing page renders forensic workbench, 6-stage pipeline, and zero overflow | **PASS** | 1232 | All assertions passed |
| mobile | `02-code-sandbox-e2e` | Pattern A: Air-Gapped Python Sandbox execution + HMAC-SHA256 receipt verification | **PASS** | 6927 | All assertions passed |
| mobile | `03-redteam-containment` | Pattern C: Mandatory Containment Moment blocks secret exfiltration, /etc/shadow, and metadata SSRF | **PASS** | 4621 | All assertions passed |
| mobile | `04-browser-sandbox-and-ssrf` | Pattern B: SSRF Guard blocks 169.254.169.254 and allows public URL DOM inspection | **PASS** | 6180 | All assertions passed |
| mobile | `05-empty-and-validation` | Empty state, inline invalid input validation, and preset recovery | **PASS** | 1025 | All assertions passed |
| mobile | `06-navigation-and-ledger` | Navigate Red-Team Containment Matrix and verify Audit Ledger signatures | **PASS** | 1053 | All assertions passed |

## Expected Security/Validation Warnings

- [desktop] 04-browser-sandbox-and-ssrf: http — 400 http://45.32.110.141/api/execute
- [desktop] 04-browser-sandbox-and-ssrf: console — Failed to load resource: the server responded with a status of 400 (Bad Request)
- [mobile] 04-browser-sandbox-and-ssrf: http — 400 http://45.32.110.141/api/execute
- [mobile] 04-browser-sandbox-and-ssrf: console — Failed to load resource: the server responded with a status of 400 (Bad Request)

## Issues Discovered & Fixed During QA

1. **Issue #1 (P1 — Fixed in Stage 2/3)**: When calling `qwen3.8-27b` on Vultr Serverless Inference with `max_tokens=160`, the model spent all tokens in `reasoning` and fell back to displaying raw chain-of-thought.
   - **Fix**: Removed fallback to `msg.get('reasoning')` and increased `max_tokens=700` for `qwen3.8-27b` with full artifact/self-healing context.
   - **Regression Status**: Verified resolved (`02-code-sandbox-e2e` and `07-deployed-vultr-live-execution.png`).
2. **Issue #2 (P1 — Fixed in Stage 2/3)**: In `browser_sandbox` mode, SSRF target URL check originally ran after the red-team keyword matcher, causing `http://169.254.169.254/v1.json` in Browser Mode to return 200 (red-team receipt) instead of HTTP 400 SSRF rejection.
   - **Fix**: Moved `is_ssrf_or_private_url` pre-check to the top of `execute_sandbox_task` when `mode == 'browser_sandbox'` and wired HTTP 400 error display in `src/App.tsx`.
   - **Regression Status**: Verified resolved (`04-browser-sandbox-and-ssrf` passes on both desktop and mobile).

## Screenshots Captured

- `evidence/stage-3-qa/screens/01-landing-telemetry-landing-desktop.png`
- `evidence/stage-3-qa/screens/02-code-sandbox-e2e-verified-receipt-desktop.png`
- `evidence/stage-3-qa/screens/03-redteam-containment-containment-proven-desktop.png`
- `evidence/stage-3-qa/screens/04-browser-sandbox-and-ssrf-ssrf-blocked-desktop.png`
- `evidence/stage-3-qa/screens/04-browser-sandbox-and-ssrf-browser-verified-desktop.png`
- `evidence/stage-3-qa/screens/05-empty-and-validation-empty-state-desktop.png`
- `evidence/stage-3-qa/screens/05-empty-and-validation-invalid-input-desktop.png`
- `evidence/stage-3-qa/screens/06-navigation-and-ledger-redteam-matrix-desktop.png`
- `evidence/stage-3-qa/screens/06-navigation-and-ledger-audit-ledger-desktop.png`
- `evidence/stage-3-qa/screens/01-landing-telemetry-landing-mobile.png`
- `evidence/stage-3-qa/screens/02-code-sandbox-e2e-verified-receipt-mobile.png`
- `evidence/stage-3-qa/screens/03-redteam-containment-containment-proven-mobile.png`
- `evidence/stage-3-qa/screens/04-browser-sandbox-and-ssrf-ssrf-blocked-mobile.png`
- `evidence/stage-3-qa/screens/04-browser-sandbox-and-ssrf-browser-verified-mobile.png`
- `evidence/stage-3-qa/screens/05-empty-and-validation-empty-state-mobile.png`
- `evidence/stage-3-qa/screens/05-empty-and-validation-invalid-input-mobile.png`
- `evidence/stage-3-qa/screens/06-navigation-and-ledger-redteam-matrix-mobile.png`
- `evidence/stage-3-qa/screens/06-navigation-and-ledger-audit-ledger-mobile.png`
