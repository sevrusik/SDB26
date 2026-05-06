# FRC A2A Extension — Agent Identity Forensics
## SDB-26 Extension: Forensic Reason Codes for Agentic Submission Contexts

**Version:** 0.5 (Draft for public comment)  
**Status:** Proposed extension to FRC v1.0  
**Repository:** github.com/sevrusik/SDB-26  
**Scope:** Measurement framework — implementation-agnostic

---

## Motivation

FRC v1.0 addresses document-level authenticity: was the submitted file generated, manipulated, or screen-captured? It answers the question: *is this document real?*

In agentic contexts, a prior question must be answered first: *who is submitting this document, and under what authority?*

As financial systems adopt A2A (agent-to-agent) commerce — where AI agents autonomously open accounts, initiate payments, and complete onboarding on behalf of principals — the attack surface shifts upstream. Agentic fraud pipelines can:

- Generate synthetic KYC documents on-demand at submission time
- Submit at velocity that exceeds human-adapted detection cadences
- Chain delegated authority across multiple agents, each adding an attestation layer that may be unverifiable
- Exploit the absence of a human review step to automate bypass at scale

FRC v1.0 detects the document artifact. FRC A2A Extension detects the submission context.

**These are complementary, not alternative, layers. Both must be evaluated.**

---

## Scope Boundaries

This extension defines **what should be measured** in A2A forensic contexts. It does not specify:

- Which cryptographic implementation to use for agent attestation
- Which identity standard (W3C VC, C2PA, MCP, SPIFFE, or other) to adopt
- How agents should be registered or provisioned

Implementation choices are left to the deploying institution. This framework defines the measurement dimensions and failure modes that any implementation must address.

### Core FRC Compatibility

This extension does **not** replace the base FRC contract in `schemas/frc_schema_v1_0_0.json`.
For every evaluated submission, systems should preserve a valid core FRC payload:

- `verdict`: `GENUINE | FRAUD | INSUFFICIENT`
- `sdb26_class`: `GENUINE | SYNTHETIC | SCREENSHOT | EDITED | INSUFFICIENT`
- `attack_level`: `L1 | L2 | L3 | INF`
- `primary_codes` / `supporting_codes`
- `required_action`, `verdict_confidence`, `model_trace`

The A2A layer adds agent-context fields (`agent_verdict`, `compound_verdict`, L0 codes) on top of this base payload.

**Out of scope:**
- Human identity verification (covered by FRC v1.0)
- Device attestation for human-operated flows
- Sanctions/PEP screening of the principal
- AML transaction monitoring

---

## Core Concept: The Submission Trust Chain

In A2A onboarding, a document submission involves a chain of entities:

```
Principal (human or institution)
    ↓ authorises
Orchestrating Agent
    ↓ delegates to
Submitting Agent
    ↓ submits document to
Financial System (verifier)
```

Each link in this chain is a potential attack surface. FRC A2A Extension defines forensic signals for each link.

**Trust chain integrity requires:**
1. The submitting agent can be identified and its authority verified
2. The delegation chain from principal to submitting agent is unbroken and auditable
3. The document submitted is consistent with the claimed submission context
4. The submission behaviour is consistent with legitimate agent operation
5. Where external data or tools were used, the **instrumentation trace** attributes each material call to an allowed connector/tool scope (see L0-D)

### Submission modes (verifier perspective)

Implementations SHOULD classify each evaluated submission into one of:

| Mode | Description | L0-D expectation |
|------|-------------|------------------|
| **A — Human-direct** | End user or analyst uploads evidence; no managed agent owns the session | Instrumentation optional; identity/delegation L0-A/B still apply if the channel asserts an agent |
| **B — Agent-mediated** | A managed or orchestrated agent assembles the package (e.g. screening workflow, MCP-backed research, multi-step onboarding) | Instrumentation **required** for material external/tool calls: without an attributable trace, treat as `FRC-L0-DATA-PATH-UNATTRIBUTED` per policy |

