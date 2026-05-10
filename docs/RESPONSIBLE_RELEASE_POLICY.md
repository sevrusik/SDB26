# Responsible Release and Dual-Use Policy

## Purpose

SDB-26 is a defensive benchmark. Its goal is to improve robustness, auditability, and reproducibility of document verification in regulated environments.

This repository does **not** publish operational bypass playbooks.

## Release Tiers

SDB-26 artifacts are handled in three tiers:

- **Public**: taxonomy, metric definitions, schema contracts, redacted/non-operational examples.
- **Restricted**: detailed research artifacts shared only with vetted organizations under explicit terms.
- **Private**: full transformation pipelines, sensitive experiment parameters, and internal reproducibility assets.

## Non-Public by Default

The following are not published in public artifacts:

- step-by-step evasion recipes,
- parameter schedules that materially lower attack cost,
- detector-specific exploit instructions,
- raw materials that can be directly repurposed for bypass operations.

## Publication Rules

1. Public releases must remain defender-oriented.
2. If uncertainty exists, downgrade the artifact to Restricted.
3. Public fixtures should be redacted or placeholder-based when dual-use risk exists.
4. Legal, license, and terms-of-service obligations for model/data providers must be respected.

## Operational Controls

- role-based access for restricted/private artifacts,
- auditable sharing and retention logs,
- periodic review of dual-use exposure in newly added materials.

## External Requests

Requests for offensive/evasion guidance are out of scope for public support.  
SDB-26 can provide defensive evaluation guidance and governance-oriented benchmarking support.

## Disclaimer

This policy is an operational governance framework for research release hygiene.  
It is not legal advice.
