# SDB-26 × ENISA Secure by Design and Default Playbook — Implementation mapping (v0.1)

**Status:** implementation note (not a normative standard).  
**Canonical location:** this repository — `docs/SDB26_ENISA_SecureByDesign_Mapping_v0.1.md`.  
**Audience:** teams building or procuring document-centric identity verification; SMEs mapping controls to an open benchmark.  
**SDB-26:** [github.com/sevrusik/SDB26](https://github.com/sevrusik/SDB26) · [sdb26.com](https://sdb26.com)  
**ENISA reference:** *Security by Design and Default Playbook* — public consultation, March 2026 (document history: v0.4). Source: [ENISA](https://www.enisa.europa.eu/).

---

## 1. Why this mapping exists

ENISA’s playbook describes **how to design and operate secure products** (architecture, identity, layering, transparency, lifecycle).  
**SDB-26** describes **how to measure** whether a document-forensics stack resists realistic bypass (e.g. Bypass Rate, structured reason codes, reproducible evaluation).

They operate at different layers:

| Layer | ENISA playbook (illustrative) | SDB-26 (illustrative) |
|--------|-------------------------------|------------------------|
| Product security lifecycle | Threat modelling, secure defaults, logging, supply chain | Out of scope for the benchmark spec itself |
| Identity / document decision | Strong identity architecture, defence in depth, explainability | FRC output, attack levels L1–L3, measurable BR |

**This document connects them** so that compliance, security, and engineering can use one narrative: *secure-by-design identity evidence* plus *open measurement of bypass*.

---

## 2. Scope and limits

- **In scope:** Mapping ENISA *architectural* principles relevant to **document verification** to **SDB-26 artefacts** (FRC schema, classes, attack levels, evaluation habits).
- **Out of scope:** Replacing ENISA’s full playbook (e.g. patch management, SBOM detail, incident response procedures). Those remain **separate obligations** for the product organisation.
- **Not legal or regulatory advice.** Institutions remain responsible for their own jurisdictional obligations.
- **Not an ENISA-endorsed document.** This mapping is an independent implementation note by the SDB-26 project. It is **not** reviewed, approved, or sponsored by ENISA; any impression of endorsement should be avoided.

---

## 3. Principle mapping (core)

Quotes below are **condensed** from ENISA Section 3.1 (*Architectural Foundations*). For authoritative wording, use the published playbook.

### 3.1 Strong identity and authentication architecture

**ENISA (paraphrase):** A secure architecture needs a clear, consistent approach to how identities are **created, verified, and managed** (users, devices, services, admins), including authoritative sources and authentication across interfaces.

**Document verification reading:** Uploading a document and receiving “pass” is an **identity event**. “Verified” must mean: **which evidence** tied the document to a claimed identity, under **which policy**, with **which artefacts** retained.

**SDB-26 / FRC alignment:**

| Practice | Artefact |
|----------|----------|
| Verdict is not a black box | `verdict`, `sdb26_class`, `attack_level`, `required_action` |
| Signal-level explainability | `primary_codes`, `supporting_codes` with `FRC-L1|L2|L3|INF-*` |
| Evidence strength explicit | Per-code `confidence`, `evidence_strength` (see `schemas/frc_schema_v1_0_0.json`) |
| Reproducibility hook | `model_trace.detector_version`, `model_trace.pipeline_id` |
| Audit-friendly payload | Optional `decision_id`, `evaluated_at` |

**Gap if missing:** Vendor “pass/fail” only → **does not satisfy** the spirit of this principle for regulated or high-risk use.

---

### 3.2 Defence in depth

**ENISA (paraphrase):** Layered controls so **failure of one mechanism does not cause complete compromise**; **some controls may be bypassed** — design for graceful degradation, diverse controls, no single “silver bullet.”

**Document verification reading:** One model or one metadata check must not be the only line. **Independent families** of signal (e.g. synthetic / manipulation / presentation or capture) should contribute; bypass of one layer should **not** automatically mean total bypass.

**SDB-26 alignment:**

| Concept | SDB-26 expression |
|---------|-------------------|
| Layered attacks | `attack_level`: **L1** (synthetic), **L2** (editing/metadata), **L3** (capture/presentation), **INF** (insufficient evidence) |
| Class separation | `sdb26_class`: `SYNTHETIC`, `EDITED`, `SCREENSHOT`, `GENUINE`, `INSUFFICIENT` |
| No single-code over-trust | Schema constraints (e.g. certain fraud classes require appropriate codes; `GENUINE` constraints on codes) |
| Measurement | Bypass Rate (BR) / agent variants in benchmark methodology — **empirical** defence-in-depth test |

**Implementation habit:** Map each **detector family** in your pipeline to an **attack level** and ensure FRC outputs **combine** layers instead of collapsing to one scalar.

---

### 3.3 Open Design (avoiding obscurity)

**ENISA (paraphrase):** Security should not rely on **hidden behaviour**; **transparent designs** are easier to **audit, validate, and improve**. Open design does **not** mean publishing secrets — it means security rests on keys, authentication, and sound implementation, not secrecy of the mechanism.

**Document verification reading:** Institutions should be able to **inspect methodology**, **re-run evaluation**, and **compare vendors** on agreed fixtures — not trust marketing accuracy.

**SDB-26 alignment:**

| Concept | SDB-26 expression |
|---------|-------------------|
| Open schema | Published FRC JSON Schema in this repo: `schemas/frc_schema_v1_0_0.json` |
| Open benchmark | Public corpus methodology and BR definitions (`METHODOLOGY.md`, `STANDARD.md`) |
| Operational transparency | `model_trace` + versioned pipelines |
| Independent audit | Third parties can validate outputs against schema + benchmark |

---

## 4. Extended mapping (selected ENISA playbook topics)

Short cross-reference for product teams extending beyond the “big three” principles.

| ENISA playbook theme (section titles) | Document verification angle | SDB-26 / implementation note |
|----------------------------------------|------------------------------|------------------------------|
| Trust boundaries & threat modelling | Where does “untrusted document” enter? | Map upload channel to threat cases in eval sets |
| Least privilege | Who can see raw biometrics / documents? | Product control; not specified in FRC |
| Attack surface minimisation | Fewer exposed APIs = smaller risk | Product architecture |
| Logging, monitoring, alerting | Security-relevant logs, tamper-evident | Correlate logs with `decision_id` / FRC payload |
| Supply chain controls | Third-party models and dependencies | Align vendor contracts with `detector_version` provenance |

---

## 5. SME minimal package (practical)

For organisations that cannot implement the full playbook immediately, a **proportionate** bundle that still aligns with both ENISA’s direction and SDB-26:

1. **Identity evidence policy** — Define what “verified” means (which signals must be present for auto-approve vs manual review).
2. **Layered pipeline** — At least **two independent families** (e.g. pixel-level + capture/presentation heuristics, or document integrity + synthetic detection).
3. **Structured output** — Emit FRC-compatible payloads (`primary_codes` / `supporting_codes`, `model_trace`) for every decision.
4. **Version pinning** — Store `detector_version` and `pipeline_id` for every decision.
5. **Pilot measurement** — Run a **small fixed eval set** and track BR or proxy metrics before scaling.

This is **not** full ENISA compliance; it is a **staging point** toward secure-by-design identity operations.

---

## 6. Reference implementations (informative)

SDB-26 does **not** mandate a specific product. Any stack that emits **schema-valid FRC** and participates in **open evaluation** can use this mapping. Implementations may mirror `schemas/` and `tests/frc/` for CI; the **normative** schema and fixtures live in **this** repository.

---

## 7. Versioning

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-05-02 | Initial mapping: identity architecture, defence in depth, open design; SME package |

**Planned v0.2 (engineering-focused):** Add a **one-page worked example** so a team can implement and validate end-to-end without reading the full playbook:

- **Inputs:** One concrete fixture (e.g. a labelled sample image or a reference like `tests/frc/valid_01_fraud_l3.json` as the *target* output shape).
- **Pipeline trace:** Short table: detector / layer → raw signal → mapped `attack_level` / candidate FRC codes.
- **Output:** Full **schema-valid** FRC JSON (copy-paste ready), with `model_trace` filled as you would in production.
- **Verification:** Command or pointer to validate against `schemas/frc_schema_v1_0_0.json` (e.g. CI pattern in this repository).
- **Optional:** HTTP trace (request/response redacted) if the example is API-driven.

**Optional:** Cross-link to a public ENISA consultation response if the SDB-26 project files one.

---

## 8. References

- ENISA — *Security by Design and Default Playbook* (consultation, March 2026): [enisa.europa.eu](https://www.enisa.europa.eu/)
- SDB-26 — this repository: [github.com/sevrusik/SDB26](https://github.com/sevrusik/SDB26) · [sdb26.com](https://sdb26.com)
- FRC JSON Schema (canonical): `schemas/frc_schema_v1_0_0.json`
