# FRC Codebook v1.0.0

## L1 — Synthetic generation

- `FRC-L1-FFT-GRID` — frequency-grid artifacts suggestive of synthetic generation.
- `FRC-L1-GEN-TEXTURE-UNIFORM` — unnatural texture/noise uniformity.
- `FRC-L1-SEM-INCOHERENCE` — logical inconsistency in document data (corroborating signal).
- `FRC-L1-ORNAMENT-ANOMALY` — anomalies in seals/guilloches/ornament elements.

## L2 — Manipulation/editing

- `FRC-L2-ELA-DIVERGENCE` — local recompression divergence in edited regions.
- `FRC-L2-FONT-INCONSISTENCY` — rendering/kerning inconsistencies indicating insertion.
- `FRC-L2-METADATA-WIPE` — metadata absent/reset or generic editor signatures (never sole reject reason).

## L3 — Screen recapture attacks

- `FRC-L3-MOIRE-PATTERN` — moire interference consistent with display recapture.
- `FRC-L3-RGB-SUBPIXEL-GRID` — display subpixel grid signatures.
- `FRC-L3-DOUBLE-COMPRESSION` — double JPEG compression indicators.

## INF — Insufficient evidence/quality

- `FRC-INF-LOW-RESOLUTION` — insufficient resolution for reliable forensic analysis.
- `FRC-INF-MOTION-BLUR` — blur blocks reliable signal extraction.
- `FRC-INF-EXIF-ABSENT` — no EXIF; alone is not fraud evidence.
- `FRC-INF-PARTIAL-DOCUMENT` — key regions/features missing from frame.
- `FRC-INF-GLARE-OBSTRUCTION` — glare obscures important security features.

## Notes

- Codes are probabilistic signals, not legal determinations.
- Cross-family convergence (for example, `fft + metadata + jpeg`) increases confidence.
- Keep code usage aligned with action policy in `docs/FRC_ACTION_MATRIX.md`.
