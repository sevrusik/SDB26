# FRC reference examples

This directory contains machine-validated JSON aligned with `schemas/frc_schema_v1_0_0.json`, the A2A audit envelope (`schemas/frc_a2a_envelope_v0_2_0.json`), and — where present — A2A type surfaces in `schemas/a2a_v1_surfaces.json` (Task / TaskStatus enums aligned with the [A2A specification](https://a2a-protocol.org/latest/specification/)).

## Core FRC payloads (document layer only)

| File | Scenario |
|------|----------|
| `valid_genuine.json` | `verdict=GENUINE`, empty `primary_codes`, `approve` |
| `valid_fraud_l3.json` | Screen-recapture indicators, `manual_review` |
| `valid_insufficient.json` | Quality / evidence gap, `FRC-INF-*` primary |

Validate locally from repository root:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_frc_schemas.py
```

---

## A2A audit envelopes (document + submission context)

These wrap a full `frc_payload` **plus** L0 / audit fields. See [docs/FRC_A2A_EXTENSION.md](../../docs/FRC_A2A_EXTENSION.md).

### Mode A — Human-direct upload

**Story:** An end user completes onboarding from a mobile app and uploads a passport photo. There is no managed agent that assembles a dossier or calls external tools on their behalf.

**What to verify as an investigator**

1. Open `frc_payload` first — treat it like any document-only case (pixels, metadata, screenshot signals).
2. Check `submission_mode` is `human_direct`.
3. Expect **`instrumentation_trace` absent** (optional field). Lack of tool logs here is normal; do **not** apply `FRC-L0-DATA-PATH-UNATTRIBUTED` unless policy says every human channel must log internal pipeline steps (unusual).
4. **`l0_codes`** may be empty if no agent attestation exists. Escalation is driven by document FRC, not missing MCP logs.

**Example file:** [`a2a_audit_mode_a_human_upload.json`](a2a_audit_mode_a_human_upload.json)

---

### Mode B — Agent-mediated (managed package)

**Story:** A KYC screening orchestrator delegates to leaf workers, calls internal gateways, and may use governed connectors (MCP/API). The package delivered to compliance is tied to tool calls and handoffs.

**What to verify as an investigator**

1. Read **`instrumentation_trace.tool_invocations`**: each material external step should have `tool_id`, `invoked_at`, and correlatable identity (`connector_id` when relevant).
2. Read **`instrumentation_trace.subagent_handoffs`**: each orchestrator→worker step should pair with audit policy (matches `HAR` definitions in STANDARD §4.5 preview).
3. If dossier cites third-party facts but **no invocation** explains where they came from → investigate `FRC-L0-DATA-PATH-UNATTRIBUTED` (policy).
4. **`l0_codes`** and **`hitl_checkpoint_id`**: check policy-mandated human approval before submit.
5. **`compound_verdict`**: document failure (`FRC` fraud / synthetic) still **dominates** → typically `BLOCK` even if the agent layer looks clean.

**Example file:** [`a2a_envelope_example.json`](a2a_envelope_example.json) — includes optional `a2a_correlation` (`TASK_STATE_*`, Agent Card URI, protocol binding/version) for verifiers that record the upstream A2A Task.

---

### Mode B — Escalate and review variants

These fixtures cover two operationally common outcomes where the document layer remains `GENUINE`:

- **Escalate due to missing traceability:** [`a2a_audit_mode_b_escalate_missing_trace.json`](a2a_audit_mode_b_escalate_missing_trace.json)
  - `compound_verdict = ESCALATE`
  - `l0_codes` includes `FRC-L0-DATA-PATH-UNATTRIBUTED`
  - no `instrumentation_trace` block, matching a policy breach in Mode B
- **Review under partial attestation policy:** [`a2a_audit_mode_b_partial_attestation_review.json`](a2a_audit_mode_b_partial_attestation_review.json)
  - `compound_verdict = REVIEW`
  - example uses policy-conditional `FRC-L0-MODEL-UNDISCLOSED`
  - demonstrates `agent_submitted` middle mode

Use these to test downstream workflow routing (`TRUSTED` vs `REVIEW` vs `ESCALATE`) without changing the core FRC schema.

---

### Additional policy-path fixtures (v0.5)

- **INSUFFICIENT + UNATTESTED => ESCALATE**  
  [`a2a_audit_insufficient_unattested_escalate.json`](a2a_audit_insufficient_unattested_escalate.json)
  - aligns with A2A guidance: unresolved agent attestation blocks blind retry loops
  - includes `agent_verdict = UNATTESTED`

- **Repeated L0 high-risk pattern => BLOCK override**  
  [`a2a_audit_repeated_l0_pattern_block.json`](a2a_audit_repeated_l0_pattern_block.json)
  - demonstrates institution-specific hard override for repeated unattributed/handoff failures
  - includes `agent_verdict = SUSPICIOUS`

These are policy illustrations, not universal defaults.

---

### Mode — `agent_submitted` (optional middle case)

Use `agent_submitted` when a named bot or integration posts files **without** the full managed-agent cookbook (no subagent graph, partial logging). Document which fields are populated in your runbook; L0-D codes apply **only** where your policy promises instrumentation.

---

## Quick comparison

| Question | Mode A (human-direct) | Mode B (agent-mediated) |
|----------|------------------------|-------------------------|
| Is `instrumentation_trace` required? | No | Yes for material tool/connector use |
| Can `l0_codes` be empty? | Yes, if no agent claims | Possible; empty does not imply safe if logs are missing |
| Primary fraud signal | `frc_payload` | `frc_payload` **and** L0-D if policy applies |
| Typical `chain_depth` | `0` | `>= 1` when orchestrator + workers exist |
| Is `agent_verdict` required? | Optional | Optional but recommended for explicit routing |

---

## Redaction

Published fixtures use synthetic IDs and digests. Production logs must follow data-minimisation and retention rules; see FRC A2A Extension open questions on PII in `args_digest`.

Note: `agent_verdict` is optional in the envelope schema but recommended for explicit policy routing audits.
