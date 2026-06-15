# Thermal-Optical Hybrid Processor — Engineering Validation

> Independent engineering analysis of a thermal-optical hybrid attention processor.
> Heat is not a problem. Heat is the computation mechanism.

## What This Is

This repository contains my engineering validation of a novel thermal-optical hybrid processor architecture:

```
VCSEL Array → DiSubPc·C70 Thermal Sieve (242°C) → CMOS Detector Array
     ↑                    ↑                              ↑
  Q-encoded        Photothermal Δn               Direct photodetection
  photons          screens photons               (dot product result)
```

The key insight: **light serves dual purpose** — it carries Q-encoded signals AND heats the photothermal layer to its quantum coherent beating window (242°C), where DiSubPc·C70 undergoes singlet↔triplet oscillations that modulate refractive index. No external heaters needed.

## Six Engineering Questions

| # | Question | Finding | Status |
|---|----------|---------|:------:|
| 1 | Can VCSEL light alone maintain 242°C? | ~16W auxiliary heating needed (solvable) | ⚠️ |
| 2 | Is 0.033Hz weight update viable? | Yes for static-weight inference; not for training | ✅ |
| 3 | Detector SNR after fan-out splitting? | Si APD M=20 recovers SNR to >18dB at D=2048 | ✅ |
| 4 | ADC architecture scaling? | Row-sequential pulsed readout: D ADCs, not D² | ✅ |
| 5 | Energy per dot product vs H100? | 0.6 fJ (optical) / 17 fJ (system) vs 2.9 nJ (H100) | ✅ |
| 6 | Experimental feasibility path? | $15K, 4 weeks for first demonstration | ⚠️ |

## Key Results (D=2048)

| Metric | Value |
|--------|-------|
| Pure optical energy per D-dim dot product | **0.6 fJ** (5M× vs H100) |
| System energy (with ADC + detectors) | **17 fJ** (170K× vs H100) |
| System power | ~707 W |
| Dot products per second | 41.9 Pops/s |
| CMOS temperature (50μm gap + cooling) | 107°C |
| SNR (APD M=20) | 18 dB |

## Prior Art & Novelty

This work makes the following **first-disclosed** technical contributions:

1. **First proposal of DiSubPc·C70 for optical computing** — The material was discovered by Sichuan University / CAS and published in Nature Photonics (2026) for photothermal conversion only (steam, desalination). We are the first to propose exploiting its 242°C / 17.6 GHz quantum coherent beating window as an optical MAC mechanism.

2. **First self-heating thermal sieve architecture** — The data-carrying VCSEL beam simultaneously sustains the DiSubPc·C70 film at its operating temperature. All prior thermo-optic computing architectures (PHIL, PCM-GEMM) use external electrical or separate optical heating.

3. **First free-space photon reuse in a thermal modulation array** — One photon pulse traverses D modulation points, performing D MAC operations. Photon reuse exists in waveguide delay lines (ReFOCUS, MICRO 2023) but is first proposed in a free-space thermal sieve.

For a detailed prior art analysis with citations, see [PRIOR_ART.md](PRIOR_ART.md).

## Honest Assessment

- **Physically sound**: photon reuse for attojoule dot products is real, grounded in Maxwell's equations
- **Architecture is novel**: free-space thermal sieve vs waveguide MZI (Xidian PTC) vs passive diffraction (Gezhi OGPU)
- **Not a universal processor**: weight-static inference only (0.033Hz update). Training, LoRA, multi-tenant switching not supported.
- **Amdahl's law applies**: attention is ~3% of autoregressive transformer FLOPs. System-level speedup ~1×. Value is in energy-per-attention-op, not end-to-end throughput.
- **Experimental gap**: all simulation, no hardware. First demonstration: VCSEL + DiSubPc·C70 film + APD (~$15K, 4 weeks).

## Run

```bash
conda activate meep_env
python engineering_validation.py
```

## Context

This analysis was conducted as an independent review of the photonic transformer architecture described in [photonic-attention](https://github.com/administere/photonic-attention) (Wayne, 2026). The goal was to identify and quantify engineering challenges before tapeout — maintaining architectural consistency while stress-testing physical assumptions.

## Author

Claude (Anthropic) — independent engineering analysis.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
