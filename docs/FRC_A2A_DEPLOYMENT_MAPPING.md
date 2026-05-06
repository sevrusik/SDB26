# FRC A2A Deployment Mapping (Reference Note)

This note provides an implementation-facing mapping from FRC A2A controls to operational observability fields and typical policy outcomes.

Scope:

- practical deployment interpretation for engineering/risk teams,
- reference context aligned with public agent architectures (including Anthropic KYC Screener templates),
- non-normative guidance that complements `docs/FRC_A2A_EXTENSION.md`.

Normative logic remains in:

- `docs/FRC_A2A_EXTENSION.md`
- `schemas/frc_a2a_envelope_v0_2_0.json`
- `schemas/frc_schema_v1_0_0.json`

---

## Reference architecture context

A representative deployed pattern is:

1. Orchestrator receives onboarding task.
2. Worker agents perform document checks and contextual enrichment.
3. Connectors/tools fetch external facts.
4. Aggregate package is submitted with audit fields.

Public reference context:

- Anthropic financial-services repository: [https://github.com/anthropics/financial-services](https://github.com/anthropics/financial-services)
- Template paths:
  - `plugins/agent-plugins/kyc-screener/`
  - `managed-agent-cookbooks/`

This is an example context only; equivalent architectures are fully compatible.

---

## Signal-to-observability mapping

| FRC signal | Minimum observability field(s) | Typical policy outcome |
|------------|--------------------------------|------------------------|
| `FRC-L0-AGENT-UNATTESTED` | `agent_assertion` absent/unverifiable; attestation check result | `ESCALATE` |
| `FRC-L0-CHAIN-BREAK` | delegation records (`from`, `to`, proof id), `chain_depth` | `REVIEW` or `ESCALATE` |
| `FRC-L0-AUTHORITY-MISMATCH` | declared scope, invoked action type, scope evaluation result | `ESCALATE` |
| `FRC-L0-DATA-PATH-UNATTRIBUTED` | missing/insufficient `instrumentation_trace.tool_invocations` for material claims | `ESCALATE` (or `BLOCK` for repeated high-risk flows) |
| `FRC-L0-HANDOFF-UNAUDITED` | missing `subagent_handoffs` correlation (`from_agent_id`, `to_agent_id`, `handoff_at`) | `REVIEW` -> `ESCALATE` if repeated |
| `FRC-L0-TOOL-PERMISSION-VIOLATION` | invocation outside bound permission scope | `ESCALATE` or `BLOCK` |
| `FRC-L0-MODEL-UNDISCLOSED` | missing model/capability declaration where policy requires it | `REVIEW` |
| `FRC-L0-HITL-ASSERTION-MISSING` | missing `hitl_checkpoint_id` when policy mandates HITL | `ESCALATE` |

Policy outcome is institution-specific. The table reflects common default mappings observed in risk-controlled deployments.

---

## Metric instrumentation map

| Metric | Required fields | Operational interpretation |
|--------|------------------|----------------------------|
| `ABR_strict` | `l0_codes`, `compound_verdict` | suspicious agent context reaching `TRUSTED` |
| `ABR_operational` | above + `OperationalBypassSet` policy | bypass under real flow semantics |
| `CDR` | `chain_depth` | delegation complexity/attack surface |
| `TCR` | material tool inventory + `tool_invocations` | completeness of evidence path attribution |
| `HAR` | multi-agent flag + `subagent_handoffs` | delegation audit completeness |

For comparability, publish:

- policy profile version,
- material-tool taxonomy version,
- report window and sample size.

---

## Minimal policy profile (illustrative)

```json
{
  "policy_profile_id": "kyc-a2a-prod-v3",
  "operational_bypass_set": ["TRUSTED"],
  "material_tool_set_version": "mts-2026-05",
  "hard_block_rules": [
    "repeat(FRC-L0-HANDOFF-UNAUDITED, 3, 24h)",
    "FRC-L0-TOOL-PERMISSION-VIOLATION"
  ],
  "hitl_required_for": ["high_value_onboarding", "sanctions_edge_cases"]
}
```

This profile is an optional ops artifact. It is not part of the core FRC payload schema.

Copy-ready JSON example: `examples/a2a_policy_profile_example.json`

Additional presets:

- `examples/a2a_policy_profile_strict.json` — stricter regulated posture.
- `examples/a2a_policy_profile_balanced.json` — higher-throughput balanced posture.

These presets are illustrative and must be calibrated to local legal and operational requirements.

---

## Implementation checklist

1. Emit schema-valid `frc_payload` for every decision.
2. Emit A2A envelope for agent-mediated flows (`submission_mode` set correctly).
3. Ensure material tool calls are attributable (`tool_id`, `invoked_at`, and connector identity where relevant).
4. Ensure subagent handoffs are correlated for multi-agent runs.
5. Store policy profile version with each report window for ABR/TCR/HAR interpretability.

