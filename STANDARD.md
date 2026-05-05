# SDB-26 Standard Document

**The 2026 Synthetic Document Benchmark**  
**Version:** 1.0  
**Date:** April 2026  
**Author:** Ruslan Mishyn  
**Status:** Public Draft

---

## 1. Scope

This standard defines a methodology for evaluating the effectiveness of document verification systems against AI-generated and synthetically manipulated documentary evidence.

SDB-26 applies to:
- Identity document verification systems (KYC)
- Document authenticity verification in financial services
- Any system that accepts documentary evidence as input

SDB-26 does not evaluate:
- Biometric liveness detection
- Sanctions or PEP screening
- Transaction monitoring

This standard is complemented by FRC (Forensic Reason Codes) documentation for explainable decision outputs:
- `docs/FRC_OVERVIEW.md`
- `docs/FRC_SCHEMA.md`
- `docs/FRC_CODEBOOK.md`
- `docs/FRC_ACTION_MATRIX.md`
- `schemas/frc_schema_v1_0_0.json`

---

## 2. Definitions

**Synthetic document:** Any document image produced by a generative AI model, including but not limited to diffusion models, GANs, and large multimodal models, whether or not subsequently post-processed.

**Screenshot attack:** The process of capturing a synthetic document via a screen capture device (mobile phone, tablet, desktop screenshot tool) to strip provenance metadata and C2PA signatures, producing a new file without AI generation markers.

**Bypass Rate (BR):** The percentage of synthetic documents in a given test set that receive an "approved," "genuine," or equivalent positive verdict from the system under test.

**Confidence Gap (CG):** The mean confidence score assigned by the system under test to synthetic documents that it incorrectly approves.

**Generator Sensitivity (GS):** The Bypass Rate calculated separately for each AI generation tool represented in the test corpus.

**System under test (SUT):** The document verification system, API, or model being evaluated against SDB-26.

**Ground truth:** The known classification of each document in the test corpus — synthetic or genuine — established at corpus creation.

---

## 3. Test Corpus Specification

### 3.1 Corpus Structure

The SDB-26 test corpus is organised into three levels of synthetic complexity.

#### Level 1 — Standard Generation

Documents produced by general-purpose image generation models without post-processing optimisation.

| Parameter | Specification |
|-----------|--------------|
| Generators | DALL-E 3, Midjourney v6, Stable Diffusion XL, ChatGPT Image 2, Seedream 5 Lite, Kling O1 Image, Flux 2 (standard config) |
| Document types | Passport (minimum 3 countries), National ID (minimum 2 countries) |
| Minimum samples | 30 per generator per document type |
| Post-processing | None permitted |
| Resolution | Minimum 512×512 pixels |
| Format | JPEG or PNG |

#### Level 2 — Advanced Diffusion

Documents produced by fine-tuned or specialised generation pipelines with metadata injection.

| Parameter | Specification |
|-----------|--------------|
| Generators | Fine-tuned diffusion models, specialised ID generation tools |
| Document types | Passport, National ID, Bank statement, Invoice |
| Minimum samples | 30 per generator per document type |
| Post-processing | Metadata injection permitted (camera model, timestamp, device info) |
| Resolution | Minimum 512×512 pixels |
| Format | JPEG with injected EXIF |

#### Level 3 — Screenshot Attack

Documents produced by any generation method, then captured via screenshot.

| Parameter | Specification |
|-----------|--------------|
| Source documents | Any Level 1 or Level 2 document |
| Capture method | Screen capture via mobile device (minimum 2 different devices) |
| Device types | iOS and Android represented |
| Minimum samples | 50 total |
| Post-processing | No additional processing after screenshot permitted |
| Format | JPEG (as produced by device camera roll) |

### 3.2 Genuine Document Control Set

Each SDB-26 evaluation must include a genuine document control set to measure False Positive Rate.

| Parameter | Specification |
|-----------|--------------|
| Document types | Same types as synthetic corpus |
| Minimum samples | Equal to synthetic corpus size |
| Source | Camera-captured originals with full EXIF |
| Verification | Ground truth verified by human review |

### 3.3 Corpus Integrity

- All documents in the corpus are assigned a unique identifier
- SHA-256 hash of each document is recorded at corpus creation
- Ground truth labels are stored separately from the corpus files
- Corpus version is recorded with each evaluation