Document-level FRC (`frc_payload`) always applies to **files and pixels**. L0-D applies to **how the package was produced** — complementary layers.

---

## Level L0 — Agent Provenance

L0 codes address the submitting entity and its authority chain. These signals are evaluated **before** document-level analysis (L1/L2/L3).

### L0-A: Agent Identity Signals

| Code | Signal | Measurable indicator | Failure mode |
|------|--------|---------------------|--------------|
| `FRC-L0-AGENT-UNATTESTED` | No verifiable identity claim from the submitting agent | Agent submission contains no cryptographic identity assertion OR assertion cannot be verified against a trusted root | Anyone can submit as any agent; no accountability chain |
| `FRC-L0-AGENT-EXPIRED` | Agent identity claim is valid in format but expired or revoked | Timestamp on identity assertion outside valid window; revocation status check fails | Compromised or decommissioned agents remain able to submit |
| `FRC-L0-MODEL-UNDISCLOSED` | No model version or capability disclosure in agent assertion | Agent does not declare which model/version is operating; fingerprinting inconsistent with declared system | Cannot assess whether agent capability matches claimed function |

Policy note for `FRC-L0-MODEL-UNDISCLOSED`: this code is **policy-conditional**.  
Apply when institution policy, contract terms, or supervisory requirements mandate model/capability disclosure for agent-operated submissions.

### L0-B: Delegation Chain Signals

| Code | Signal | Measurable indicator | Failure mode |
|------|--------|---------------------|--------------|
| `FRC-L0-CHAIN-BREAK` | Gap in delegation chain from principal to submitting agent | Submitting agent claims authority from Agent A, but Agent A's delegation assertion is absent or unverifiable | Any agent can claim authority without proof |
| `FRC-L0-AUTHORITY-MISMATCH` | Claimed authority scope does not match action taken | Agent asserts authorisation for action type X; action taken is type Y (e.g. asserts read-only, performs write) | Privilege escalation via scope mismatch |
| `FRC-L0-PRINCIPAL-ABSENT` | No verifiable human or institutional principal in delegation chain | Delegation chain terminates in an agent, not a verified principal | Fully autonomous fraud chains with no accountable human |

### L0-C: Temporal and Behavioural Signals

| Code | Signal | Measurable indicator | Failure mode |
|------|--------|---------------------|--------------|
| `FRC-L0-TEMPORAL-ANOMALY` | Document creation timestamp within seconds of submission | File creation time delta from submission time < threshold (suggested: < 30 seconds); or timestamp inconsistent with claimed capture device | On-demand synthetic generation per submission |
| `FRC-L0-VELOCITY-FLAG` | Submission rate inconsistent with legitimate agent operation | Single agent submits > N unique documents in window T; or agent submits from multiple geographic contexts simultaneously | Agentic fraud pipeline operating at scale |
| `FRC-L0-SESSION-ANOMALY` | Session characteristics inconsistent with declared agent type | Headless browser fingerprint; non-human timing patterns; missing expected agent headers | Bot submission masquerading as legitimate agent |

Privacy note for `FRC-L0-SESSION-ANOMALY`: evaluate session signals under data minimisation and jurisdictional constraints (for example GDPR/ePrivacy and local supervisory guidance).  
Only collect and retain fields required for fraud-risk assessment and auditability.

### L0-D: Instrumentation, data path, and human checkpoints

Reference architectures for financial agents (skills + governed connectors + subagent handoffs) imply a measurable layer beyond identity: **what tools ran, with what permissions, and whether human review was recorded before high-risk action.** L0-D codes address gaps in that layer.

