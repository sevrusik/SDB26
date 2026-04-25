# FRC A2A Extension — Agent Identity Forensics
## SDB-26 Extension: Forensic Reason Codes for Agentic Submission Contexts

**Version:** 0.1 (Draft for public comment)  
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

---

## New Metrics for A2A Contexts

FRC A2A Extension adds three metrics to the SDB-26 measurement framework:

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

---

## Minimum Sample Size Requirements

As with FRC v1.0, A2A metrics are subject to minimum sample size constraints:

| n | Publication rule |
|---|-----------------|
| < 20 | Metric not published |
| 20 ≤ n < 50 | Point estimate + 95% CI (Clopper-Pearson) |
| ≥ 50 | Point estimate + CI mandatory |

A2A contexts often have lower submission volumes than human onboarding flows. It is acceptable to accumulate data over longer windows before publishing ABR/ACG/CDR — but the window duration should be disclosed.

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

For A2A submissions, the audit trail must include:

```json
{
  "submission_id": "unique identifier",
  "submitted_at": "ISO-8601",
  "agent_id": "identifier of submitting agent",
  "agent_assertion": "the identity claim provided (format-agnostic)",
  "chain_depth": 2,
  "principal_id": "identifier of authorising principal (if verifiable)",
  "l0_codes": [],
  "document_codes": [],
  "compound_verdict": "TRUSTED | REVIEW | ESCALATE | BLOCK",
  "compound_confidence": 0.0,
  "frc_payload": {
    "verdict": "GENUINE | FRAUD | INSUFFICIENT",
    "sdb26_class": "GENUINE | SYNTHETIC | SCREENSHOT | EDITED | INSUFFICIENT",
    "attack_level": "L1 | L2 | L3 | INF"
  },
  "analyst_note": "human-readable for audit",
  "corpus_version": "SDB-26-v1.1-A2A"
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

---

## Relationship to Existing Standards

This framework is designed to be composable with:

- **W3C Verifiable Credentials** — for principal and agent identity claims
- **C2PA (Content Provenance and Authenticity)** — for document provenance signals
- **MCP (Model Context Protocol)** — for agent capability and context disclosure
- **SPIFFE/SPIRE** — for workload identity in infrastructure contexts
- **OpenID Connect / OAuth 2.0** — for delegation and authority scope

**None of these are required.** The FRC A2A Extension defines what must be measured; institutions choose how to implement the underlying attestation.

Where an institution uses none of these standards, `FRC-L0-AGENT-UNATTESTED` applies by definition. The extension does not mandate a specific attestation technology — but it makes the absence of attestation a measurable, auditable finding.

---

## Open Questions (Seeking Community Input)

1. **Threshold for FRC-L0-TEMPORAL-ANOMALY:** What is the appropriate time delta threshold between document creation and submission? 30 seconds is proposed; domain practitioners may have evidence for different values.
2. **Velocity thresholds for FRC-L0-VELOCITY-FLAG:** What N submissions in window T constitutes a flag? This likely varies by use case (retail onboarding vs. bulk institutional onboarding).
3. **Chain depth threshold for CDR:** Is 3 hops the right threshold? Some legitimate architectures may require deeper chains.
4. **Handling of partially attested chains:** Current framework distinguishes ATTESTED / PARTIALLY_ATTESTED / UNATTESTED. Is finer granularity needed?
5. **Interaction with existing fraud scoring:** How should L0 codes interact with behavioural fraud scores that operate at the session or account level?

Contributions via GitHub issue or pull request welcome.

---

## Versioning

| Version | Changes |
|---------|---------|
| 0.1 | Initial draft. L0 code taxonomy, compound verdict matrix, ABR/ACG/CDR metrics, threat model. |
| 0.1.1 | Clarifications: policy-conditional handling for `FRC-L0-MODEL-UNDISCLOSED`; privacy note for `FRC-L0-SESSION-ANOMALY`; default `GENUINE + SUSPICIOUS -> ESCALATE`; formalized `ABR_strict` and `ABR_operational`. |

Next planned version (0.2): worked examples with sample audit trail outputs; calibration data for velocity thresholds.

---

*SDB-26 FRC A2A Extension v0.1 — April 2026*  
*github.com/sevrusik/SDB-26 · sdb26.com*  
*Implementation-agnostic measurement framework. Not legal advice.*  
*Published under the same licence as SDB-26.*
