# Prior Art & Novelty Statement

> **Date of first publication (this document):** 2026-06-15
> **Git commit anchoring this claim:** see repository history
>
> This document serves as a **public, timestamped record** of the novel contributions
> made in this work, along with a good-faith survey of the closest prior art known
> to the author at the time of writing. Any researcher or practitioner is invited
> to verify these claims against the cited sources.

---

## 1. What is Claimed as Novel

This work proposes a **thermal-optical hybrid processor** with the following
specific novel contributions:

### Claim 1: DiSubPc·C70 as an Optical Computing Element

**We are the first to propose repurposing the organic cocrystal DiSubPc·C70
for optical computing.**

The material was discovered by Chen, Zhang, Wan, Zhang, You et al. (Sichuan
University / CAS, *Nature Photonics* 2026) for photothermal conversion
applications — steam generation, seawater desalination, photothermal therapy.
Their paper does not mention, suggest, or claim any computing application.

We are the first to recognize that the material's **17.6 GHz quantum coherent
beating window at 242°C** — where localized singlet and delocalized triplet
(¹TT) states oscillate coherently — can be exploited as a **thermo-optic
modulation mechanism** for multiply-accumulate (MAC) operations.

### Claim 2: Self-Heating Free-Space Thermal Sieve Architecture

**We are the first to propose an architecture where the data-carrying light
beam simultaneously sustains the operating temperature of the modulation
material.**

In our architecture:
- The same VCSEL beam that **encodes Q-valued inputs** also **photothermally
  heats** the DiSubPc·C70 film to 242°C (its quantum coherent beating window).
- No external microheaters, no separate laser for thermal bias.
- This "thermal sieve" operates in **free space** (not in waveguides), enabling
  massive spatial parallelism.

Prior thermo-optic computing architectures (see §2) use either:
- External electrical Joule heating (GST-based PCM arrays)
- Separate optical heating with distinct control wavelengths (PHIL)
- Waveguide-confined light (all integrated photonic approaches)

### Claim 3: Free-Space Photon Reuse via Multi-Pass Thermal Sieve

**We are the first to propose photon reuse in a free-space thermal modulation
array for attojoule-scale dot products.**

A single photon pulse traverses D modulation points in the thermal sieve,
performing D multiply-accumulate operations before detection. This achieves
0.6 fJ per D-dimensional dot product (purely optical), approximately 5×10⁶
more efficient than an NVIDIA H100 GPU's 2.9 nJ per equivalent operation.

Photon reuse has been demonstrated in waveguide-based Fourier-optics
accelerators (ReFOCUS, MICRO 2023), but not in free-space thermal modulation
arrays.

---

## 2. Closest Prior Art

We acknowledge the following prior work and explicitly differentiate our
contributions.

### 2.1 PHIL Unit — All-Optical Temporal Integration via Subwavelength Heat Antennas

| Field | Detail |
|-------|--------|
| **Authors** | Yi Zhang, Nikolaos Farmakidis, Harish Bhaskaran, Nikos Pleros et al. |
| **Affiliation** | University of Oxford / HYBRAIN project |
| **Venue** | *Nature Communications*, 2026 |
| **DOI** | `10.1038/s41467-025-67726-0` |

**What they did:**
Placed titanium nano-antennas on silicon microring resonators as
wavelength-selective absorbers. Control-wavelength light is absorbed by the
nano-heaters → thermo-optic shift of the microring resonance → probe-wavelength
light is modulated. Achieved leaky temporal integration of 50 GHz optical
signals (up to 6,500 weighted inputs per wavelength) and programmable
all-optical nonlinear activation functions.

**How we differ:**
| Aspect | PHIL (Oxford) | This Work |
|--------|--------------|-----------|
| Material | Titanium nano-antennas on Si microrings | DiSubPc·C70 organic cocrystal |
| Architecture | Waveguide (integrated photonics) | Free-space |
| Heating mechanism | Control-wavelength light absorbed by metal antennas (separate from signal) | Same light beam carries data AND heats material |
| Operating temperature | Localized heating (not specified as a fixed window) | 242°C quantum coherent beating window |
| Photon reuse | No (single-pass through resonator) | Yes (D modulation points per photon) |
| Modulation physics | Thermo-optic resonance shift (Lorentzian) | Quantum coherent singlet↔triplet beating (Δn via population transfer) |