| Code | Signal | Measurable indicator | Failure mode |
|------|--------|---------------------|--------------|
| `FRC-L0-DATA-PATH-UNATTRIBUTED` | Decision or dossier cannot be tied to verified data/tool provenance | Material factual claims or file assembly steps lack a logged connector/tool attribution, or logs cannot be correlated with `submission_id` | “Trust me” agent output with no auditable path from evidence to conclusion |
| `FRC-L0-CONNECTOR-OUT-OF-POLICY` | Data source not in institutional allowlist | Tool invocation references an MCP server / API / datastore ID outside published `OperationalConnectorSet` | Shadow data feeds; ungoverned enrichment |
| `FRC-L0-HANDOFF-UNAUDITED` | Orchestrator delegated to a worker/subagent without audit correlation | Multi-agent flow present (e.g. handoff events) but no paired record: from-id, to-id, time, declared scope | Forged or opaque delegation inside the agent graph |
| `FRC-L0-TOOL-PERMISSION-VIOLATION` | Tool call outside declared permission set | Invoked `tool_id` not in agent’s bound allowlist for this session, or args imply a capability beyond granted scope | Privilege escalation via tools |
| `FRC-L0-SECRET-BINDING-UNKNOWN` | Cannot verify workload credential binding | Secret or token used for external access cannot be mapped to attested workload/agent identity (vault binding opaque) | Stolen keys used from unattested process |
| `FRC-L0-HITL-ASSERTION-MISSING` | High-risk path without recorded human checkpoint | Policy defines mandatory human approval before submit/escalate; no `hitl_checkpoint_id` (or equivalent) in audit trail | Fully automated approval where regulation or policy requires sign-off |

Policy notes:

- **`FRC-L0-HITL-ASSERTION-MISSING`** is **policy-conditional**: apply only where the institution’s control framework or jurisdiction requires a recorded human decision for the action class.
- **PII and tool arguments:** instrumentation SHOULD store hashes/digests of arguments (`args_digest`) rather than raw payloads where possible; see Open Questions.

**Reproducibility (recommended audit fields, not codes):** `agent_template_id`, `skills_manifest_hash`, and `connector_manifest_hash` (or equivalent) SHOULD be recorded when submissions are produced from versioned agent templates — analogous to forensic packet `generation_context` for synthetic media.

---

## Compound Verdict: Document + Agent

FRC A2A Extension introduces a two-dimensional verdict:

```
{
  "frc_payload": {
    "verdict": "GENUINE | FRAUD | INSUFFICIENT",
    "sdb26_class": "GENUINE | SYNTHETIC | SCREENSHOT | EDITED | INSUFFICIENT",
    "attack_level": "L1 | L2 | L3 | INF"
  },
  "agent_verdict": "ATTESTED | PARTIALLY_ATTESTED | UNATTESTED | SUSPICIOUS",
  "compound_verdict": "TRUSTED | REVIEW | ESCALATE | BLOCK",
  "l0_codes": ["FRC-L0-TEMPORAL-ANOMALY", "FRC-L0-CHAIN-BREAK"],
  "document_codes": ["FRC-L1-FFT-GRID"],
  "compound_note": "Human-readable summary for audit trail"
}
```

### Compound Verdict Decision Matrix

| Document class (`sdb26_class`) | Agent verdict | Compound verdict | Rationale |
|-----------------|---------------|-----------------|-----------|
| GENUINE | ATTESTED | TRUSTED | Document and agent both verified |
| GENUINE | PARTIALLY_ATTESTED | REVIEW | Document passes; agent chain incomplete |
| GENUINE | UNATTESTED | ESCALATE | Document passes; agent identity not verifiable |
| GENUINE | SUSPICIOUS | ESCALATE | Document passes but agent shows fraud signals; default safe handling is escalation |
| SYNTHETIC/EDITED/SCREENSHOT | any | BLOCK | Document fails regardless of agent status |
| INSUFFICIENT | ATTESTED | REVIEW | Cannot assess document; agent verified |
| INSUFFICIENT | UNATTESTED | ESCALATE | Cannot assess either layer |

**Key principle:** A genuine document submitted by an unattested or suspicious agent should not result in automatic approval. The agent layer is not decorative — it is a primary signal.

