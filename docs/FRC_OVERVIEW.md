# Forensic Reason Codes (FRC) Overview

FRC adds an explainability layer for document-risk decisions in SDB-26.
Instead of opaque `PASS/FAIL`, systems return structured evidence:

- machine-readable reason codes (`FRC-L1-*`, `FRC-L2-*`, `FRC-L3-*`, `FRC-INF-*`)
- confidence and evidence strength per code
- required operational action (`approve`, `manual_review`, `recapture_required`, `reject`)
- audit-ready forensic note

## Repository Map

- `docs/FRC_SCHEMA.md` — human-readable schema contract
- `docs/FRC_CODEBOOK.md` — code dictionary and semantics
- `docs/FRC_ACTION_MATRIX.md` — policy mapping from evidence to action
- `schemas/frc_schema_v1_0_0.json` — machine-validated JSON Schema
- `examples/frc/` — valid sample payloads; [examples/frc/README.md](examples/frc/README.md) documents Mode A vs Mode B investigator steps
- `tests/frc/` — valid/invalid fixtures for CI

## Core Principle

A decision without reasons is hard to audit.  
FRC makes decision logic traceable and testable.

## Minimal Payload

```json
{
  "verdict": "FRAUD",
  "sdb26_class": "SCREENSHOT",
  "primary_codes": [
    {
      "code": "FRC-L3-MOIRE-PATTERN",
      "confidence": 0.88,
      "evidence_strength": "strong"
    }
  ],
  "required_action": "manual_review"
}
```

## Validation

Use JSON Schema validation against `schemas/frc_schema_v1_0_0.json` in CI to ensure:

- field consistency (`verdict`, `sdb26_class`, `attack_level`)
- code namespace validity (`FRC-L1|L2|L3|INF-*`)
- guardrails (for example, metadata wipe cannot be sole reject reason)

## Agent-mediated submissions (A2A extension)

For **agent-to-agent** or managed-agent workflows, see [FRC_A2A_EXTENSION.md](FRC_A2A_EXTENSION.md).  
Audit records can be validated with `schemas/frc_a2a_envelope_v0_2_0.json` (nested `frc_payload` must still satisfy the core FRC schema).  
Run `python scripts/validate_frc_schemas.py` after `pip install -r requirements-dev.txt` to check reference fixtures (see repository root).