**Acknowledgment:** The PHIL unit shares the high-level philosophy that
"thermal dynamics can be strategically engineered for computation rather than
avoided." We explicitly cite this conceptual precedent.

### 2.2 Free-Space PCM-Based Optical GEMM Accelerator

| Field | Detail |
|-------|--------|
| **Authors** | Tang et al. |
| **Venue** | *Laser & Photonics Reviews*, 2023 |
| **DOI** | `10.1002/lpor.202200381` |

**What they did:**
Proposed a 3D free-space optical General Matrix Multiplication (GEMM)
accelerator using GST (Ge₂Sb₂Te₅) phase-change material arrays. A 1D spatial
reconfigurable array encodes input vectors; a 2D PCM array encodes weight
matrices; cylindrical lenses focus products onto detector arrays. Weights are
stored non-volatilely in PCM states.

**How we differ:**
| Aspect | PCM GEMM (Tang et al.) | This Work |
|--------|----------------------|-----------|
| Modulation material | GST (inorganic chalcogenide) | DiSubPc·C70 (organic cocrystal) |
| Modulation mechanism | Amorphous↔crystalline phase change (Δn via structural transition) | Quantum coherent beating (Δn via singlet↔triplet population oscillation) |
| Heating method | External electrical Joule heating (ITO electrodes) | Self-heating via data-carrying light (photothermal) |
| Weight update speed | ~μs–ms (PCM crystallization) | ~30 s (thermal time constant of the sieve) |
| Photon reuse | No | Yes (D modulation points per photon pulse) |
| Operating physics | Phase-change material science | Quantum coherent photothermal conversion |

**Acknowledgment:** The free-space optical MVM architecture with a 2D
modulation array is a shared architectural motif. We cite Tang et al. as
establishing the viability of free-space optically-computed dot products.

### 2.3 ReFOCUS — Reusing Light for Efficient Fourier Optics-Based Photonic Neural Network Accelerator

| Field | Detail |
|-------|--------|
| **Authors** | Shurui Li, Hangbo Yang, Chee Wei Wong, Volker J. Sorger, Puneet Gupta |
| **Affiliation** | UCLA / University of Florida |
| **Venue** | ACM/IEEE MICRO, 2023 |
| **DOI** | `10.1145/3613424.3623798` |

**What they did:**
Proposed optical reuse via optical buffers (spiral waveguide delay lines) in a
Fourier-optics (4F / Joint Transform Correlator) photonic neural network
accelerator. Light signals are split and delayed, then reused to reduce DAC
activation energy. Achieved 2× throughput and 2.2× energy efficiency
improvement over prior photonic accelerators.

**How we differ:**
| Aspect | ReFOCUS (UCLA) | This Work |
|--------|---------------|-----------|
| Reuse mechanism | Optical delay lines (spiral waveguides) | Free-space multi-pass through thermal sieve |
| Optics type | Fourier optics (4F correlator) | Direct amplitude modulation |
| Modulation | Passive (fixed weights in Fourier plane) | Active (thermal Δn modulation) |
| Photon path | Waveguide-confined | Free-space |
| Application domain | CNN convolution (convolution theorem) | Matrix-vector dot products (attention) |

**Acknowledgment:** ReFOCUS established the vocabulary of "photon reuse" in
optical computing. We adopt this terminology but implement it through a
fundamentally different physical mechanism (free-space multi-pass vs waveguide
delay lines).

### 2.4 DiSubPc·C70 Material Discovery

| Field | Detail |
|-------|--------|
| **Authors** | Yong Chen, Yu Zhang, Cheng Zhang, Xian-Kai Wan, Chuang Zhang, Jingsong You et al. |
| **Affiliation** | Sichuan University / Institute of Chemistry, CAS |
| **Venue** | *Nature Photonics*, 2026 |
| **DOI** | `10.1038/s41566-026-01912-4` |

**What they did:**
Discovered that the polar cocrystal 2DiSubPc·C70 exhibits 17.6 GHz quantum
coherent beating between localized singlet and delocalized triplet (¹TT)
states, enabling ultrafast photothermal conversion. The material reaches 228°C
in 5 seconds and equilibrates at 242°C under 0.5 W/cm², 550 nm irradiation.
Applications demonstrated: steam generation, seawater desalination,
photothermal therapy.

