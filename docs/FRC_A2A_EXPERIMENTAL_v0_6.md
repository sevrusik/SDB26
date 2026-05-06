# FRC A2A Experimental Track v0.6 (Non-normative)

This document captures exploratory extensions for autonomous/multi-agent risk controls.

Status:

- Experimental (not part of the normative v0.5 contract)
- Not required for v1.0.x conformance
- Intended for field testing and community feedback

Normative references remain:

- `docs/FRC_A2A_EXTENSION.md`
- `schemas/frc_a2a_envelope_v0_2_0.json`
- `schemas/frc_schema_v1_0_0.json`

---

## Why this track exists

The core A2A extension v0.5 focuses on identity, delegation, and instrumentation traceability.
Emerging multi-agent deployments introduce additional failure modes that may require explicit control classes and metrics before becoming normative.

This track isolates those candidates so the standard can stay stable while experimentation continues.

---

## Candidate L0 classes (proposed)

These codes are proposed for testing and are not yet part of normative code dictionaries:

- `FRC-L0-GOAL-MISALIGNMENT`
- `FRC-L0-COORDINATION-FAILURE`
- `FRC-L0-FEEDBACK-LOOP`
- `FRC-L0-CASCADE-ERROR`
- `FRC-L0-UNBOUNDED-EXECUTION`

---

## Candidate envelope fields (proposed)

Optional fields for pilots (outside normative schema):

- `autonomy_level` (`ASSISTED | SEMI_AUTONOMOUS | AUTONOMOUS`)
- `max_action_scope` (string policy reference)
- `requires_human_checkpoint` (boolean)
- `instrumentation_trace.guardrail_events[]`

Suggested `guardrail_events[]` shape:

```json
{
  "event_type": "policy_violation | loop_detected | manual_override",
  "event_at": "ISO-8601 timestamp",
  "policy_ref": "internal policy key",
  "action_taken": "review | escalate | block | continue"
}
```

---

## Candidate metrics (proposed)

### GVR — Governance Violation Rate

Share of agent-mediated runs with one or more guardrail violations.

### AII — Autonomy Intervention Index

Human interventions per 100 agent-mediated runs, segmented by autonomy level.

---

## Experimental fixtures

See:

- `examples/frc/experimental/a2a_exp_goal_misalignment_review.json`
- `examples/frc/experimental/a2a_exp_feedback_loop_escalate.json`

These fixtures are intentionally excluded from normative schema CI in v1.0.x.

---

## Graduation criteria to normative track

A candidate control should move from experimental to normative only after:

1. Consistent semantics across at least two independent deployments.
2. Stable observability fields and low ambiguity in interpretation.
3. Demonstrated utility in reducing false trust decisions.
4. Community review and changelog transparency.