---

## 4. Measurement Methodology

### 4.1 Bypass Rate (BR)

**Formula:**

```
BR = FN / (FN + TP) × 100
```

Where:
- FN = False Negatives (synthetic documents approved as genuine)
- TP = True Positives (synthetic documents correctly flagged)

**Reporting requirements:**
- BR must be reported per level (L1, L2, L3)
- BR must be reported per document type
- BR must be reported per generator (Generator Sensitivity)
- Overall BR across all levels must be reported

### 4.2 Confidence Gap (CG)

**Formula:**

```
CG = mean(confidence_score[i]) for all i where:
  verdict[i] = "genuine" AND ground_truth[i] = "synthetic"
```

**Reporting requirements:**
- CG must be reported as mean ± standard deviation
- CG must be reported per level
- If no false negatives exist at a level, CG is reported as N/A

### 4.3 Generator Sensitivity (GS)

**Formula:**

```
GS[generator] = BR calculated using only documents from that generator
```

**Reporting requirements:**
- GS must be reported for each generator represented in the corpus
- Results must be presented as a ranked table (highest to lowest BR)

### 4.4 False Positive Rate (FPR)

**Formula:**

```
FPR = FP / (FP + TN) × 100
```

Where:
- FP = False Positives (genuine documents flagged as synthetic)
- TN = True Negatives (genuine documents correctly approved)

**Reporting requirements:**
- FPR must be reported alongside BR
- A system optimised only for BR at the expense of FPR is not compliant with SDB-26 reporting standards

### 4.5 Planned v1.1 Agent-layer and Compound Metrics (Preview)

The following metrics are defined as v1.1 planned additions and are non-normative for v1.0 compliance. They are aligned with the FRC A2A extension and intended for early adopters.

**Agent Bypass Rate (ABR_strict):**

```
ABR_strict = N(L0_high_risk AND compound_verdict = "TRUSTED")
             / N(L0_high_risk)
```

**Agent Confidence Gap (ACG):**

```
ACG = mean(verdict_confidence[i]) for i where:
  L0_high_risk[i] = true AND compound_verdict[i] = "TRUSTED"
```

**Chain Depth Rate (CDR):**

```
CDR[k] = share of submissions with delegation_chain_depth = k
```

**Signal tiering for v1.1 reporting:**
- `L0_any`: any L0 signal present
- `L0_high_risk`: high-risk L0 subset defined by policy (for ABR/ACG denominator)

**Compound Attack Rate (planned):**

```
compound_attack_rate =
  N((document_class in {SYNTHETIC, EDITED, SCREENSHOT}) AND L0_any)
  / N(total submissions)
```

v1.1 reporting is expected to include BR (document layer), ABR/ACG/CDR (agent layer), and compound attack rate (cross-layer).

---

## 5. Evaluation Procedure

### 5.1 System Configuration

The system under test must be evaluated in its standard production configuration. Custom configurations or parameter adjustments specifically for the SDB-26 evaluation are not permitted unless disclosed.

### 5.2 Document Submission

Documents must be submitted to the system under test in the same format as they would be submitted in production use. No pre-processing of test documents is permitted unless the SUT applies the same pre-processing to all production documents.

### 5.3 Verdict Collection

The evaluation must collect:
- Binary verdict (genuine / synthetic / suspicious / insufficient quality)
- Confidence score (0.0 to 1.0 or 0 to 100)
- Processing time per document

### 5.4 Corpus Blinding

The system under test must not be trained or fine-tuned on SDB-26 corpus documents prior to evaluation. Evaluations conducted after training on corpus documents must be disclosed as such.

---

## 6. Reporting Format

Results must be reported using the standard JSON schema defined in [results_schema.json](results_schema.json).

Required fields:
- benchmark version
- system under test (name and version)
- evaluation date
- corpus version used
- results per level
- generator sensitivity table
- false positive rate
- evaluator (self-evaluated or third-party)

Optional fields:
- processing time statistics
- hardware configuration
- API mode (free / paid / enterprise)

---

## 7. Publication Standards

Organisations publishing SDB-26 results must:

1. Use the standard JSON schema
2. Disclose whether evaluation was self-conducted or third-party
3. Disclose the corpus version used
4. Not selectively report levels (all levels tested must be reported)
5. Include FPR alongside BR

