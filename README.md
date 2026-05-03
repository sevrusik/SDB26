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

### v1.1 Planned Extensions (Preparation)

SDB-26 v1.1 planning introduces agent-layer and cross-layer reporting additions. These additions are planned and non-normative for v1.0 compliance.

- **ABR / ACG / CDR** formalization in `STANDARD.md`
- **Signal tiering:** `L0_any` vs `L0_high_risk`
- **Submission-channel aware reporting:** `submission_channel` in `results_schema.json`
- **Cross-layer co-occurrence metric:** `compound_attack_rate`

See implementation guidance in `METHODOLOGY.md`:
- `Submission Channel Constraints`
- `Compound Attack Taxonomy`

---

## FRC Package (v1.0)

SDB-26 now includes a Forensic Reason Codes (FRC) package for explainable, audit-ready decision outputs.

- Overview: [docs/FRC_OVERVIEW.md](docs/FRC_OVERVIEW.md)
- Human-readable schema: [docs/FRC_SCHEMA.md](docs/FRC_SCHEMA.md)
- Code dictionary: [docs/FRC_CODEBOOK.md](docs/FRC_CODEBOOK.md)
- Action policy mapping: [docs/FRC_ACTION_MATRIX.md](docs/FRC_ACTION_MATRIX.md)
- JSON Schema: [schemas/frc_schema_v1_0_0.json](schemas/frc_schema_v1_0_0.json)
- Valid examples: [examples/frc](examples/frc)
- CI fixtures (valid/invalid): [tests/frc](tests/frc)

Advanced extension draft for agent-to-agent contexts:
- [docs/FRC_A2A_EXTENSION.md](docs/FRC_A2A_EXTENSION.md) (v0.1.1 clarifications)

Implementation note — how SDB-26 maps onto ENISA *Secure by Design and Default* (consultation playbook):
- [docs/SDB26_ENISA_SecureByDesign_Mapping_v0.1.md](docs/SDB26_ENISA_SecureByDesign_Mapping_v0.1.md)

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

Full results: [fraudlens_v2_2026-04.json](fraudlens_v2_2026-04.json)

---

## Quick Start

**For compliance teams:**
1. Request the test corpus: sevrusik@gmail.com
2. Run your current verification stack against the corpus
3. Report results using the [standard JSON schema](results_schema.json)

**For vendors:**
1. Read [STANDARD.md](STANDARD.md) for full methodology
2. Request corpus access for verified organisations
3. Publish your results — transparency builds trust
4. Optionally output explainable verdicts using [FRC schema](schemas/frc_schema_v1_0_0.json)

**For researchers:**
1. Read [METHODOLOGY.md](METHODOLOGY.md)
2. Contribute via pull request
3. Propose new document categories or generators
4. If instrumenting A2A context, report `submission_channel` and `compound_attack_rate` (v1.1 preparation fields)

---

## Repository Structure

```
SDB-26/
├── README.md           — This file
├── STANDARD.md         — Full standard document
├── METHODOLOGY.md      — Detailed measurement methodology
├── CHANGELOG.md
├── results_schema.json — Standard benchmark results schema
├── fraudlens_v2_2026-04.json
├── docs/
│   ├── FRC_OVERVIEW.md
│   ├── FRC_SCHEMA.md
│   ├── FRC_CODEBOOK.md
│   ├── FRC_ACTION_MATRIX.md
│   ├── FRC_TECHNICAL_REFERENCE.md
│   └── FRC_A2A_EXTENSION.md
├── schemas/
│   └── frc_schema_v1_0_0.json
├── examples/
│   └── frc/
└── tests/
    └── frc/
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

## Public Draft Disclaimer

This repository is published as an implementation-agnostic measurement framework and reference specification.

It includes:
- methodology and terminology,
- schema contracts,
- reference examples and validation fixtures.

It does not include:
- client data,
- institution-specific calibration thresholds,
- production scoring weights or anti-evasion operational playbooks.

Forensic outputs are probabilistic indicators, not legal determinations.

---

*SDB-26 was developed in parallel with a technical response to the AMLA public consultation on draft CDD Regulatory Technical Standards (Article 28(1) of Regulation (EU) 2024/1624), proposing forensic image physics analysis as a mandatory verification layer.*
