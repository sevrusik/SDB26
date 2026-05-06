# SDB-26 Measurement Methodology

**Detailed technical guidance for evaluators**  
**Version:** 1.0 | **April 2026**

---

## Overview

This document provides detailed technical guidance for organisations conducting SDB-26 evaluations. It supplements the formal standard defined in [STANDARD.md](STANDARD.md).

---

## Why These Metrics

### Why Bypass Rate and not Accuracy?

Overall accuracy is misleading for imbalanced detection tasks. A system that approves everything has 50% accuracy on a balanced corpus — but 100% Bypass Rate. Accuracy hides the asymmetric cost of false negatives in fraud detection.

Bypass Rate isolates the metric that matters for compliance: what percentage of fraud gets through?

### Why Confidence Gap?

Bypass Rate tells you whether the system fails. Confidence Gap tells you how dangerously it fails.

A system that says "suspicious, 51% confidence" on a synthetic document it approves gives a human reviewer a chance to intervene. A system that says "genuine, 97% confidence" on the same document actively misleads the reviewer.

In our testing, Claude 3 Haiku returned 90-100% confidence on high-quality AI-generated passports it incorrectly classified as genuine. This is a maximal Confidence Gap — the system was most confident where it was most wrong.

### Why Generator Sensitivity?

Fraudsters will use the tool the system cannot detect. Generator Sensitivity reveals which specific tools a system is blind to, allowing organisations to understand their specific exposure rather than relying on aggregate metrics that may obscure critical gaps.

---

## Corpus Design Rationale

### Why Three Levels?

The three levels map to the actual threat landscape in 2026:

**Level 1** represents the democratised threat — tools anyone can access. If a system cannot handle Level 1, it is not production-ready.

**Level 2** represents the professional threat — tools requiring knowledge and effort. This is where most current systems begin to fail.

**Level 3** represents the structural threat — the Screenshot Attack that bypasses C2PA and provenance standards by design. No provenance-based system can address Level 3. Only physics-based forensic analysis can.

### Why Include Genuine Documents?

False Positive Rate is as important as Bypass Rate for production KYC. A system with 0% BR and 50% FPR cannot be deployed — it would reject half of legitimate customers.

SDB-26 requires FPR reporting to prevent systems from being optimised for BR at the expense of usability.

---

## The Screenshot Attack — Technical Detail

The Screenshot Attack (Level 3) is the most important level in SDB-26 because it is the level at which all current provenance-based defences fail.

### Mechanism

1. A synthetic document is generated at Level 1 or Level 2
2. The document is displayed on a screen (computer monitor, tablet, phone)
3. A mobile device photographs the screen, producing a new JPEG file
4. The new file has:
   - No C2PA signature (the chain is broken)
   - No AI generation markers in EXIF
   - Plausible device metadata from the photographing device
   - Real JPEG compression artifacts from the capture process

### Why Provenance Standards Fail

C2PA attaches provenance to the file at creation. The screenshot produces a new file. The new file has no provenance record — not a broken one, but an absent one.

A system checking for C2PA signatures on a Level 3 document finds nothing suspicious. The file looks like it was taken by a phone camera. Because it was — of a screen displaying a fake.

### What Detects Level 3

Physics-based forensic analysis examines the spectral properties of the image itself, not the metadata surrounding it. Key signals:

- **Moiré patterns:** When a digital screen is photographed, the pixel grid of the screen interferes with the sensor grid of the camera, producing characteristic frequency domain patterns
- **Double compression artifacts:** The image has been compressed twice — once by the generation process, once by the device camera — producing DCT coefficient distributions different from single-capture images
- **Screen reflection artifacts:** Depending on conditions, screen curvature and reflection introduce subtle distortions detectable in frequency analysis
- **Pixel grid regularity:** Screen pixels have a regular grid structure that differs from the noise structure of optical sensors

These signals are present even in high-quality screen captures and cannot be removed without degrading the image to the point of uselessness for fraud purposes.

---

## Evaluation Procedure — Step by Step

### Step 1: Corpus Preparation