Default policy sets `GENUINE + SUSPICIOUS -> ESCALATE`.  
`BLOCK` may be applied as an institution-specific override for high-risk segments or repeated suspicious patterns.

**Mode B note:** For **agent-mediated** submissions, institutions MAY map `FRC-L0-DATA-PATH-UNATTRIBUTED` or `FRC-L0-HANDOFF-UNAUDITED` to `agent_verdict = SUSPICIOUS` (or force `compound_verdict = ESCALATE`) even when the document layer is `GENUINE`, unless explicit policy accepts unattributed tool paths for that product.

---

## New Metrics for A2A Contexts

FRC A2A Extension adds the following metrics to the SDB-26 measurement framework:

### ABR — Agent Bypass Rate

ABR must be published in two variants:

**ABR_strict** — bypass only when suspicious agent-context submissions end in direct trust.

```
ABR_strict = (submissions with L0 flags AND compound_verdict = TRUSTED)
             / (total submissions with L0 flags)
```

**ABR_operational** — bypass according to operational semantics where `REVIEW` does not block risk exposure in the evaluated flow.

```
ABR_operational = (submissions with L0 flags AND compound_verdict ∈ OperationalBypassSet)
                  / (total submissions with L0 flags)
```

Where `OperationalBypassSet` must be disclosed explicitly (for example `{TRUSTED}` or `{TRUSTED, REVIEW}` depending on flow design).

**Interpretation:** High ABR indicates the agent verification layer is not effectively gating submissions. Institutions should report both variants together with policy mapping for interpretability.

### ACG — Agent Confidence Gap

**Definition:** Mean confidence score on submissions where L0 codes are present but compound verdict is TRUSTED.

**Interpretation:** High ACG indicates the system is near the approval boundary on suspicious agent submissions — small perturbations could flip the verdict. Low headroom for adversarial optimisation.

### CDR — Chain Depth Rate

**Definition:** Share of A2A submissions where the delegation chain depth exceeds a defined threshold (suggested: > 3 hops).

**Interpretation:** Longer chains increase the attack surface for chain forgery and reduce auditability. High CDR may indicate architectural decisions that should be reviewed.

### TCR — Tool Call Coverage Rate

**Definition:** Share of **agent-mediated** submissions where every material external/tool invocation has a log record linking `tool_id` (and, where applicable, `connector_id`) to `submission_id` within the retention window.

```
TCR = (agent-mediated submissions with full tool attribution)
      / (total agent-mediated submissions)
```

**Interpretation:** Low TCR means the environment cannot reconstruct *how* the dossier was built — undermining independent audit and post-incident review. Publish TCR only over windows where `n` meets the sample-size table below.

### HAR — Handoff Audit Rate

**Definition:** Share of multi-agent submissions where each orchestrator→worker handoff has a paired audit record (`from_agent_id`, `to_agent_id`, timestamp, declared scope or scope digest).

```
HAR = (multi-agent submissions with fully audited handoffs)
      / (total multi-agent submissions)
```

**Interpretation:** Low HAR indicates opaque internal delegation — the same class of risk as `FRC-L0-HANDOFF-UNAUDITED`, measured at corpus/system level.

**Publication:** As with ABR, optionally report **HAR_strict** vs **HAR_operational** depending on whether partial handoff logs count as sufficient for the evaluated policy.

---

## Minimum Sample Size Requirements

As with FRC v1.0, A2A metrics are subject to minimum sample size constraints:

| n | Publication rule |
|---|-----------------|
| < 20 | Metric not published |
| 20 ≤ n < 50 | Point estimate + 95% CI (Clopper-Pearson) |
| ≥ 50 | Point estimate + CI mandatory |

A2A contexts often have lower submission volumes than human onboarding flows. It is acceptable to accumulate data over longer windows before publishing ABR/ACG/CDR/TCR/HAR — but the window duration should be disclosed.

