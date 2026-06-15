# OpenTimestamps Proofs

These `.ots` files are [OpenTimestamps](https://opentimestamps.org/) proofs that
anchor the content hashes of the core project files to the **Bitcoin blockchain**,
providing cryptographic, trustless proof that these files existed at a specific
point in time.

## How to Verify

```bash
# Install OpenTimestamps client
pip install opentimestamps-client

# Verify a proof (run from repo root, where the original .md file exists)
cd /home/wayne/thermal-optical-validation
ots verify .ots/PRIOR_ART.md.ots

# Or specify the target file explicitly
ots verify -f PRIOR_ART.md .ots/PRIOR_ART.md.ots
```

## What Gets Timestamped

The OTS proof stores the SHA-256 hash of the file at the time of stamping.
If the file is modified after stamping, verification will fail — this is by design.
The proof demonstrates that the **exact content** of the file existed before the
Bitcoin block height recorded in the proof.

## Files Under Timestamp Protection

| File | Description |
|------|-------------|
| `PRIOR_ART.md.ots` | Prior art analysis and novelty claims |
| `README.md.ots` | Chinese README with originality statement |
| `README_EN.md.ots` | English README with originality statement |
| `comprehensive_validation.py.ots` | Full engineering validation code |
| `engineering_validation.py.ots` | Core validation code |
| `first_principles.py.ots` | First principles analysis |

## Initial Timestamp

- **Created:** 2026-06-15
- **Calendar servers:** OpenTimestamps public pool, Eternity Wall, Catallaxy
- **Status:** Pending Bitcoin confirmation (typically 1-6 blocks, ~10-60 minutes)

After Bitcoin confirmation, re-run `ots upgrade .ots/*.ots` to complete the
anchoring. Once upgraded, the proof can be verified independently by anyone,
anywhere, without trusting any third party.
