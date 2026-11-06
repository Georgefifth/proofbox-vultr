# Human Submission Checklist — ProofBox (Vultr: Agent Rush Hackathon 2026)

> Per safety and competition rules, **you (the human participant)** perform the final form submission on [lablab.ai/ai-hackathons/vultr-hackathon](https://lablab.ai/ai-hackathons/vultr-hackathon). Everything below is ready to copy, paste, and upload from `submission/`.

---

## Step-by-Step Submission Instructions

1. **Open the Official LabLab Submission Page**:
   - Go to [https://lablab.ai/ai-hackathons/vultr-hackathon](https://lablab.ai/ai-hackathons/vultr-hackathon) (logged into your LabLab account) and open your team submission form.
   - Select **Challenge 01 — Blast Radius Zero**.
2. **Copy Basic Information from `submission/fields.md`**:
   - **Project Title**: `ProofBox — Zero-Blast-Radius Agent Sandbox on Vultr`
   - **Short Description**: Copy the 178-character Elevator Pitch from `submission/fields.md`.
   - **Long Description**: Copy the Markdown block under `## About the project / Long description` in `submission/fields.md`.
   - **Technology & Category Tags**: Add `vultr`, `vultr-cloud-compute`, `vultr-serverless-inference`, `docker`, `python`, `fastapi`, `react`, `typescript`, `playwright`, `ai-agents`, `cybersecurity`, `sandboxing`.
3. **Upload Cover Image, Video & Slide Presentation from `submission/assets/`**:
   - **Cover Image / Thumbnail**: Upload `submission/assets/cover-16x9.png` (for 16:9 cover) or `submission/assets/thumbnail.png` (for 3:2 thumbnail).
   - **Video Presentation**: Upload `submission/assets/demo.mp4` (`1920x1080`, `55.4s`, `8.3 MB`, includes narration, captions, and the required **Containment Moment** in Scene 5).
   - **Slide Presentation**: Upload `submission/assets/ProofBox-Presentation-Slides.pdf` (7-slide widescreen technical deck).
   - **Gallery Images (Optional/If supported)**: Upload `gallery-01-workbench.png` through `gallery-05-validation-benchmark.png` with their matching captions from `submission/fields.md`.
4. **Fill App Hosting & Repository Links**:
   - **Public GitHub Repository**: `https://github.com/Georgefifth/proofbox-vultr`
   - **Demo Application Platform**: `Vultr Cloud Compute`
   - **Application URL**: `http://45.32.110.141`
5. **(Optional Bonus Visibility) Showcase on Vultr Community**:
   - Post the same summary and links on [https://community.vultr.com/e/vultr-agent-rush-hackathon](https://community.vultr.com/e/vultr-agent-rush-hackathon).

---

## Pre-Submission Verification Checklist

- [x] **Project Title & Short Pitch**: Present in `submission/fields.md` (`178` chars, `<= 200` char limit).
- [x] **Thumbnail (`submission/assets/thumbnail.png`)**: Bespoke generated graphic (not cropped screenshot), `1500x1000` (3:2), `91 KB` (`< 5 MB`).
- [x] **Cover Image (`submission/assets/cover-16x9.png`)**: `1920x1080` (16:9), `836 KB` (`< 5 MB`).
- [x] **Gallery Images (`gallery-01` .. `gallery-05`)**: 5 PNG images, `1500x1000` (3:2 ratio), `395 KB–748 KB` (`< 5 MB`), captions `122–126` chars (`<= 150` chars).
- [x] **Demo Video (`submission/assets/demo.mp4`)**: `1920x1080` @ 30fps, `55.4s`, narrated with captions, explicitly demonstrates a live **Containment Moment** on Vultr.
- [x] **Slide Deck (`submission/assets/ProofBox-Presentation-Slides.pdf`)**: 7-page 16:9 PDF deck with architecture, problem flow, exploded stack, live demo, containment proof, and validation benchmark.
- [x] **All Quantitative Claims Match Stage 3.5 Evidence**: `100% (12/12)` validation pass rate, `3.29s` mean latency, `41ms` SSRF block, `0` secrets exposed (`evidence/stage-3.5-validation/report.md`).
- [x] **Live Vultr Deployment URL Verified**: `http://45.32.110.141` and `http://45.32.110.141/api/health` return `HTTP 200 OK`.
- [x] **Public GitHub Repo Verified & Secret-Free**: `https://github.com/Georgefifth/proofbox-vultr` returns `HTTP 200 OK`, README documents Vultr Cloud Compute + Vultr Serverless Inference + Sandbox architecture, zero secrets committed.
