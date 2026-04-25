# FRC Action Matrix v1.0.0

## Goal

Map forensic evidence to consistent operational outcomes.

## Decision rules

| Condition | Required action | Default verdict |
|---|---|---|
| Any primary `FRC-INF-*` | `recapture_required` | `INSUFFICIENT` |
| Strong L3 evidence or multiple moderate L3 signals | `manual_review` (+ recapture recommendation) | `FRAUD` / `SCREENSHOT` |
| Strong L2 evidence + corroboration | `manual_review` or `reject` (policy) | `FRAUD` / `EDITED` |
| Strong L1 evidence + corroboration | `manual_review` or `reject` (policy) | `FRAUD` / `SYNTHETIC` |
| Weak-only mixed evidence | `manual_review` | `INSUFFICIENT` |
| No suspicious primary evidence and quality sufficient | `approve` | `GENUINE` |

## Guardrails

1. `FRC-L2-METADATA-WIPE` cannot be the sole reject reason.
2. Reject decisions should include either:
   - one strong primary + independent corroboration, or
   - policy override with explicit rationale.
3. Every non-approve outcome must include:
   - at least one primary code,
   - forensic note,
   - required action.

## SDB-26 linkage

- L1 -> `SYNTHETIC`
- L2 -> `EDITED`
- L3 -> `SCREENSHOT`
- INF -> `INSUFFICIENT`