Organisations may not:
- Claim "SDB-26 certified" without publishing full results
- Publish partial results without disclosing that other levels were not tested
- Modify the corpus and publish results as SDB-26 compliant

---

## 8. Versioning Policy

| Version | Change type | Description |
|---------|-------------|-------------|
| 1.x | Minor | Addition of new generators or document types to corpus |
| 2.0 | Major | Changes to metric definitions or measurement methodology |

Previous version results remain valid and comparable within the same major version.

Results from different major versions are not directly comparable and must be reported separately.

---

## 9. Governance

SDB-26 v1.0 is maintained by Ruslan Mishyn.

Contributions, corrections, and proposals for future versions are welcomed via GitHub pull request or email to sevrusik@gmail.com.

The benchmark governance model will be reviewed when the first external organisation publishes SDB-26 results. Independent governance is the long-term goal.

---

## 10. Legal

SDB-26 methodology is published under Creative Commons Attribution 4.0 International (CC BY 4.0).

The test corpus is not included in this license. Corpus access is provided to verified organisations under separate terms.

Use of the name "SDB-26" to describe non-compliant evaluations or modified methodologies is not permitted.

---

## Appendix A: Generator Classification Matrix

### Tier 1 — Publicly Available Tools (Level 1 Corpus)

*Accessible to any user without specialist knowledge*

| Tool | Type | Forgery Complexity | Detectability |
|------|------|--------------------|---------------|
| Midjourney v6 | Diffusion model | Medium | FFT fingerprint |
| DALL-E 3 | Diffusion model | Medium | Spectral artifacts |
| Stable Diffusion XL | Open source | Medium | GAN/diffusion markers |
| ChatGPT Image 2 | Multimodal generator | Medium | Pipeline markers |
| Seedream 5 Lite | Diffusion model | Medium | Frequency-domain artifacts |
| Kling O1 Image | Multimodal generator | Medium | Cross-model texture signatures |
| Adobe Firefly | Commercial | Medium | C2PA present |
| Canva AI | Commercial | Low | Visible artifacts |
| ChatGPT 4o Image | Multimodal | Medium | Pipeline markers |

**Tier 1 Characteristics:**
- Visible artifacts under forensic analysis
- Absent or minimal EXIF
- Standard spectral signatures
- Detectable by standard forensic tools

---

### Tier 2 — Specialised Tools (Level 2 Corpus)

*Require technical knowledge or specialist access*

| Tool | Type | Forgery Complexity | Detectability |
|------|------|--------------------|---------------|
| Stable Diffusion + LoRA (ID trained) | Fine-tuned | High | Residual artifacts |
| ComfyUI + custom workflow | Open source pipeline | High | Pipeline mismatch |
| Flux.1 | Advanced diffusion | High | Frequency anomalies |
| Flux 2 | Advanced diffusion | High | Frequency anomalies |
| Nano Banana 2 | Fine-tuned image generator | High | Residual generation artifacts |
| Specialised ID generators | Closed tools | Very high | PRNU analysis |
| FaceSwap + template | Hybrid method | High | Face-document mismatch |
| Inpainting (partial replacement) | Editing | Very high | ELA analysis |

**Tier 2 Characteristics:**
- Minimal visual artifacts
- Injected metadata from real device
- Convincing file structure
- Requires advanced forensic analysis

---

### Tier 3 — Advanced Techniques (Level 3 Corpus)

*Structurally bypass standard defences*

| Technique | Bypass Mechanism | What It Bypasses | Detectability |
|-----------|-----------------|------------------|---------------|
| Screenshot Attack (iOS) | New file without C2PA | C2PA, EXIF, AI markers | Moiré patterns, double compression |
| Screenshot Attack (Android) | New file without C2PA | C2PA, EXIF, AI markers | Screen grid artifacts |
| Print & Rescan | Physical analog gap | All digital markers | Scanner noise patterns |
| Screen recording frame | Video frame extraction | Metadata | Compression artifacts |
| Virtual camera injection | Stream substitution | Liveness detection | Pipeline inconsistency |

**Tier 3 Characteristics:**
- No AI markers in metadata
- Plausible device fingerprint from capture device
- Complete bypass of C2PA chain of custody
- Detectable only through physical forensic analysis

