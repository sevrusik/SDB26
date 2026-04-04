# SDB-26: The 2026 Synthetic Document Benchmark

**Version:** 1.0  
**Released:** April 2026  
**Author:** Ruslan Mishyn  
**Status:** Public Draft  
**Contact:** sevrusik@gmail.com

---

## What is SDB-26?

SDB-26 is the first open benchmark for testing document verification systems against AI-generated documentary fraud.

The KYC industry has no independent standard for measuring what percentage of synthetic documents pass through a given verification stack undetected. SDB-26 fills this gap.

---

## The Problem

Vision AI models — including leading commercial systems — consistently classify high-quality AI-generated identity documents as genuine with 90-100% confidence.

Forensic physics analysis detects the same documents with 100% recall.

The gap between these two results is not marginal. It is total. And it is undetected by current industry benchmarks because no current industry benchmark exists.

---

## What SDB-26 Measures

Three metrics that vendor marketing does not report:

| Metric | Definition |
|--------|-----------|
| **Bypass Rate (BR)** | % of synthetic documents incorrectly approved |
| **Confidence Gap (CG)** | Mean confidence assigned to incorrectly approved synthetic documents |
| **Generator Sensitivity (GS)** | BR broken down by AI generation tool |

---

## Three Levels of Synthetic Complexity

| Level | Name | Description |
|-------|------|-------------|
| L1 | Standard Generation | DALL-E 3, Midjourney, SD XL — no post-processing |
| L2 | Advanced Diffusion | Fine-tuned models, metadata injection |
| L3 | Screenshot Attack | Any L1/L2 document captured via screenshot — bypasses C2PA |

---

## Our Baseline Results (FraudLens v2.0, April 2026)

| System | L1 BR | L2 BR | L3 BR |
|--------|--------|--------|--------|
| Claude 3 Haiku (Vision AI) | 100% | 100% | pending |
| FraudLens FFT Forensics | 0% | 0% | pending |

Full results: [RESULTS/fraudlens_v2_2026-04.json](RESULTS/fraudlens_v2_2026-04.json)

---

## Quick Start

**For compliance teams:**
1. Request the test corpus: sevrusik@gmail.com
2. Run your current verification stack against the corpus
3. Report results using the [standard JSON schema](SCHEMA/results_schema.json)

**For vendors:**
1. Read [STANDARD.md](STANDARD.md) for full methodology
2. Request corpus access for verified organisations
3. Publish your results — transparency builds trust

**For researchers:**
1. Read [METHODOLOGY.md](METHODOLOGY.md)
2. Contribute via pull request
3. Propose new document categories or generators

---

## Repository Structure

```
SDB-26/
├── README.md           — This file
├── STANDARD.md         — Full standard document
├── METHODOLOGY.md      — Detailed measurement methodology  
├── RESULTS/
│   └── fraudlens_v2_2026-04.json
├── SCHEMA/
│   └── results_schema.json
└── CHANGELOG.md
```

---

## Citation

If you use SDB-26 in research or product evaluation, please cite:

```
Mishyn, R. (2026). SDB-26: The 2026 Synthetic Document Benchmark.
Retrieved from https://github.com/sevrusik/SDB-26
```

---

## License

Methodology: Creative Commons Attribution 4.0 International (CC BY 4.0)  
You may use, share, and adapt the methodology with attribution.

Test corpus: Available to verified organisations on request. Not for public distribution.

---

*SDB-26 was developed in parallel with a technical response to the AMLA public consultation on draft CDD Regulatory Technical Standards (Article 28(1) of Regulation (EU) 2024/1624), proposing forensic image physics analysis as a mandatory verification layer.*
