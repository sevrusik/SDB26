# Forensic Reason Codes (FRC) — Technical Reference
## SDB-26 Document Authenticity Framework

**Version:** 1.0  
**Status:** Draft  
**Repository:** github.com/sevrusik/SDB26

---

## Overview

Forensic Reason Codes (FRC) provide structured, machine-readable explanations for document authenticity verdicts. They replace single-verdict outputs (`PASS` / `FAIL`) with a taxonomy of specific forensic signals — enabling audit trails, regulatory defensibility, and explainable AI compliance.

**Core principle:** A verdict without a reason code is not auditable. FRC makes the basis for every decision explicit and reproducible.

---

## Verdict Structure

Every document assessment produces a structured output:

```json
{
  "verdict": "GENUINE | FRAUD | INSUFFICIENT",
  "verdict_confidence": 0.0–1.0,
  "primary_codes": ["FRC-L1-FFT-GRID", "FRC-L2-METADATA-WIPE"],
  "supporting_codes": [],
  "forensic_note": "Human-readable explanation for audit trail",
  "required_action": "approve | manual_review | recapture_required | reject",
  "sdb26_class": "SYNTHETIC | SCREENSHOT | EDITED | GENUINE | INSUFFICIENT",
  "attack_level": "L1 | L2 | L3 | INF",
  "evaluated_at": "ISO-8601 timestamp",
  "sdb26_version": "SDB-26-v1.0",
  "model_trace": {"detector_version": "x.y.z", "pipeline_id": "prod-kyc-v1"}
}
```

---

## Level L1 — Synthetic Generation

Codes indicating the document was never produced by a physical device or process.

| Code | Signal | Detection method | Notes |
|------|--------|-----------------|-------|
| `FRC-L1-FFT-GRID` | Regular frequency grid characteristic of GAN/Diffusion generation algorithms | FFT analysis — periodic peaks in mid-frequency bands (0.1–0.4 cycles/pixel) | Most reliable L1 signal; present in SDXL, SD 1.5, Midjourney outputs |
| `FRC-L1-GEN-TEXTURE-UNIFORM` | Overly uniform paper texture; absence of natural sensor noise (PRNU analysis negative) | PRNU residual analysis; noise field uniformity scoring | Requires reference PRNU library for claimed device; absence alone is weak |
| `FRC-L1-SEM-INCOHERENCE` | Logical inconsistency in document data (e.g. document number fails regional checksum validation despite visually perfect typography) | Data validation layer — checksum, date logic, issuing authority format rules | Note: this is a data validation signal, not image forensics. Treat as corroborating evidence, not primary forensic signal |
| `FRC-L1-ORNAMENT-ANOMALY` | Specific distortions on complex graphical elements (coats of arms, guilloche patterns) characteristic of current generative model limitations | Visual inspection layer (LLM-assisted); pattern matching on known artifact signatures | Model-specific; artifact signatures change with model versions — requires corpus refresh |

**SDB-26 class:** `SYNTHETIC`  
**Typical confidence range when codes present:** 0.70–0.95

---

## Level L2 — Manipulation / Editing

Codes for genuine documents that have been altered after original issuance.

| Code | Signal | Detection method | Notes |
|------|--------|-----------------|-------|
| `FRC-L2-ELA-DIVERGENCE` | Error Level Analysis reveals different compression levels in the name/data field vs. the rest of the document | ELA at 90% re-compression quality; regional variance analysis | Effective for JPEG manipulation; less reliable for PNG-sourced documents |
| `FRC-L2-FONT-INCONSISTENCY` | Micro-differences in character rendering (kerning, anti-aliasing) indicating text insertion | Sub-pixel font rendering analysis; comparison against known issuing authority typography profiles | Requires reference typography database per issuing authority and document type |
| `FRC-L2-METADATA-WIPE` | File metadata (EXIF) absent or replaced with generic software defaults (Photoshop, GIMP, DALL-E signatures) | EXIF analysis; software signature detection against known editing tool fingerprints | Absence of EXIF alone is not proof of manipulation — see FRC-INF-EXIF-ABSENT |

**SDB-26 class:** `EDITED`  
**Typical confidence range when codes present:** 0.60–0.90  
**Note:** L2 attacks on genuine documents are often the highest-stakes fraud class in HNW onboarding and source-of-funds verification. The document base is authentic; only data fields have been altered.

---

## Level L3 — Screen Photo Attack

Codes for documents captured by photographing a screen — the most operationally common attack class in 2025–2026.

| Code | Signal | Detection method | Notes |
|------|--------|-----------------|-------|
| `FRC-L3-MOIRE-PATTERN` | Moiré interference pattern from re-photographing an LCD/OLED display | FFT analysis — characteristic interference peaks at screen pixel frequency; spatial domain moiré detection | Present even at high camera quality; visible at specific spatial frequencies regardless of capture device resolution |
| `FRC-L3-RGB-SUBPIXEL-GRID` | Subpixel grid boundaries of monitor visible at high magnification | High-frequency spatial analysis; subpixel pattern detection | Requires sufficient image resolution (>300 DPI equivalent); may be absent in very high quality captures |
| `FRC-L3-DOUBLE-COMPRESSION` | Evidence of double JPEG compression with different quantization tables — once on screen, once at capture | Quantization table inconsistency analysis; JPEG ghost detection | Strong signal when present; absence does not rule out L3 attack (PNG capture path has no JPEG artifacts) |

