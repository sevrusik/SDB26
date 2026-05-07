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
| **ABR** / **ACG** (v1.1 preview) | Agent bypass patterns; **ACG** uses envelope **`compound_confidence`** on joint approvals (not document-only scores) | Surfaces weak agent/instrumentation gating next to document BR |
| **TCR** / **HAR** (v1.1 preview) | Tool-call coverage and handoff audit rates on agent-mediated flows | Measures whether logs reconstruct *how* the package was built |

Reference methodology: `STANDARD.md` (§4.5 preview metrics), `METHODOLOGY.md`, `results_schema.json`.

---

## Attack Levels

SDB-26 evaluates three escalating attack classes:

- **L1 — Standard Generation:** direct AI-generated documents, no post-processing
- **L2 — Advanced Diffusion:** fine-tuning/editing/metadata manipulation scenarios
- **L3 — Screen Recapture:** synthetic/edited files recaptured through display pipelines

L3 is critical because recapture can remove or distort many provenance cues while preserving plausible visual content.

---

## Audit Trails

SDB-26 includes FRC (Forensic Reason Codes) and the **FRC A2A Extension** (`docs/FRC_A2A_EXTENSION.md`, **v0.5.2**) so decisions stay auditable when submissions pass through **human-direct**, **agent-assisted**, or **managed-agent** channels.

**Core links**

- `docs/FRC_OVERVIEW.md`
- `docs/FRC_A2A_EXTENSION.md`
- `docs/FRC_A2A_DEPLOYMENT_MAPPING.md`

**What v0.5.2 adds for implementers**

- **Compound routing** joins document FRC with an **`agent_verdict`** posture. The decision matrix now includes **INSUFFICIENT × PARTIALLY_ATTESTED → REVIEW** and **INSUFFICIENT × SUSPICIOUS → ESCALATE**, plus a small **decision tree** so “bad scan + bad agent path” is not treated as a pure quality retry.
- **Normative L0 → `agent_verdict` mapping** (precedence for UNATTESTED / SUSPICIOUS / PARTIALLY_ATTESTED / ATTESTED) so **`PARTIALLY_ATTESTED`** is not an informal catch-all.
- **Confidence split:** `verdict_confidence` in the core FRC payload = **document layer** only; **`compound_confidence`** on the envelope = confidence in the final **`compound_verdict`** (document + agent + policy). Published composition rules (`CC_MIN` / `CC_DOC_ONLY` / `CC_CUSTOM`) keep benchmarks comparable.
- **A2A Protocol alignment:** optional **`a2a_correlation`** and **`schemas/a2a_v1_surfaces.json`** reuse formal **Task** / **TaskState** / discovery shapes from the open [Agent2Agent (A2A) specification](https://a2a-protocol.org/latest/specification/) instead of parallel type names.
- **Threat model:** extends to **T6** (shadow connector / `FRC-L0-CONNECTOR-OUT-OF-POLICY`) and **T7** (opaque secret–workload binding / `FRC-L0-SECRET-BINDING-UNKNOWN`) alongside existing instrumentation-evasion coverage.

This bridges document-level authenticity to **agent-era traceability** (`instrumentation_trace`, L0/L0-D signals, ABR / ACG / TCR / HAR where applicable).

---

## FRC A2A schemas (machine validation)

- `schemas/frc_schema_v1_0_0.json` — document-layer FRC.
- `schemas/frc_a2a_envelope_v0_2_0.json` — audit envelope (`agent_verdict`, `compound_verdict`, **`compound_confidence`**, optional **`agent_layer_confidence`**, **`a2a_correlation`**).
- `schemas/a2a_v1_surfaces.json` — A2A type surfaces for correlation fields.
- Examples and CI: `examples/frc/`, `scripts/validate_frc_schemas.py`.

---

## Reference Implementation

Practical implementation path:

- **Forensic packet collection workflow** (`collect_forensic_packet.py`) used for corpus-building and repeatable acquisition pipelines.
- **Schema-valid decision artifacts** using FRC/FRC A2A outputs and fixtures in this repository (see **FRC A2A schemas** above).

Related artifacts in this repo:

- `examples/frc/`
- `tests/frc/`
- `CHANGELOG.md` — release notes including FRC A2A **v0.5.1** / **v0.5.2** refinements.

---

## Why now

As AI generation quality and agent-mediated onboarding velocity rise, trust controls must move from static checks to measurable, reproducible evidence chains.

SDB-26 provides that measurement contract.