---

### Forgery Complexity Matrix

```
Complexity     Tier  Tool                    Time        Cost
──────────────────────────────────────────────────────────────
Low            1     Canva AI                2 min       Free
Low            1     ChatGPT 4o Image        2 min       ~$0.10
Medium         1     ChatGPT Image 2         3 min       ~$0.12
Medium         1     Midjourney v6           5 min       ~$0.50
Medium         1     DALL-E 3                5 min       ~$0.08
Medium         1     Seedream 5 Lite         5 min       ~$0.10
Medium         1     Kling O1 Image          5 min       ~$0.12
High           2     SD + LoRA               30 min      Free
High           2     Flux.1                  15 min      ~$0.20
High           2     Flux 2                  15 min      ~$0.25
High           2     Nano Banana 2           20 min      ~$0.20
Very High      2     Specialised ID tool     1 hour      $5-50
Structural     3     Screenshot Attack       1 min       Free
Structural     3     Print & Rescan          10 min      ~$0.10
```

**Key insight:** The most dangerous forgeries are the cheapest. The Screenshot Attack costs $0, takes 1 minute, completely bypasses C2PA, and is detectable only through physical forensic analysis.

---

## Appendix B: Detection Methods Matrix

### What Each Method Detects

| Detection Method | Tier 1 | Tier 2 | Tier 3 | Description |
|-----------------|--------|--------|--------|-------------|
| **Template matching** | ⚠️ Partial | ❌ No | ❌ No | Document template conformity check |
| **EXIF validation** | ⚠️ Partial | ⚠️ Partial | ❌ No | File metadata verification |
| **C2PA / provenance** | ✅ Yes | ✅ Yes | ❌ No | File chain of custody |
| **Liveness detection** | ⚠️ Partial | ⚠️ Partial | ❌ No | Live presence verification |
| **Vision AI (Claude/GPT)** | ❌ No | ❌ No | ❌ No | Visual content analysis |
| **GAN fingerprint** | ✅ Yes | ⚠️ Partial | ⚠️ Partial | Generative network signature |
| **FFT spectral analysis** | ✅ Yes | ✅ Yes | ✅ Yes | Frequency domain analysis |
| **PRNU sensor noise** | ✅ Yes | ✅ Yes | ✅ Yes | Camera sensor noise signature |
| **ELA (Error Level Analysis)** | ✅ Yes | ✅ Yes | ⚠️ Partial | Compression error level analysis |
| **Pipeline mismatch** | ✅ Yes | ✅ Yes | ⚠️ Partial | Processing pipeline inconsistency |
| **Moiré pattern detection** | ❌ No | ❌ No | ✅ Yes | Screen-sensor interference patterns |
| **Double compression** | ❌ No | ❌ No | ✅ Yes | Dual compression artifacts |
| **Scanner stripe detection** | N/A | N/A | ✅ Yes | FFT carriage movement patterns |

**Legend:**
- ✅ Yes — reliably detects
- ⚠️ Partial — detects in some cases
- ❌ No — does not detect

---

### Critical Finding

```
Only methods that detect ALL three levels:
✅ FFT spectral analysis
✅ PRNU sensor noise analysis

Methods blind to ALL levels:
❌ Vision AI (Claude 3 Haiku, GPT-4V, and equivalents)

Methods blind to Level 3 (Screenshot Attack):
❌ Template matching
❌ EXIF validation
❌ C2PA / provenance
❌ Liveness detection
❌ GAN fingerprint (partial)
```

**Practical implication for compliance teams:**

If your KYC stack does not include FFT spectral analysis or PRNU analysis, you have 0% protection against Level 3 attacks — regardless of the quality of other components.

---

### Minimum Recommended Stack for Production KYC (2026)

```
Layer 1: Template + EXIF validation    → baseline protection (Tier 1)
Layer 2: C2PA provenance check         → protection against unsophisticated forgeries
Layer 3: GAN/diffusion fingerprint     → protection against Tier 1-2
Layer 4: FFT + PRNU forensic physics   → protection against all levels including L3
Layer 5: Human review for flagged      → final verification
```

Absence of Layer 4 means structural blindness to the Screenshot Attack — the most accessible and prevalent technique in 2026.
