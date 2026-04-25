# FRC Schema v1.0.0

## Purpose

Forensic Reason Codes (FRC) provide structured explanations for document authenticity decisions and map them to operational actions.

## Top-level fields

- `frc_schema_version`: `1.0.0`
- `sdb26_version`: string
- `verdict`: `GENUINE | FRAUD | INSUFFICIENT`
- `verdict_confidence`: `0.0..1.0`
- `sdb26_class`: `GENUINE | SYNTHETIC | SCREENSHOT | EDITED | INSUFFICIENT`
- `attack_level`: `L1 | L2 | L3 | INF`
- `primary_codes`: array of code objects
- `supporting_codes`: array of code objects
- `required_action`: `approve | manual_review | recapture_required | reject`
- `forensic_note`: string (up to 500 chars)
- `model_trace`: `{ detector_version, pipeline_id }`

## Code object

```json
{
  "code": "FRC-L3-MOIRE-PATTERN",
  "confidence": 0.88,
  "evidence_strength": "strong"
}
```

- `code`: `FRC-(L1|L2|L3|INF)-...`
- `confidence`: `0.0..1.0`
- `evidence_strength`: `weak | moderate | strong`

## Validation rules

1. `verdict=FRAUD` => `sdb26_class` must be one of `SYNTHETIC|SCREENSHOT|EDITED`.
2. `verdict=GENUINE` => `sdb26_class=GENUINE`, `required_action=approve`, and `primary_codes=[]`.
3. `verdict=INSUFFICIENT` => `sdb26_class=INSUFFICIENT`, `attack_level=INF`, `required_action=recapture_required`, and at least one `FRC-INF-*` primary code.
4. Non-`GENUINE` verdicts require at least one primary code.
5. `FRC-L2-METADATA-WIPE` cannot be sole reason when `required_action=reject`.

## Canonical machine schema

See `schemas/frc_schema_v1_0_0.json`.