---

## INSUFFICIENT Handling in A2A

The INSUFFICIENT class takes on additional significance in A2A contexts:

**If agent is ATTESTED but document is INSUFFICIENT:**  
→ Request re-submission via the same attested agent. The agent identity is not in question; only the document quality.

**If agent is UNATTESTED and document is INSUFFICIENT:**  
→ Do not request re-submission until agent attestation is resolved. Requesting re-submission from an unattested agent generates more unverifiable data.

**If both layers are INSUFFICIENT:**  
→ Terminate session. Request human-initiated re-submission.

**Policy requirement:** INSUFFICIENT handling in A2A must be documented explicitly, including: what triggers re-submission, how many re-submission attempts are permitted before escalation, and what agent attestation is required for each attempt.

---

## Audit Trail Requirements

**Machine validation:** Conformant audit records MAY be validated with `schemas/frc_a2a_envelope_v0_2_0.json`. The nested `frc_payload` MUST satisfy `schemas/frc_schema_v1_0_0.json`.

For A2A submissions, the audit trail must include the core record below. **Agent-mediated (Mode B)** submissions SHOULD additionally include `instrumentation_trace` when any external tool or connector was used.

```json
{
  "a2a_extension_version": "0.2.0",
  "submission_id": "unique identifier",
  "submitted_at": "ISO-8601",
  "submission_mode": "human_direct | agent_submitted | agent_managed_package",
  "agent_id": "identifier of submitting agent",
  "agent_template_id": "optional — e.g. kyc-screener v1",
  "skills_manifest_hash": "optional — sha256 of bundled skills snapshot",
  "connector_manifest_hash": "optional — sha256 of .mcp.json or allowlist snapshot",
  "agent_assertion": "the identity claim provided (format-agnostic)",
  "chain_depth": 2,
  "principal_id": "identifier of authorising principal (if verifiable)",
  "l0_codes": ["FRC-L0-DATA-PATH-UNATTRIBUTED"],
  "document_codes": ["FRC-L1-FFT-GRID"],
  "compound_verdict": "TRUSTED | REVIEW | ESCALATE | BLOCK",
  "compound_confidence": 0.0,
  "hitl_checkpoint_id": "optional — recorded human approval correlation ID",
  "frc_payload": {
    "verdict": "GENUINE | FRAUD | INSUFFICIENT",
    "sdb26_class": "GENUINE | SYNTHETIC | SCREENSHOT | EDITED | INSUFFICIENT",
    "attack_level": "L1 | L2 | L3 | INF"
  },
  "instrumentation_trace": {
    "tool_invocations": [
      {
        "seq": 1,
        "tool_id": "exiftool.read_metadata",
        "connector_id": "internal.forensics",
        "invoked_at": "2026-05-06T12:00:01Z",
        "declared_permission_scope": "metadata_read",
        "args_digest": "sha256:…"
      }
    ],
    "subagent_handoffs": [
      {
        "from_agent_id": "orchestrator-1",
        "to_agent_id": "kyc-leaf-1",
        "handoff_at": "2026-05-06T12:00:00Z",
        "scope_digest": "sha256:…"
      }
    ]
  },
  "analyst_note": "human-readable for audit",
  "corpus_version": "SDB-26-A2A-v0.2"
}
```

**Minimum retention:** audit trail records must be retained for at least as long as the associated account or transaction relationship, or as required by applicable regulation — whichever is longer.

---

## Threat Model

This extension addresses the following threat actors:

**T1 — Automated synthetic identity pipeline**  
Adversary operates a pipeline that generates unique synthetic documents on-demand for each A2A submission. Goal: bypass per-document duplicate detection while maintaining submission velocity.  
*Primary codes:* FRC-L0-TEMPORAL-ANOMALY, FRC-L0-VELOCITY-FLAG, FRC-L1-FFT-GRID

