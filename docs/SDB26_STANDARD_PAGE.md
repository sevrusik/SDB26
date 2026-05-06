# SDB-26 Standard Page

## Hero Section

**SDB-26 is a benchmark for document authenticity, not marketing accuracy.**

SDB-26 defines how to measure whether document verification systems can withstand synthetic, edited, and screen-recaptured artifacts in real operational conditions.

---

## Measurement Grid

SDB-26 is built around measurable, reproducible outcomes:

| Metric | Meaning | Why it matters |
|--------|---------|----------------|
| **BR** (Bypass Rate) | Share of fraudulent/synthetic documents incorrectly approved | Core indicator of control failure |
| **CG** (Confidence Gap) | Mean confidence on wrongly approved cases | Detects overconfident errors |
| **GS** (Generator Sensitivity) | BR segmented by generator/model family | Shows where systems break first |
| **FPR** (False Positive Rate) | Share of genuine cases flagged as suspicious/fraud | Tracks business and customer impact |

Reference methodology: `STANDARD.md`, `METHODOLOGY.md`, `results_schema.json`.

---

## Attack Levels

SDB-26 evaluates three escalating attack classes:

- **L1 — Standard Generation:** direct AI-generated documents, no post-processing
- **L2 — Advanced Diffusion:** fine-tuning/editing/metadata manipulation scenarios
- **L3 — Screen Recapture:** synthetic/edited files recaptured through display pipelines

L3 is critical because recapture can remove or distort many provenance cues while preserving plausible visual content.

---

## Audit Trails

SDB-26 includes FRC (Forensic Reason Codes) and A2A extension artifacts to keep decisions auditable in agent-mediated flows:

- `docs/FRC_OVERVIEW.md`
- `docs/FRC_A2A_EXTENSION.md`
- `docs/FRC_A2A_DEPLOYMENT_MAPPING.md`

This provides a bridge from document-level authenticity to agent-era traceability (`instrumentation_trace`, L0/L0-D signals, ABR/TCR/HAR style controls).

---

## Reference Implementation

Practical implementation path:

- **Forensic packet collection workflow** (`collect_forensic_packet.py`) used for corpus-building and repeatable acquisition pipelines.
- **Schema-valid decision artifacts** using FRC/FRC A2A outputs and fixtures in this repository.

Related artifacts in this repo:

- `examples/frc/`
- `tests/frc/`
- `schemas/frc_schema_v1_0_0.json`
- `schemas/frc_a2a_envelope_v0_2_0.json`

---

## Why now

As AI generation quality and agent-mediated onboarding velocity rise, trust controls must move from static checks to measurable, reproducible evidence chains.

SDB-26 provides that measurement contract.

