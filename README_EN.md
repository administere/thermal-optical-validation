# ARIS Thermal-Optical Computing Lab

> An AI-driven automated validation environment for optical computing materials. Swap the material, keep the pipeline.

## What This Is

An [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)-powered engineering validation project for photothermal optical computing materials.

Core idea: use light for matrix multiplication, use heat to control refractive index. The key trick is **photon reuse** — one light pulse through 2048 modulation points = 2048 multiplications.

Currently based on DiSubPc·C70 (Nature Photonics 2026) experimental data, but the pipeline is **material-agnostic** — swap in TiO₂, VO₂, Sb₂S₃, or any thermo-optic material, and the analysis flow stays the same.

## Quick Start

```bash
git clone https://github.com/administere/thermal-optical-aris.git
cd thermal-optical-aris
bash setup-aris.sh   # One command: ARIS + 80 research skills + Python deps
claude               # Launch — all skills auto-loaded
```

No GPU required. No API key needed. Review mode defaults to manual (paste to any free model).

## ARIS Research Skills (inside claude)

| Command | Purpose |
|------|------|
| `/research-lit "topic"` | Multi-source literature review |
| `/idea-discovery "direction"` | Idea generation → novelty check |
| `/research-pipeline "direction"` | Full pipeline: lit → ideas → experiments → paper |
| `/auto-review-loop "paper"` | Auto review → fix → re-review |
| `/paper-writing "report"` | Plan → figures → LaTeX → PDF |

80 skills covering the entire research lifecycle.

## Analysis Pipeline

### Core Engineering
| Script | Purpose |
|------|--------|
| `工程验证.py` | Thermal coupling, SNR, noise budget, energy efficiency, D-scaling |
| `综合验证.py` | 8-subsystem multi-dimensional validation |
| `第一性原理.py` | Five theorems from Maxwell/Boltzmann first principles |
| `能量对比v2.py` | 5-scheme energy comparison (incl. quantum beat) |
| `FDTD光学验证.py` | MEEP full-wave electromagnetic simulation |

### Material Source Data
| Script | Purpose |
|------|--------|
| `材料源数据/吸收分析.py` | Urbach-tail extrapolation of absorption coefficient |
| `材料源数据/调制机制.py` | Three modulation mechanisms (thermal/electronic/quantum beat) |
| `材料源数据/晶体结构分析.py` | Cocrystal structure & χ⁽²⁾ nonlinearity |

### MZI Mesh Simulation
Clements unitary decomposition → SVD matrix multiplication → fidelity/crosstalk analysis, with 4-level verification tests.

## How to Swap Materials

1. Drop new material absorption/thermal data into `材料源数据/`
2. Update material constants in the scripts (density, MW, bandgap)
3. Run the chain:
   ```
   吸收分析.py → 调制机制.py → 工程验证.py → 能量对比v2.py
   ```
4. (Optional) Use ARIS `/research-lit` to auto-search competitor literature

## Energy Conclusions (DiSubPc·C70)

| Scheme | Energy/dot product | vs H100 |
|------|:--:|:--:|
| DiSubPc·C70 self-heating @ 850nm | 377,000 fJ | 8× |
| DiSubPc·C70 external heat @ 570nm | 706,000 fJ | 4× |
| TiO₂ external heat @ 570nm | 693,000 fJ | 4× |
| **DiSubPc·C70 quantum beat 17.6 GHz** | **14,000 fJ** | **199×** |

> H100 GPU: ~2,900,000 fJ/dot product

**Bottom line: classical thermo-optic is only a few × better than GPU. Quantum beat is the only path to an order-of-magnitude breakthrough.**

## Key Risks

1. **Quantum beat → optical modulation unverified**: paper only proves beats produce heat
2. **242°C long-term stability unknown**: MOESM7 only measured 45 minutes
3. **850nm absorption uncertain ~10×**: α = 35–3500 cm⁻¹
4. **dn/dT not directly measured**: using typical organic semiconductor values

## Related

**[Liberation Stele](https://github.com/administere/photothermal-liberation-stele)** — the other side of the coin: if everything goes right, how far can this go? Planetary-scale architectures, solar-sail constellations. Not feasibility — aspiration.

---

🤖 AI-assisted analysis · ARIS Automated Research Environment · [arXiv:2605.03042](https://arxiv.org/abs/2605.03042)
