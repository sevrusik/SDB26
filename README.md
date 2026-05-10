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

Conference/landing-style overview page:
- [docs/SDB26_STANDARD_PAGE.md](docs/SDB26_STANDARD_PAGE.md)
- [docs/SDB26_STANDARD_PAGE.html](docs/SDB26_STANDARD_PAGE.html)
- [docs/AUTHOR.md](docs/AUTHOR.md)
- [docs/AUTHOR.html](docs/AUTHOR.html)

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

## FRC Package (v1.0)

SDB-26 now includes a Forensic Reason Codes (FRC) package for explainable, audit-ready decision outputs.

- Overview: [docs/FRC_OVERVIEW.md](docs/FRC_OVERVIEW.md)
- Human-readable schema: [docs/FRC_SCHEMA.md](docs/FRC_SCHEMA.md)
- Code dictionary: [docs/FRC_CODEBOOK.md](docs/FRC_CODEBOOK.md)
- Action policy mapping: [docs/FRC_ACTION_MATRIX.md](docs/FRC_ACTION_MATRIX.md)
- JSON Schema: [schemas/frc_schema_v1_0_0.json](schemas/frc_schema_v1_0_0.json)
- Valid examples: [examples/frc](examples/frc) — see [examples/frc/README.md](examples/frc/README.md) (Mode A / Mode B walkthrough); includes `a2a_audit_mode_a_human_upload.json`, `a2a_audit_mode_b_escalate_missing_trace.json`, `a2a_audit_mode_b_partial_attestation_review.json`, `a2a_audit_insufficient_unattested_escalate.json`, `a2a_audit_repeated_l0_pattern_block.json`, and `a2a_envelope_example.json`
- CI fixtures (valid/invalid): [tests/frc](tests/frc) — validated by [scripts/validate_frc_schemas.py](scripts/validate_frc_schemas.py) (see [requirements-dev.txt](requirements-dev.txt))

Advanced extension draft for agent-to-agent contexts:
- [docs/FRC_A2A_EXTENSION.md](docs/FRC_A2A_EXTENSION.md) (v0.5.2 — L0-D instrumentation, TCR/HAR, compound matrix incl. `INSUFFICIENT`×`PARTIALLY_ATTESTED`/`SUSPICIOUS`, threat actors T6–T7, normative `agent_verdict` mapping, compound confidence, investigator appendix)
- JSON Schema (audit envelope): [schemas/frc_a2a_envelope_v0_2_0.json](schemas/frc_a2a_envelope_v0_2_0.json)
- Deployment relationship note: v0.5 now includes a dedicated section mapping FRC A2A controls to deployed agent architectures (including Anthropic `kyc-screener` as public reference context).
- Deployment mapping companion: [docs/FRC_A2A_DEPLOYMENT_MAPPING.md](docs/FRC_A2A_DEPLOYMENT_MAPPING.md) (`FRC signal -> observability fields -> policy outcomes`)
- Policy profile template: [examples/a2a_policy_profile_example.json](examples/a2a_policy_profile_example.json) (copy/adapt for ABR/TCR/HAR reporting profiles)
- Policy profile presets: [examples/a2a_policy_profile_strict.json](examples/a2a_policy_profile_strict.json) and [examples/a2a_policy_profile_balanced.json](examples/a2a_policy_profile_balanced.json)
- Experimental continuity track (non-normative): [docs/FRC_A2A_EXPERIMENTAL_v0_6.md](docs/FRC_A2A_EXPERIMENTAL_v0_6.md), with sample fixtures under `examples/frc/experimental/`

Implementation note — how SDB-26 maps onto ENISA *Secure by Design and Default* (consultation playbook):
- [docs/SDB26_ENISA_SecureByDesign_Mapping_v0.1.md](docs/SDB26_ENISA_SecureByDesign_Mapping_v0.1.md)

Responsible release and dual-use policy:
- [docs/RESPONSIBLE_RELEASE_POLICY.md](docs/RESPONSIBLE_RELEASE_POLICY.md)

---

## Three Levels of Synthetic Complexity

| Level | Name | Description |
|-------|------|-------------|
| L1 | Standard Generation | DALL-E 3, Midjourney, SD XL, ChatGPT Image 2, Seedream 5 Lite, Kling O1 Image, Flux 2 — no post-processing |
| L2 | Advanced Diffusion | Split into **L2G** (generation/editing complexity) and **L2E** (post-processing evasion strata) |
| L3 | Screenshot Attack | Any L1/L2 document captured via screenshot — bypasses C2PA |

L2 includes normative split:
- **L2G:** generation/editing-focused advanced diffusion cases
- **L2E:** adversarial post-processing attempts with subclasses:
`L2E1_CHROMA_REENCODE`, `L2E2_AUTHENTIC_BLEND`, `L2E3_FFT_ENVELOPE_TRANSPLANT`, `L2E4_CFA_REMOSAIC`, `L2E5_RELAUNDER_IMG2IMG`.
See `STANDARD.md` Section 3.1 and BR reporting requirements in Section 4.1 (`BR_L2E_total`, `BR_L2E_by_subclass`, `BR_L2E_worst_subclass`).

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
│   ├── FRC_A2A_EXTENSION.md
│   ├── SDB26_ENISA_SecureByDesign_Mapping_v0.1.md  — ENISA SbD playbook mapping (v0.1)
│   └── RESPONSIBLE_RELEASE_POLICY.md               — dual-use release policy
├── schemas/
│   ├── frc_schema_v1_0_0.json
│   ├── frc_a2a_envelope_v0_2_0.json
│   └── l2e_fixture_schema_v0_1_0.json
├── scripts/
│   └── validate_frc_schemas.py   — CI: validates tests/frc + examples/frc
├── requirements-dev.txt          — jsonschema (for the validator script)
├── examples/
│   ├── frc/
│   └── l2e/                       — redacted L2E fixture examples
└── tests/
    └── frc/
```

**Reference implementation:** [FraudLens](https://github.com/sevrusik/fraudlens) (API + detectors) mirrors the ENISA mapping under `docs/` for convenience; **normative** FRC schema and fixtures remain in this repository.

---

## Citation

If you use SDB-26 in research or product evaluation, please cite:

```
Mishyn, R. (2026). SDB-26: The 2026 Synthetic Document Benchmark.
Retrieved from https://github.com/sevrusik/SDB26
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
- unrestricted operational L2E transformation parameter sets.

Forensic outputs are probabilistic indicators, not legal determinations.

---

*SDB-26 was developed in parallel with a technical response to the AMLA public consultation on draft CDD Regulatory Technical Standards (Article 28(1) of Regulation (EU) 2024/1624), proposing forensic image physics analysis as a mandatory verification layer.*