1. Request corpus access: sevrusik@gmail.com
2. Verify SHA-256 hashes of received files against the corpus manifest
3. Record corpus version number
4. Do not pre-process or modify corpus files

### Step 2: System Configuration

1. Document the system under test: name, version, API mode, configuration
2. Ensure the system is in standard production configuration
3. Document any configuration that differs from production

### Step 3: Submission

Submit each document to the system under test individually. Record:

```json
{
  "document_id": "SDB26_L1_MEX_001",
  "verdict": "genuine",
  "confidence": 0.94,
  "processing_time_ms": 2340,
  "raw_response": { ... }
}
```

### Step 4: Metric Calculation

Calculate metrics per the formulas in STANDARD.md Section 4.

Recommended calculation order:
1. Separate results by level (L1, L2, L3)
2. Separate results by document type within each level
3. Separate results by generator within each level
4. Calculate BR, CG, GS for each grouping
5. Calculate FPR from genuine document control set

### Step 5: Results File

Complete the JSON results file per the schema in [results_schema.json](results_schema.json).

If your implementation supports explainable decision output, validate forensic payloads against [schemas/frc_schema_v1_0_0.json](schemas/frc_schema_v1_0_0.json) and use examples in `examples/frc/`.  
This repository ships [scripts/validate_frc_schemas.py](scripts/validate_frc_schemas.py) (with [requirements-dev.txt](requirements-dev.txt)) to re-check `tests/frc/` fixtures and the A2A envelope example in CI or locally.

### Step 6: Publication (Optional)

Publish results to your organisation's public channels. Include the JSON results file or link to it.

Notify sevrusik@gmail.com if publishing, to be included in the public results registry.

---

## Worked Example

### Setup

- System under test: FraudLens v2.0 (FFT forensic mode)
- Corpus: SDB-26 v1.0
- Level: L2 (Mexican AI-generated passports, n=94)

### Submission Results

```
Total documents submitted: 94
Synthetic documents: 94 (ground truth)
Genuine documents: 0 (control set tested separately)

Verdicts received:
  AI-generated: 94
  Genuine: 0
  Insufficient quality: 0
  Error: 0
```

### Metric Calculation

```
BR = FN / (FN + TP) × 100
   = 0 / (0 + 94) × 100
   = 0.0%

CG = N/A (no false negatives)

Average confidence: 74% (PAID mode)
Average processing time: 2.5 seconds per document
```

### Results File

```json
{
  "benchmark": "SDB-26",
  "version": "1.0",
  "system": "FraudLens",
  "system_version": "2.0",
  "mode": "PAID",
  "date": "2026-04",
  "level": "L2",
  "document_type": "passport",
  "country": "MEX",
  "samples": 94,
  "bypass_rate": 0.0,
  "confidence_gap": null,
  "mean_confidence_correct": 0.74,
  "fpr": "tested_separately"
}
```

---

## Common Evaluation Errors

**Error 1: Testing only L1**
A system that handles L1 but not L3 is not adequately characterised. Always test all levels.

**Error 2: Not including genuine documents**
BR without FPR is incomplete. Include the genuine document control set.

**Error 3: Custom configuration for evaluation**
The system must be evaluated as deployed. Tuning specifically for the benchmark invalidates results.

**Error 4: Reporting aggregate accuracy instead of BR**
Overall accuracy on a balanced corpus does not reveal the fraud-specific failure rate. Report BR.

**Error 5: Not recording confidence scores**
Confidence Gap requires confidence scores for each verdict. Ensure your integration captures this.

---

## Frequently Asked Questions

**Q: Can we test our system internally without publishing results?**
A: Yes. SDB-26 is designed for both internal evaluation and public reporting. Internal use does not require publication.

**Q: What if our system returns "suspicious" rather than binary verdicts?**
A: Map "suspicious" to whichever category your system treats it as for action purposes. If suspicious triggers manual review rather than automatic approval, it counts as a True Positive for BR purposes.

**Q: Can we use SDB-26 to compare two different vendor systems?**
A: Yes. This is an intended use case. Ensure both systems are evaluated on the same corpus version with the same configuration documentation.