**SDB-26 class:** `SCREENSHOT`  
**Typical confidence range when codes present:** 0.65–0.90  
**Why L3 is hardest to detect:** A screen photo of a genuine document carries valid device EXIF from the capturing device. C2PA provenance chain is absent but that alone is a weak signal. Only intrinsic image signals (moiré, subpixel grid, compression artifacts) reliably distinguish L3 from genuine capture.

---

## Level INF — Insufficient Quality

Codes indicating the image quality or data availability is insufficient for reliable forensic analysis. **Honest uncertainty is preferable to a low-confidence verdict.**

| Code | Signal | Action |
|------|--------|--------|
| `FRC-INF-LOW-RESOLUTION` | Resolution below 150 DPI — micro-artifact analysis impossible | Request re-submission at ≥ 300 DPI |
| `FRC-INF-MOTION-BLUR` | Excessive motion blur — impossible to distinguish AI noise from capture defect | Request re-capture |
| `FRC-INF-EXIF-ABSENT` | No EXIF metadata present — cannot assess provenance chain | Note: absence alone is not a fraud signal; many legitimate capture pipelines strip EXIF. Combine with other signals |
| `FRC-INF-PARTIAL-DOCUMENT` | Only partial document visible — key security features outside analysis frame | Request full document re-submission |
| `FRC-INF-GLARE-OBSTRUCTION` | Severe glare obscuring document security features | Request re-capture under different lighting |

**SDB-26 class:** `INSUFFICIENT`  
**Handling:** INSUFFICIENT should route to human review or guided re-capture — never to automatic approval. Document INSUFFICIENT handling policy in your runbook.

---

## Multi-Code Combinations

FRC codes are additive. Multiple codes from different levels indicate compound attack or compounding evidence.

**High-confidence combinations:**

| Combination | Interpretation | Typical confidence |
|------------|---------------|-------------------|
| `FRC-L3-MOIRE-PATTERN` + `FRC-L2-METADATA-WIPE` | Screen photo of an edited document | 0.85–0.95 |
| `FRC-L1-FFT-GRID` + `FRC-L1-GEN-TEXTURE-UNIFORM` | Multiple convergent L1 signals — strong synthetic indicator | 0.88–0.97 |
| `FRC-L2-ELA-DIVERGENCE` + `FRC-L2-FONT-INCONSISTENCY` | Dual manipulation signals — high confidence edit | 0.80–0.92 |
| `FRC-L3-DOUBLE-COMPRESSION` + `FRC-L3-RGB-SUBPIXEL-GRID` | Screen capture with sub-pixel evidence | 0.82–0.93 |

**Cross-level codes:** When L1 and L3 codes co-occur (e.g. AI-generated document photographed from screen), primary classification is L3 (screen attack) with L1 as corroborating signal.

---

## Example API Response

```json
{
  "document_id": "DOC-2026-001",
  "verdict": "FRAUD",
  "verdict_confidence": 0.89,
  "required_action": "manual_review",
  "primary_codes": [
    "FRC-L3-MOIRE-PATTERN",
    "FRC-L2-METADATA-WIPE"
  ],
  "supporting_codes": [
    "FRC-L1-GEN-TEXTURE-UNIFORM"
  ],
  "forensic_note": "Moiré interference pattern detected on document security layer. File creation software signature consistent with Adobe products; original camera metadata absent. High probability: screen photo attack (document photographed from monitor). Secondary signal: paper texture uniformity inconsistent with physical document scan.",
  "sdb26_class": "SCREENSHOT",
  "attack_level": "L3",
  "sdb26_version": "SDB-26-v1.0",
  "model_trace": {"detector_version": "1.0.0", "pipeline_id": "prod-kyc-v1"},
  "evaluated_at": "2026-04-24T14:23:11Z",
  "frc_schema_version": "1.0.0"
}
```

---

## Versioning and Corpus Dependency

FRC codes are versioned alongside the SDB-26 corpus. New generative model releases may introduce new artifact signatures requiring new codes or updated detection thresholds.

**Current version:** FRC-1.0 (April 2026)  
**Corpus alignment:** SDB-26-v1.0  
**Model signatures included:** SDXL 1.0, SD 1.5, Midjourney v6, DALL-E 3, ChatGPT Image 2, Seedream 5 Lite, Kling O1 Image, Flux 2, Nano Banana 2, screenshot simulation pipeline

When a new generative model produces artifacts not covered by existing FRC codes, a new code is proposed via GitHub issue with:
- Corpus examples (minimum 20 confirmed instances)
- Detection method description
- False positive rate estimate on genuine document control set

---

## Limitations and Honest Uncertainty

FRC codes represent probabilistic forensic signals — not legal proof. Several important constraints apply:

- **Absence of FRC codes ≠ GENUINE.** A document may be synthetic without triggering any current FRC code if it uses a novel generation method outside the current corpus.
- **FRC-L1-GEN-TEXTURE-UNIFORM** requires a reference PRNU library for the claimed capture device. Without this library, the signal is weakened.
- **FRC-L1-SEM-INCOHERENCE** is a data validation signal, not image forensics. It should be treated as corroborating evidence, not a standalone fraud indicator.
- **FRC-INF codes** indicate the analysis is inconclusive — not that the document is genuine. INSUFFICIENT should always escalate, never auto-approve.
- Detector performance (BR/FPR) varies by document type, jurisdiction, and generator. Metrics should be measured on your specific document mix using SDB-26 methodology.

---

*SDB-26 Forensic Reason Codes — v1.0*  
*github.com/sevrusik/SDB26 · sdb26.com*  
*Not legal advice. Forensic signals are probabilistic indicators, not legal determinations.*
