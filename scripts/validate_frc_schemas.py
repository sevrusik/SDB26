#!/usr/bin/env python3
"""Validate FRC v1.0.0 and FRC A2A envelope v0.2.0 fixtures against canonical schemas.

Usage (from repository root):
  python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
  .venv/bin/python scripts/validate_frc_schemas.py

CI: see .github/workflows/frc-validate.yml
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
    from referencing import Registry, Resource
except ImportError:
    print(
        "Missing dependency: install with\n"
        "  python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt",
        file=sys.stderr,
    )
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
TESTS_FRC = ROOT / "tests" / "frc"
EXAMPLES_FRC = ROOT / "examples" / "frc"

FRC_URI = "https://sdb26.com/schemas/frc_schema_v1_0_0.json"
ENV_URI = "https://sdb26.com/schemas/frc_a2a_envelope_v0_2_0.json"
A2A_SURF_URI = "https://sdb26.com/schemas/a2a_v1_surfaces.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def frc_registry() -> tuple[dict, Registry]:
    frc = load_json(SCHEMAS / "frc_schema_v1_0_0.json")
    registry = Registry().with_resource(FRC_URI, Resource.from_contents(frc))
    return frc, registry


def envelope_registry() -> tuple[dict, Registry]:
    frc = load_json(SCHEMAS / "frc_schema_v1_0_0.json")
    envelope = load_json(SCHEMAS / "frc_a2a_envelope_v0_2_0.json")
    a2a_surfaces = load_json(SCHEMAS / "a2a_v1_surfaces.json")
    registry = (
        Registry()
        .with_resource(FRC_URI, Resource.from_contents(frc))
        .with_resource(A2A_SURF_URI, Resource.from_contents(a2a_surfaces))
        .with_resource(ENV_URI, Resource.from_contents(envelope))
    )
    return envelope, registry


def main() -> int:
    errors: list[str] = []

    frc_schema, _ = frc_registry()
    frc_validator = Draft202012Validator(frc_schema)

    for name in sorted(TESTS_FRC.glob("valid_*.json")):
        data = load_json(name)
        try:
            frc_validator.validate(data)
        except ValidationError as e:
            errors.append(f"FAIL {name.relative_to(ROOT)}: expected valid — {e.message}")

    for name in sorted(TESTS_FRC.glob("invalid_*.json")):
        data = load_json(name)
        try:
            frc_validator.validate(data)
            errors.append(f"FAIL {name.relative_to(ROOT)}: expected invalid, but schema accepted it")
        except ValidationError:
            pass

    for name in ("valid_genuine.json", "valid_fraud_l3.json", "valid_insufficient.json"):
        path = EXAMPLES_FRC / name
        if not path.is_file():
            errors.append(f"Missing example {path.relative_to(ROOT)}")
            continue
        try:
            frc_validator.validate(load_json(path))
        except ValidationError as e:
            errors.append(f"FAIL {path.relative_to(ROOT)}: {e.message}")

    envelope_schema, env_reg = envelope_registry()
    env_validator = Draft202012Validator(envelope_schema, registry=env_reg)
    a2a_examples = sorted(EXAMPLES_FRC.glob("a2a_*.json"))
    if not a2a_examples:
        errors.append("Missing A2A examples: expected at least one examples/frc/a2a_*.json")
    for path in a2a_examples:
        if not path.is_file():
            errors.append(f"Missing A2A example {path.relative_to(ROOT)}")
            continue
        try:
            env_validator.validate(load_json(path))
        except ValidationError as e:
            errors.append(f"FAIL {path.relative_to(ROOT)}: {e.message}")

    if errors:
        print("FRC schema validation failed:\n", file=sys.stderr)
        for line in errors:
            print(f"  {line}", file=sys.stderr)
        return 1

    print("OK: all FRC fixtures, core examples, and A2A envelope examples validate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
