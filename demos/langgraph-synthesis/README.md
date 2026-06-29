# LangGraph Multi-Agent Synthesis Demo

Demonstrates **LAR-1** in a 3-agent LangGraph pipeline. No LLM API key required — agents are deterministic stubs.

## What it shows

| Agent | Role | LAR-1 tags |
|-------|------|------------|
| **Researcher** | Gathers facts | `C=obs`, high `L`, `V=verified_tool` |
| **Critic** | Challenges claims | `C=rev`, medium `L`, `V=unverified` |
| **Synthesizer** | Merges outputs | weights inputs by `L × C × V` |

**Baseline** treats every message equally. **With LAR-1** down-ranks hypotheses (`C=hyp`, low `L`) relative to verified observations.

## Requirements

- Python 3.10+
- Dependencies in [`requirements.txt`](./requirements.txt)

## Quick start

From the **repository root**:

```bash
cd demos/langgraph-synthesis
pip install -r requirements.txt
python -m synthesis.compare
```

Optional virtualenv (recommended):

```bash
cd demos/langgraph-synthesis
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m synthesis.compare
```

## Expected output

You should see two blocks:

1. **BASELINE** — all agent lines prefixed with `(equal)`
2. **WITH LAR-1** — lines prefixed with `(w=…)`; observation ~0.85, hypothesis ~0.06

## Project layout

```
demos/langgraph-synthesis/
├── README.md
├── requirements.txt
└── synthesis/
    ├── agents.py    # researcher, critic, synthesizer stubs
    ├── graph.py     # LangGraph StateGraph
    ├── lar1.py      # attach/read LAR-1 in additional_kwargs
    └── compare.py   # baseline vs LAR-1 entrypoint
```

## Run only the graph

```python
from synthesis.graph import run_pipeline

print(run_pipeline("agent protocols", use_lar1=True))
```

## Related

- [LAR-1 spec](../../SPEC/lar1-schema.json)
- [`@lar-1/core`](../../packages/lar1-core/) TypeScript reference SDK

## License

MIT