**T2 — Compromised legitimate agent**  
A legitimate registered agent is compromised and used to submit fraudulent documents. Its attestation is valid; only document-level signals can detect the fraud.  
*Primary codes:* FRC-L0-AGENT-EXPIRED (if timely revocation exists), L1/L2/L3 codes for document

**T3 — Chain forgery**  
Adversary constructs a plausible delegation chain that terminates in a verifiable root but includes forged intermediate links.  
*Primary codes:* FRC-L0-CHAIN-BREAK, FRC-L0-AUTHORITY-MISMATCH

**T4 — Scope escalation**  
A legitimately attested agent performs actions outside its declared authority scope, potentially including submitting documents for principals it is not authorised to represent.  
*Primary codes:* FRC-L0-AUTHORITY-MISMATCH, FRC-L0-PRINCIPAL-ABSENT

**T5 — Instrumentation evasion**  
Adversary relies on plausible dossier text or stitched files while omitting or tampering with tool/connector logs so reviewers cannot reconstruct data provenance.  
*Primary codes:* FRC-L0-DATA-PATH-UNATTRIBUTED, FRC-L0-HANDOFF-UNAUDITED, FRC-L0-TOOL-PERMISSION-VIOLATION

---

## Relationship to Existing Standards

This framework is designed to be composable with:

- **W3C Verifiable Credentials** — for principal and agent identity claims
- **C2PA (Content Provenance and Authenticity)** — for document provenance signals
- **MCP (Model Context Protocol)** — for governed tool and data access; L0-D treats connector identity and logged invocations as forensic artefacts (not as a substitute for document FRC)
- **SPIFFE/SPIRE** — for workload identity in infrastructure contexts
- **OpenID Connect / OAuth 2.0** — for delegation and authority scope

**None of these are required.** The FRC A2A Extension defines what must be measured; institutions choose how to implement the underlying attestation.

Where an institution uses none of these standards, `FRC-L0-AGENT-UNATTESTED` applies by definition. The extension does not mandate a specific attestation technology — but it makes the absence of attestation a measurable, auditable finding.

---

## Relationship to deployed agent architectures

This extension is implementation-agnostic, but it is designed to map cleanly onto real multi-step agent deployments where workflows are assembled from:

- workflow-specific agent templates,
- governed data/tool connectors,
- orchestrator-to-worker delegation with auditable handoffs.

A concrete public reference context is Anthropic's financial-services repository and its KYC screening workflow template:

- Anthropic `KYC Screener` agent template (plugin context):  
  `plugins/agent-plugins/kyc-screener/`
- Managed deployment cookbook context:  
  `managed-agent-cookbooks/`

