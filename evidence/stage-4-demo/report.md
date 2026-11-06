# Stage 4 Demo Video & Presentation Slides Report — ProofBox on Vultr

## 1. Production Pipeline & Tools Used
- **Engine**: `~/tools/demo-recorder` (Remotion + React SVG + Playwright Live Capture + `edge-tts` + FFmpeg sidechain-ducked BGM).
- **Fact Validation (`project/facts.json`)**: `3` verified facts backed by Stage 3.5 empirical evidence (`100%` pass rate across 12 cases, `3.29s` mean dispatch latency, `0` secrets exposed), `1` unverified claim explicitly blocked (`0` validation errors).
- **Storyboard (`planning/storyboard.json`)**: 7 choreographed scenes (`55.37s` total duration, `1920x1080` @ 30fps, H.264 + AAC 160kbps audio).

---

## 2. Exported Deliverables in `evidence/stage-4-demo/`

| Asset | File Path | Specification | Verification Status |
|---|---|---|---|
| **Full Narrated Demo Video** | `evidence/stage-4-demo/demo.mp4` | `1920x1080`, 30fps, `55.37s`, `8.6 MB`, narrated + synchronized captions + sidechain BGM | Frame-checked across all 7 scenes (PASS) |
| **Cover Image** | `evidence/stage-4-demo/cover.png` | `1920x1080` PNG (`836 KB`) | Inspected via `read` (PASS) |
| **PDF Presentation Deck** | `evidence/stage-4-demo/slides/ProofBox-Presentation-Slides.pdf` | 7-page 16:9 widescreen PDF presentation deck | Verified ready for LabLab upload |
| **Editable Vector Schematics** | `evidence/stage-4-demo/assets/proofbox_hero.svg`, `proofbox_stack.svg` | Custom SVG architecture & 4-layer stack diagrams | Verified |
| **Scene-by-Scene Slide PNGs** | `evidence/stage-4-demo/slides/slide-01-opening.png` .. `slide-07-closing.png` | 7 high-resolution 1080p PNG slides | All 7 visually inspected via `read` |

---

## 3. Visual QA & Frame Inspection Checklist

1. **Slide 01 (`slide-01-opening.png` — `opening_title`)**: Displays ProofBox title, 3 verified metric badges (`35 VULTR MODELS LIVE`, `3.29s MEAN DISPATCH`, `HMAC-SHA256 RECEIPTS`), and custom SVG control-plane schematic with timed HUD callout on the 3-Model Vultr Inference Triad.
2. **Slide 02 (`slide-02-problem.png` — `problem_flow`)**: Programmatic SVG bottleneck diagram contrasting `Unisolated Host Exec` (`Secret & SSRF Breach`) against `ProofBox Sandbox` (`uid=65534 · net=none · 0 Secrets`).
3. **Slide 03 (`slide-03-architecture.png` — `exploded_view`)**: Isometric 4-layer exploded stack showing Layer 1 (`Nemotron 3.5 Safety Gate`), Layer 2 (`DeepSeek V4.1 Self-Healing Planner`), Layer 3 (`Ephemeral Docker Sandbox`), and Layer 4 (`Qwen 3.8 Verifier & Notary`).
4. **Slide 04 (`slide-04-live-code-demo.png` — `real_footage_with_annotations`)**: Real Playwright capture from `http://45.32.110.141` demonstrating Pattern A air-gapped CSV analysis, self-healing currency parser, SVG chart artifact, and HMAC-SHA256 signature verification.
5. **Slide 05 (`slide-05-containment-moment.png` — `real_footage_with_annotations`)**: Mandatory Hackathon Containment Moment captured live on `http://45.32.110.141`, showing `THREAT CONTAINED & NEUTRALIZED — HOST INTEGRITY 100% INTACT` (`VULTR_API_KEY=False`, `/etc/shadow Errno 13`, `169.254.169.254 Network is unreachable`) and the 4/4 Red-Team Containment Matrix.
6. **Slide 06 (`slide-06-validation.png` — `technical_validation`)**: Animated empirical benchmark bars (`100%` pass rate vs `91.7%` initial baseline, `3.3s` mean latency, `41ms` SSRF block, `100%` container teardown) alongside explicit Scope Boundaries.
7. **Slide 07 (`slide-07-closing.png` — `closing_summary`)**: Summary card with live Vultr deployment URL (`http://45.32.110.141`) and public GitHub repository (`github.com/Georgefifth/proofbox-vultr`).