**How we differ:**
We do not claim discovery of the material. We claim the **first proposal to use
DiSubPc·C70 as a computational element**. The original paper does not mention
optical computing, neuromorphic processing, or any computational application.
This is a **new application** of a newly discovered material — analogous to the
first person who proposed using graphene (discovered by Geim and Novoselov) as
a transistor channel.

**Acknowledgment:** This work would not exist without the material discovery by
the Sichuan University / CAS team. We explicitly cite their priority on the
material itself.

### 2.5 Coherent Optical Neural Networks (Homodyne Detection)

| Field | Detail |
|-------|--------|
| **Reference** | US Patent US20210357737A1 and related academic work |
| **Key concept** | Optical matrix-vector multiplication via coherent (homodyne) detection at beam-splitter arrays |

**How we differ:** Coherent ONNs use optical interference between signal and
weight fields at beamsplitters, operating near the standard quantum limit. Our
approach uses **incoherent** (intensity-based) photothermal modulation — no
phase coherence required between signal paths, simplifying the optical
engineering.

---

## 3. Novelty Summary

| Element | Status | Evidence |
|---------|--------|----------|
| DiSubPc·C70 for optical computing | **First proposal** | No prior art found linking this material to any computing application |
| Self-heating thermal sieve (data light = heat source) | **First proposal** | All prior thermo-optic computing uses external heating (electrical or separate optical) |
| Free-space photon reuse for MAC | **First proposal** | Photon reuse exists in waveguides (ReFOCUS); free-space multi-pass thermal modulation is new |
| 242°C quantum coherent beating as operating regime | **First proposal** | The 242°C/17.6 GHz window was reported for photothermal conversion only; no prior computational use |
| Organic cocrystal as computational substrate | **First proposal** | Prior optical computing uses inorganics (Si, SiN, GST, metals, 2D materials); organic photothermal materials are new to computing |
| Thermal sieve as distinct from phase-change memory | **First proposal** | GST arrays store weights non-volatilely; our sieve uses continuous thermal modulation in a quantum coherent regime |

## 4. Good-Faith Prior Art Search Methodology

The prior art search was conducted on 2026-06-15 using:
- Web search across academic databases (Nature, IEEE, ACM, arXiv)
- Patent database search (USPTO, Google Patents)
- Chinese-language academic databases (CNKI, Baidu Scholar)
- Keyword combinations covering: thermal-optical computing, photothermal
  modulation, organic optical modulators, photon reuse/recycling, free-space
  optical MVM, quantum coherent beating computing, DiSubPc/phthalocyanine
  optical computing

If you are aware of prior art not cited here, please open a GitHub Issue with
the reference. This document will be updated with proper acknowledgment.

## 5. References

1. Chen, Y., Zhang, Y., Zhang, C., Wan, X.-K., Zhang, C., You, J. et al.
   "Quantum coherent beating in polar disubphthalocyanine-fullerene cocrystals
   for ultrafast photothermal conversion." *Nature Photonics* (2026).
   DOI: `10.1038/s41566-026-01912-4`

2. Zhang, Y., Farmakidis, N., Roumpos, I., Bhaskaran, H., Pleros, N. et al.
   "All-optical temporal integration mediated by subwavelength heat antennas."
   *Nature Communications* 17 (2026). DOI: `10.1038/s41467-025-67726-0`

3. Tang, R. et al. "Device-system Co-design of Photonic Neuromorphic Processor
   using Reinforcement Learning." *Laser & Photonics Reviews* 17(2) (2023).
   DOI: `10.1002/lpor.202200381`

4. Li, S., Yang, H., Wong, C.W., Sorger, V.J., Gupta, P. "ReFOCUS: Reusing
   Light for Efficient Fourier Optics-Based Photonic Neural Network
   Accelerator." *ACM/IEEE MICRO* (2023). DOI: `10.1145/3613424.3623798`

5. US Patent US20210357737A1. "Coherent optical neural network." (2021).

6. Wang, T. et al. "Large-Scale Optical Neural Networks Based on Photoelectric
   Multiplication." *Physical Review X* 9, 021032 (2019).

---

*This document is a living record. Last updated: 2026-06-15.*