**Q: Is the corpus representative of real-world fraud?**
A: The corpus is designed to be representative of the tools and techniques available in 2026. It will be updated as generation techniques evolve. No corpus can be exhaustive — SDB-26 provides a standardised baseline, not a guarantee of comprehensive coverage.

**Q: What happens when new AI generators emerge?**
A: New generators are added to the corpus in minor version updates (1.x). Results from different minor versions are comparable; the new generators appear as additional rows in Generator Sensitivity.

---

## Submission Channel Constraints

*Added in preparation for SDB-26 v1.1. Reflects agentic payment infrastructure context (AP2, x402, MPP).*

Different submission channels affect which forensic signals are available for analysis. Evaluators should document the submission channel alongside corpus results.

### Traditional KYC API
Standard REST API submission with multipart file upload. Full forensic signal set available: EXIF metadata, PDF container structure, pixel-level analysis, PRNU. This is the reference channel for SDB-26 baseline results.

### HTTP x402 (Coinbase protocol)
Documents submitted via HTTP 402 payment-gated endpoints. Key constraint: x402 flows may not preserve end-to-end capture provenance in integration logs. **Impact:** `FRC-L2-METADATA-WIPE` is weakened as a standalone indicator and should be paired with pixel-level signals (FFT, ELA) for reliable classification.

### MPP (Stripe/Tempo Merchant Payment Protocol)
Stablecoin-native submission channel. Supports both fiat and on-chain settlement. Metadata preservation depends on merchant implementation. **Impact:** evaluators should verify whether EXIF is preserved end-to-end before relying on provenance-based signals. Document channel configuration in the results file.

### Agent-mediated submission (agentic onboarding)
Documents submitted by an AI agent acting on behalf of a principal. Two additional constraints apply:

1. **Temporal signal availability:** Agent submission pipelines may batch-process documents, introducing artificial delays between file creation and submission. Calibrate `FRC-L0-TEMPORAL-ANOMALY` thresholds by use case.
2. **Velocity baseline:** Legitimate bulk onboarding agents may have naturally high submission rates. Establish per-use-case velocity baselines before activating `FRC-L0-VELOCITY-FLAG`.

**Recommendation:** add `submission_channel` as a reported field in results JSON (`"api" | "x402" | "mpp" | "agent"`). This enables channel-stratified metrics in v1.1.

---

## Compound Attack Taxonomy

*Added in preparation for SDB-26 v1.1. Addresses simultaneous document-layer and agent-layer attacks.*

SDB-26 v1.0 defines three document attack levels (L1, L2, L3) evaluated independently of submission context. As agentic infrastructure matures, a new attack class emerges: **compound attacks**, where document-layer and agent-layer signals indicate coordinated risk in the same submission.

### Definition
A compound attack occurs when:
- The submitted document is SYNTHETIC, EDITED, or SCREENSHOT (L1-L3), **and**
- The submitting context contains L0 risk flags (for example UNATTESTED, SUSPICIOUS, or broken delegation chain indicators)

### Why This Matters
In a compound attack, document and agent signals are independently detectable, but risk is underestimated if either layer is evaluated in isolation.

The compound verdict matrix (from FRC A2A Extension v0.3) handles this explicitly: any SYNTHETIC / EDITED / SCREENSHOT document defaults to `BLOCK` regardless of agent status.

### Measurement
Compound attacks are measured as a separate slice in SDB-26 v1.1 results:

```json
{
  "compound_attack_rate": {
    "description": "share of submissions with both L1-L3 document fraud and L0 risk flags",
    "n": 0,
    "rate": null,
    "note": "requires A2A instrumentation"
  }
}
```

This metric is optional in v1.0 reporting and planned as required for v1.1 evaluations that instrument the A2A layer.

### Relationship to Existing Metrics
- **BR (Bypass Rate)** remains the primary document-layer metric
- **ABR (Agent Bypass Rate)** is the primary agent-layer metric
- **Compound Attack Rate** measures cross-layer co-occurrence

When A2A instrumentation is available, evaluators should report all three.
