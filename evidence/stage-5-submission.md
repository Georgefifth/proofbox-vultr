# Stage 5 Submission Package Evidence — ProofBox on Vultr

## 1. Submission Package Contents (`submission/`)

| File | Purpose | Format & Size | Status |
|---|---|---|---|
| `submission/fields.md` | Complete copy-pasteable fields (Title, 178-char Pitch, Markdown Story, Tags, Links, Gallery Captions) | Markdown | Verified |
| `submission/checklist.md` | Step-by-step human submission instructions & pre-flight checklist | Markdown | Verified |
| `submission/assets/thumbnail.png` | Custom-generated 3:2 project thumbnail (not cropped from app) | PNG, `1500x1000`, `91 KB` | Verified |
| `submission/assets/cover-16x9.png` | 16:9 widescreen cover image for LabLab | PNG, `1920x1080`, `836 KB` | Verified |
| `submission/assets/demo.mp4` | 1080p30 narrated, captioned hackathon demo video with live Containment Moment | MP4 (H.264/AAC), `55.37s`, `8.3 MB` | Verified |
| `submission/assets/ProofBox-Presentation-Slides.pdf` | 7-page widescreen 16:9 technical presentation slide deck | PDF, `5.6 MB` | Verified |
| `submission/assets/gallery-01-workbench.png` .. `gallery-05-validation-benchmark.png` | 5 3:2 gallery images (`1500x1000`) with `<= 150` char English captions | PNG, `395 KB–748 KB` each | Verified |

---

## 2. Live URL & Repository Reachability Verification

- **Live Vultr Cloud Compute Web App (`http://45.32.110.141`)**: Verified HTTP 200 OK; full 6-stage Vultr Serverless Inference + Docker Sandbox pipeline active.
- **Live Vultr Health API (`http://45.32.110.141/api/health`)**: Verified HTTP 200 OK (`{"status":"ok","vmHostname":"proofbox-vultr (Vultr Cloud Compute · sgp)","inferenceStatus":"LIVE (35 Vultr Models Ready)","dockerStatus":"DOCKER CGROUPV2 + NETNS ACTIVE"}`).
- **Public GitHub Repository (`https://github.com/Georgefifth/proofbox-vultr`)**: Verified public, contains full source code, tests, evidence, and Vultr architecture documentation in `README.md`, with zero secrets committed.

---

## 3. Claim-to-Evidence Traceability

Every metric in `submission/fields.md` is backed by Stage 3 and Stage 3.5 artifacts:
- **`100% (12/12)` Real-World & OWASP Validation Pass Rate**: `evidence/stage-3.5-validation/raw_results_post_fix.json` & `evidence/stage-3.5-validation/report.md`
- **`3.29s` Mean End-to-End Sandbox Dispatch Latency**: `evidence/stage-3.5-validation/raw_results_post_fix.json` (`meanLatencyMs: 3292.2`)
- **`41ms` Cloud Metadata SSRF Block Latency**: `evidence/stage-3.5-validation/raw_results_post_fix.json` (`VAL-07-NEGATIVE-SSRF-METADATA: 41ms`)
- **`12/12` Playwright Browser E2E QA Scenarios Passed (Desktop & Mobile)**: `evidence/stage-3-qa/results.json` & `evidence/stage-3-qa/report.md`
