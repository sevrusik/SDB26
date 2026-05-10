# SDB-26 Changelog

All notable changes to the SDB-26 benchmark will be documented here.

Format follows [Semantic Versioning](https://semver.org/):
- **Major versions (x.0):** Changes to metric definitions or measurement methodology
- **Minor versions (1.x):** Addition of new generators or document types
- **Patch versions (1.0.x):** Clarifications, corrections, editorial changes

---

## [1.0.12] — May 2026

**Responsible release controls + redacted L2E fixture templates.**

### Added
- `docs/RESPONSIBLE_RELEASE_POLICY.md` — Public/Restricted/Private release model and dual-use hygiene rules.
- `schemas/l2e_fixture_schema_v0_1_0.json` — schema template for L2E fixture metadata, including `attack_subclass` and `parent_id`.
- `examples/l2e/README.md` + two redacted examples:
  - `examples/l2e/l2e_fixture_example_chroma_redacted.json`
  - `examples/l2e/l2e_fixture_example_relaunder_redacted.json`

### Changed
- `README.md` updated with policy link, L2E schema listing, and redacted example fixture directory.
- `STANDARD.md` legal section now references the responsible release policy and defender-oriented publication boundary.

---

## [1.0.11] — May 2026

**L2 Level split (L2G/L2E) + taxonomy for post-processing evasion attempts.**

### Added
- `STANDARD.md` Section 3.1: explicit **L2 split** into `L2G` (generation/editing) and `L2E` (evasion/post-processing), both normative within Level 2.
- `STANDARD.md` Section 3.1: **Level 2E (L2E)** subclasses for advanced post-processing/evasion attempts:
  - `L2E1_CHROMA_REENCODE`
  - `L2E2_AUTHENTIC_BLEND`
  - `L2E3_FFT_ENVELOPE_TRANSPLANT`
  - `L2E4_CFA_REMOSAIC`
  - `L2E5_RELAUNDER_IMG2IMG`
- Normative L2E corpus rules: subclass labels, pre/post lineage recommendation, parameter capture, and minimum sample guidance.
- `docs/FRC_CODEBOOK.md`: L2E-oriented FRC additions:
  - `FRC-L2-DCT-DOUBLE-COMP-ANOMALY`
  - `FRC-L2-ELA-LOCAL-DIVERGENCE`
  - `FRC-L2-PHASE-INCOHERENCE`
  - `FRC-L2-INTERCHANNEL-NOISE-MISMATCH`
  - `FRC-L2-SEMANTIC-TEXTURE-INCONSISTENCY`

### Changed
- `STANDARD.md` §4.1 BR reporting requirements expanded with Level 2E slices:
  - `BR_L2E_total`
  - `BR_L2E_by_subclass`
  - `BR_L2E_worst_subclass`
- `README.md` Level 2 description now explicitly includes the L2G/L2E split and links to corresponding BR reporting fields.

---

## [1.0.10] — May 2026

**FRC A2A Extension v0.5.2 — INSUFFICIENT compound rows, decision tree, threat T6/T7.**

### Added
- Compound verdict matrix rows: **`INSUFFICIENT + PARTIALLY_ATTESTED → REVIEW`**, **`INSUFFICIENT + SUSPICIOUS → ESCALATE`**; ASCII **decision tree** for insufficient-document × `agent_verdict`.
- Threat actors **T6** (shadow connector / `FRC-L0-CONNECTOR-OUT-OF-POLICY`) and **T7** (secret binding / `FRC-L0-SECRET-BINDING-UNKNOWN`).

### Changed
- `docs/FRC_A2A_EXTENSION.md` → **v0.5.2**; **INSUFFICIENT Handling in A2A** expanded for `PARTIALLY_ATTESTED` and `SUSPICIOUS`.
- `README.md` and `schemas/frc_a2a_envelope_v0_2_0.json` description pointer.

---

## [1.0.9] — May 2026

**FRC A2A Extension v0.5.1 — `agent_verdict` runtime mapping and compound confidence semantics.**

### Added
- Normative **L0→`agent_verdict` precedence table** (default trigger sets for `UNATTESTED` / `SUSPICIOUS` / `PARTIALLY_ATTESTED` / `ATTESTED`) and **confidence** section: `verdict_confidence` (document-only) vs `compound_confidence` (joint), reference composition IDs `CC_MIN` / `CC_DOC_ONLY` / `CC_CUSTOM`, optional **`agent_layer_confidence`** on the envelope.

### Changed
- `docs/FRC_A2A_EXTENSION.md` → **v0.5.1**; **ACG** now defined on **`compound_confidence`** (not `verdict_confidence`).
- `STANDARD.md` §4.5 **ACG** formula updated to match.
- `schemas/frc_schema_v1_0_0.json` — `description` on **`verdict_confidence`**.
- `schemas/frc_a2a_envelope_v0_2_0.json` — descriptions on **`compound_confidence`**, optional **`agent_layer_confidence`**.
- `examples/frc/a2a_envelope_example.json` — illustrative **`agent_layer_confidence`**.
- `README.md` — FRC A2A doc pointer **v0.5.1**.

---

## [1.0.8] — May 2026

**FRC A2A experimental continuity track (non-normative).**

### Added
- `docs/FRC_A2A_EXPERIMENTAL_v0_6.md` — exploratory annex for candidate multi-agent failure-mode controls and metrics.
- `examples/frc/experimental/a2a_exp_goal_misalignment_review.json` — experimental fixture for goal-misalignment review path.
- `examples/frc/experimental/a2a_exp_feedback_loop_escalate.json` — experimental fixture for loop-detection escalation path.

### Changed
- `docs/FRC_A2A_EXTENSION.md` now links to the experimental continuity track while preserving the normative v0.5 contract.
- `README.md` now references the experimental track and fixture location.

### Notes
- No changes to normative schema contracts in `schemas/`.
- Experimental fixtures are intentionally outside normative schema CI in v1.0.x.

---

## [1.0.7] — May 2026

**FRC A2A v0.5 policy-path fixtures + optional `agent_verdict` guidance.**

### Added
- `examples/frc/a2a_audit_insufficient_unattested_escalate.json` — `INSUFFICIENT + UNATTESTED => ESCALATE` reference path.
- `examples/frc/a2a_audit_repeated_l0_pattern_block.json` — repeated high-risk L0 pattern with policy `BLOCK` override.

### Changed
- `schemas/frc_a2a_envelope_v0_2_0.json` — added optional `agent_verdict` enum (`ATTESTED | PARTIALLY_ATTESTED | UNATTESTED | SUSPICIOUS`).
- `docs/FRC_A2A_EXTENSION.md` promoted to v0.5: optional `agent_verdict` consistency guidance + `Relationship to deployed agent architectures` section with Anthropic `kyc-screener` reference and L0/TCR/HAR mapping notes.
- `README.md` and `examples/frc/README.md` updated with new policy-path examples.
- Added companion note `docs/FRC_A2A_DEPLOYMENT_MAPPING.md` with `FRC signal -> observability fields -> policy outcomes` mapping table and implementation checklist.
- Added copy-ready policy profile template `examples/a2a_policy_profile_example.json` and linked it from README/deployment mapping note.
- Added policy profile presets `examples/a2a_policy_profile_strict.json` and `examples/a2a_policy_profile_balanced.json` for strict vs balanced operating models.

---

## [1.0.6] — May 2026

**FRC A2A v0.4 calibration guidance + additional Mode B fixtures.**

### Added
- `examples/frc/a2a_audit_mode_b_escalate_missing_trace.json` — policy path: `GENUINE` document + `FRC-L0-DATA-PATH-UNATTRIBUTED` => `compound_verdict=ESCALATE`.
- `examples/frc/a2a_audit_mode_b_partial_attestation_review.json` — policy path: partial attestation disclosure gap => `compound_verdict=REVIEW`.
- `docs/FRC_A2A_EXTENSION.md` calibration section (velocity baseline, MaterialToolSet taxonomy, phased TCR/HAR rollout).

### Changed
- `scripts/validate_frc_schemas.py` now validates all `examples/frc/a2a_*.json` fixtures (pattern-based discovery).
- `docs/FRC_A2A_EXTENSION.md` upgraded to v0.4 and version history updated.
- `examples/frc/README.md` extended with Mode B review/escalate variants.

---

## [1.0.5] — May 2026

**FRC A2A investigator walkthrough and Mode A envelope example.**

### Added
- `examples/frc/README.md` — Mode A vs Mode B checklist for investigators; `agent_submitted` note; comparison table.
- `examples/frc/a2a_audit_mode_a_human_upload.json` — valid envelope (`human_direct`, no `instrumentation_trace`).

### Changed
- `docs/FRC_A2A_EXTENSION.md` — v **0.3**: appendix linking to examples; versioning table; roadmap 0.4.
- `scripts/validate_frc_schemas.py` — validates both A2A envelope fixtures under `examples/frc/`.

---

## [1.0.4] — May 2026

**FRC schema CI and STANDARD v1.1 preview metrics (TCR/HAR).**

### Added
- `scripts/validate_frc_schemas.py` — validates `tests/frc/*`, core `examples/frc/*.json`, and `a2a_envelope_example.json` against canonical schemas.
- `requirements-dev.txt` — `jsonschema` for local/CI validation.
- `.github/workflows/frc-validate.yml` — runs the validator on schema/fixture changes.

### Changed
- `STANDARD.md` §4.5 — documented **TCR** and **HAR** (non-normative v1.1 preview, aligned with FRC A2A v0.2).
- `README.md` — repository tree includes `schemas/frc_a2a_envelope_v0_2_0.json`, `scripts/`, `requirements-dev.txt`.

---

## [1.0.3] — May 2026

**FRC A2A Extension v0.2 (documentation + envelope schema).**

### Added
- `schemas/frc_a2a_envelope_v0_2_0.json` — machine-validatable audit envelope (`instrumentation_trace`, submission modes, L0-D readiness).
- `examples/frc/a2a_envelope_example.json` — sample Mode B audit record with nested valid FRC payload.
- `docs/FRC_A2A_EXTENSION.md` v0.2: L0-D codes (data path, connectors, handoffs, tool permissions, HITL), submission modes A/B, TCR and HAR metrics, threat actor T5, expanded audit trail example, new open questions.
- `docs/FRC_CODEBOOK.md` — pointer to L0 codes in the A2A extension.

---

## [1.0.2] — May 2026

**Generator naming normalization and coverage extension update.**

### Added
- Added current generator coverage in `STANDARD.md` and `README.md` Level 1 references:
  - ChatGPT Image 2
  - Seedream 5 Lite
  - Kling O1 Image
  - Flux 2
- Added `Nano Banana 2` and `Flux 2` entries in Tier 2 generator classification and complexity matrix.
- Added pending generator sensitivity keys in `fraudlens_v2_2026-04.json`:
  - `chatgpt_image_2`
  - `seedream_5_lite`
  - `kling_o1_image`
  - `flux_2`
  - `nano_banana_2`

### Changed
- Normalized naming style to `Midjourney` across technical references and baseline result notes.
- Harmonized ChatGPT image tool naming in generator matrix (`ChatGPT 4o Image`, `ChatGPT Image 2`).

---

## [1.0.1] — April 2026

**Documentation and schema extension update (FRC package).**

### Added
- `docs/FRC_OVERVIEW.md` — entry-point overview for explainable forensic outputs
- `docs/FRC_SCHEMA.md` — human-readable FRC contract
- `docs/FRC_CODEBOOK.md` — FRC code dictionary (L1/L2/L3/INF)
- `docs/FRC_ACTION_MATRIX.md` — policy mapping from evidence to action
- `docs/FRC_TECHNICAL_REFERENCE.md` — extended technical reference draft
- `docs/FRC_A2A_EXTENSION.md` — draft extension for A2A submission contexts
- `schemas/frc_schema_v1_0_0.json` — machine-validatable FRC JSON schema
- `examples/frc/` — valid reference payloads
- `tests/frc/` — valid/invalid fixtures for CI validation

### Changed
- Updated repository links from `SCHEMA/results_schema.json` to `results_schema.json` in core docs.
- Updated `README.md` repository structure and quick links to include FRC package.
- Updated `docs/FRC_A2A_EXTENSION.md` to `v0.1.1 clarifications` (policy-conditional `FRC-L0-MODEL-UNDISCLOSED`, privacy note for `FRC-L0-SESSION-ANOMALY`, default `GENUINE + SUSPICIOUS -> ESCALATE`, formal `ABR_strict/ABR_operational`).

---

## [1.0] — April 2026

**Initial public release.**

### Benchmark
- Defined three-level corpus structure (Standard Generation, Advanced Diffusion, Screenshot Attack)
- Defined three primary metrics: Bypass Rate, Confidence Gap, Generator Sensitivity
- Defined False Positive Rate as required companion metric
- Published standard JSON reporting schema

### Corpus
- Level 1: DALL-E 3, Midjourney v6, Stable Diffusion XL
- Level 2: Specialised ID generation pipelines (MEX, JPN passport datasets)
- Level 3: Screenshot Attack corpus (in preparation, Q2 2026)

### Results
- FraudLens v2.0 baseline results published (first public SDB-26 evaluation)
- Claude 3 Haiku vision AI reference comparison published

### Documentation
- STANDARD.md: Full formal specification
- METHODOLOGY.md: Detailed evaluation guidance
- results_schema.json: JSON schema for results reporting
- README.md: Quick start guide

---

## Planned

### [1.1] — Q3 2026 (planned)
- Add Level 3 corpus (Screenshot Attack — iOS and Android)
- Add genuine document control set
- Publish FPR baseline for FraudLens v2.0
- Add Stable Diffusion XL generator sensitivity results
- Formalise ABR / ACG / CDR metric definitions in `STANDARD.md` (promoted from FRC A2A Extension draft)
- Add `L0_any` vs `L0_high_risk` signal tiering for agent-risk reporting
- Add two new sections in `METHODOLOGY.md`: submission channel constraints and compound attack taxonomy
- Add `submission_channel` to results JSON schema for channel-stratified reporting
- Add `compound_attack_rate` to results schema with BR/ABR linkage

### [1.2] — Q4 2026 (planned)
- Extend corpus to include bank statements and invoices
- Add Flux generator
- Add video deepfake document category (preliminary)

### [2.0] — 2027 (planned)
- Review metric definitions based on community feedback
- Independent governance model
- Formal certification process for "SDB-26 Compliant" designation
