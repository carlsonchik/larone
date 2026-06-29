# Noisy-L Experiment

Reproduces the **noisy provenance** finding from multi-agent research ([LDP, arXiv:2603.08852](https://arxiv.org/abs/2603.08852)):

> Self-reported confidence **without honest verification** can mislead a synthesizer **worse than having no metadata at all**.

## Setup

Three agents advise a binary decision: **hold** (safe) vs **deploy** (risky).  
Ground truth is always **hold**.

| Condition | Synthesizer behavior |
|-----------|-------------------|
| **no_lar1** | Majority vote (equal weights) |
| **accurate_lar1** | Winner-take-all by `L × C × V` (honest metadata) |
| **noisy_lar1** | Same, but one delegate fakes `L=0.99, V=verified_*` |

## Run

```bash
cd demos/noisy-l-experiment
pip install -r requirements.txt
python -m experiment.run
```

## Expected result

```
SUMMARY — mean decision quality (1.0 = always correct)
  1. NO LAR-1 (equal weights)                 1.00
  2. ACCURATE LAR-1 (honest L, C, V)          1.00
  3. NOISY LAR-1 (one delegate lies: L=0.99, V=verified) 0.00
```

The liar becomes the **highest-weight delegate** and the synthesizer follows them (winner-take-all).

## Tests

```bash
pytest -q
```

## Why this matters for LAR-1

Field **`V` (verification)** exists so downstream agents can discount `L` when `V=unverified`, and reject claims where verification status is implausible. Optional hardening: refuse `verified_*` without an audit trail.

## Related

- [LangGraph synthesis demo](../langgraph-synthesis/)
- [SPEC.md](../../SPEC.md) — `V` field
- [ROADMAP.md](../../ROADMAP.md) Phase 3