Repository: [https://github.com/anthropics/financial-services](https://github.com/anthropics/financial-services)

How FRC A2A maps in that context:

- `FRC-L0-DATA-PATH-UNATTRIBUTED` aligns with missing connector/tool attribution for material dossier claims.
- `FRC-L0-HANDOFF-UNAUDITED` aligns with missing correlation for orchestrator/worker delegation events.
- `FRC-L0-TOOL-PERMISSION-VIOLATION` aligns with calls outside session-bound tool scope.
- `TCR` and `HAR` provide system-level measurement of the same controls exposed in per-run logs.

This reference is illustrative, not normative. Any equivalent architecture can satisfy FRC A2A requirements if it provides measurable attestation, delegation integrity, and instrumentation traceability.

---

## Open Questions (Seeking Community Input)

1. **Threshold for FRC-L0-TEMPORAL-ANOMALY:** What is the appropriate time delta threshold between document creation and submission? 30 seconds is proposed; domain practitioners may have evidence for different values.
2. **Velocity thresholds for FRC-L0-VELOCITY-FLAG:** What N submissions in window T constitutes a flag? This likely varies by use case (retail onboarding vs. bulk institutional onboarding).
3. **Chain depth threshold for CDR:** Is 3 hops the right threshold? Some legitimate architectures may require deeper chains.
4. **Handling of partially attested chains:** Current framework distinguishes ATTESTED / PARTIALLY_ATTESTED / UNATTESTED. Is finer granularity needed?
5. **Interaction with existing fraud scoring:** How should L0 codes interact with behavioural fraud scores that operate at the session or account level?
6. **TCR / HAR thresholds:** Should a minimum acceptable TCR/HAR be normative for certain regulated flows, or left to institution disclosure only?
7. **What counts as “material” tool invocation:** Excluding low-risk steps (e.g. internal string normalisation) from mandatory logging — can we standardise an exclusion taxonomy?
8. **PII in instrumentation:** Recommended digests, field redaction lists, and retention caps for `args_digest` and connector payloads — community baseline for cross-border deployments.

Contributions via GitHub issue or pull request welcome.

---

## Calibration Guidance (v0.4 draft)

The following guidance is **non-normative** and intended for cross-team consistency when tuning thresholds before publishing ABR/TCR/HAR.

### 1) Velocity baseline (`FRC-L0-VELOCITY-FLAG`)

- Establish product-specific baseline windows (for example 7-14 days) before enabling hard gating.
- Segment baselines by flow type (`human_direct`, `agent_submitted`, `agent_managed_package`) and business channel.
- Start with percentile thresholds (for example P99 submissions/hour per `agent_id`) rather than fixed global limits.
- Record threshold source in policy docs and review quarterly, especially after onboarding automation changes.

### 2) Material tool invocation taxonomy (for TCR)

Define and publish which calls are **material** for audit attribution:

- **Material (include in TCR denominator):**
  - external data fetches (MCP/API/database reads that influence decision context),
  - file transformations that alter submitted evidence package,
  - rule/policy evaluation services producing decision-critical outputs.
- **Usually non-material (may be excluded if documented):**
  - deterministic string normalisation,
  - presentation formatting steps with no effect on evidence content.

Implementations SHOULD keep an explicit `MaterialToolSet` (or equivalent mapping) versioned alongside the workflow.

### 3) TCR and HAR rollout

- Phase 1 (observe): publish TCR/HAR as diagnostics, no auto-blocking.
- Phase 2 (soft control): map severe deficits (for example missing handoff audit on multi-agent flow) to `REVIEW`.
- Phase 3 (hard control): for high-risk products, map policy-defined failures (`FRC-L0-DATA-PATH-UNATTRIBUTED`, repeated `FRC-L0-HANDOFF-UNAUDITED`) to `ESCALATE` or `BLOCK`.

Where `REVIEW` is operationally equivalent to approval in a given flow, disclose this via `ABR_operational` and policy mapping.

---

### 4) Optional `agent_verdict` field in envelope

To make policy routing explicit across implementations, envelope schema `frc_a2a_envelope_v0_2_0.json` supports optional:

```json
"agent_verdict": "ATTESTED | PARTIALLY_ATTESTED | UNATTESTED | SUSPICIOUS"
```

This field is advisory and should remain consistent with `l0_codes` and `compound_verdict`.

Suggested consistency checks (implementation-level):

- `agent_verdict = UNATTESTED` should co-occur with at least one attestation/delegation L0 finding.
- `agent_verdict = SUSPICIOUS` should be explainable by high-risk behavioural/instrumentation L0 findings.
- `agent_verdict = ATTESTED` with severe L0-D signals should trigger policy review of mapping logic.

---

## Appendix: Investigator walkthrough — Mode A vs Mode B

This appendix orients **human reviewers and auditors** when both a nested `frc_payload` (document physics / metadata) and an **A2A audit envelope** are present.

### Mode A — Human-direct

1. Establish `submission_mode = human_direct` (or equivalent product classification).
2. Evaluate **document risk from `frc_payload` first** (`verdict`, `sdb26_class`, `primary_codes`, `attack_level`).
3. Treat **missing `instrumentation_trace`** as expected unless internal policy mandates pipeline logging for all channels — do **not** automatically raise `FRC-L0-DATA-PATH-UNATTRIBUTED` for Mode A without policy.
4. **`l0_codes` may be empty** when no agent identity is asserted; unresolved agent attestations (`FRC-L0-AGENT-UNATTESTED`, etc.) still map to escalation per the compound verdict matrix.

### Mode B — Agent-mediated

1. Establish `submission_mode = agent_managed_package` (or `agent_submitted` with documented partial instrumentation).
2. Evaluate **`frc_payload`** as in Mode A — document fraud dominates (`BLOCK`-class outcomes when class is SYNTHETIC/EDITED/SCREENSHOT regardless of agent layer).
3. In parallel, inspect **`instrumentation_trace`**: tool invocations MUST explain material external facts; handoffs SHOULD be pairwise auditable for multi-agent graphs (aligned with **HAR** in `STANDARD.md` §4.5 preview).
4. Cross-check **`l0_codes`** and optional **`hitl_checkpoint_id`** against institutional control requirements.

### Reference artefacts

Worked JSON and a checklist table:

- [`examples/frc/README.md`](../examples/frc/README.md) — step-by-step tables and narrative
- [`examples/frc/a2a_audit_mode_a_human_upload.json`](../examples/frc/a2a_audit_mode_a_human_upload.json) — Mode A (`GENUINE`, no instrumentation block)
- [`examples/frc/a2a_envelope_example.json`](../examples/frc/a2a_envelope_example.json) — Mode B (`FRAUD` document + tooling / handoffs)
- [`examples/frc/a2a_audit_insufficient_unattested_escalate.json`](../examples/frc/a2a_audit_insufficient_unattested_escalate.json) — `INSUFFICIENT + UNATTESTED => ESCALATE`
- [`examples/frc/a2a_audit_repeated_l0_pattern_block.json`](../examples/frc/a2a_audit_repeated_l0_pattern_block.json) — repeated L0 high-risk pattern with policy `BLOCK` override

Envelope schema version remains **`a2a_extension_version`: `0.2.0`** until a breaking envelope revision is published.

---

## Versioning

| Version | Changes |
|---------|---------|
| 0.1 | Initial draft. L0 code taxonomy, compound verdict matrix, ABR/ACG/CDR metrics, threat model. |
| 0.1.1 | Clarifications: policy-conditional handling for `FRC-L0-MODEL-UNDISCLOSED`; privacy note for `FRC-L0-SESSION-ANOMALY`; default `GENUINE + SUSPICIOUS -> ESCALATE`; formalized `ABR_strict` and `ABR_operational`. |
| 0.2 | L0-D instrumentation and data-path codes; submission modes A/B; TCR and HAR metrics; expanded audit trail (`instrumentation_trace`, template/manifest hashes, HITL correlation); threat actor T5; machine schema `schemas/frc_a2a_envelope_v0_2_0.json`. |
| 0.3 | Appendix: investigator Mode A vs Mode B walkthrough; `examples/frc/README.md` + Mode A envelope example; validator covers both envelope fixtures. |
| 0.4 | Added calibration guidance (velocity, MaterialToolSet, TCR/HAR rollout); added redacted Mode B examples for `ESCALATE` and `REVIEW` policy paths. |
| 0.5 | Added optional envelope guidance for explicit `agent_verdict`; added policy-path fixtures for `INSUFFICIENT + UNATTESTED => ESCALATE` and repeated L0 high-risk pattern => `BLOCK`. |

Next planned version (0.6): optional machine-readable policy profile examples (`OperationalBypassSet`, `MaterialToolSet`) and confidence calibration cookbook.

---

*SDB-26 FRC A2A Extension v0.5 — May 2026*  
*github.com/sevrusik/SDB-26 · sdb26.com*  
*Implementation-agnostic measurement framework. Not legal advice.*  
*Published under the same licence as SDB-26.*
