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

### L2E-focused extensions (advanced post-processing/evasion)

- `FRC-L2-DCT-DOUBLE-COMP-ANOMALY` — DCT statistics indicate recompression chain anomalies (single vs double compression inconsistency).
- `FRC-L2-ELA-LOCAL-DIVERGENCE` — local/zonal ELA divergence indicates targeted blending or patch-level post-processing.
- `FRC-L2-PHASE-INCOHERENCE` — phase coherence mismatch despite plausible magnitude envelopes in frequency domain.
- `FRC-L2-INTERCHANNEL-NOISE-MISMATCH` — inter-channel noise correlation inconsistent with natural capture pipeline.
- `FRC-L2-SEMANTIC-TEXTURE-INCONSISTENCY` — semantic-texture mismatch surviving relaundering pipelines.

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

## L0 — Agent / submission context (A2A extension)

Agent-layer and instrumentation codes (`FRC-L0-*`) are defined in [FRC_A2A_EXTENSION.md](FRC_A2A_EXTENSION.md) (not in the core FRC v1.0 code namespace validated by `frc_schema_v1_0_0.json`).

## Notes

- Codes are probabilistic signals, not legal determinations.
- Cross-family convergence (for example, `fft + metadata + jpeg`) increases confidence.
- Keep code usage aligned with action policy in `docs/FRC_ACTION_MATRIX.md`.
