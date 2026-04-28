# SDB-26 Changelog

All notable changes to the SDB-26 benchmark will be documented here.

Format follows [Semantic Versioning](https://semver.org/):
- **Major versions (x.0):** Changes to metric definitions or measurement methodology
- **Minor versions (1.x):** Addition of new generators or document types
- **Patch versions (1.0.x):** Clarifications, corrections, editorial changes

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
