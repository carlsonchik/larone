# LAR-1 — Semantic Overlay for Agent Communication

> **Latent Agent Register, v0.2**  
> A compact, machine-readable semantic layer for MCP, A2A, and any agent-to-agent protocol.  
> Time · Space · Cognition · Evidence · Likelihood · Verification

## What is LAR-1?

LAR-1 is a **semantic overlay** — not a transport, not a protocol, not a framework.  
It adds six dimensions of semantics to any agent message:

| Field | Name | Example |
|-------|------|---------|
| `T` | Time | `now`, `past`, `recall`, `future` |
| `S` | Space | `here`, `there`, `meta` |
| `C` | Cognition | `obs`, `hyp`, `inf`, `rev` |
| `E` | Evidence | `direct`, `derived`, `aggregated` |
| `L` | Likelihood | `0.78` (0.0–1.0) |
| `V` | Verification | `unverified`, `verified_tool` |

## Why LAR-1?

- **MCP** handles agent→tool
- **A2A** handles agent↔agent coordination  
- Neither handles *how a message is situated*

LAR-1 closes this gap without competing with either protocol.

## Quick example

**JSON** (`application/lar+json`):

```json
{
  "LAR-1": {
    "T": "now",
    "S": "here",
    "C": "obs",
    "E": "direct",
    "L": 0.95,
    "V": "verified_tool"
  }
}
```

**Compact:**

```
LAR:T=now,S=here,C=obs,E=direct,L=0.95,V=verified_tool
```

## Repository layout

```
larone/
├── SPEC.md                    # Human-readable specification
├── SPEC/lar1-schema.json      # Normative JSON Schema
├── SPEC/conformance/          # Test vectors (74 cases)
├── packages/lar1-core/        # TypeScript SDK
├── packages/lar1-python/      # Python SDK + CLI
├── packages/lar1-cli/         # Node CLI
├── demos/langgraph-synthesis/ # Multi-agent demo
├── ROADMAP.md
├── ALTERNATIVES.md
└── GOVERNANCE.md
```

## Reference SDK

**TypeScript** (`packages/lar1-core`):

```bash
cd packages/lar1-core
npm install && npm test   # 74 conformance + round-trip tests
```

**Python** (`packages/lar1-python`):

```bash
cd packages/lar1-python
pip install -e ".[dev]" && pytest -q
```

**CLI** (both ecosystems):

```bash
lar1 validate "LAR:C=obs,L=0.9,V=verified_tool"
lar1 compact message.json
lar1 json "LAR:T=now,C=inf,L=0.7"
```

```ts
import { parse, compact, serialize, validate } from "@lar-1/core";

const data = parse("LAR:C=obs,L=0.9,V=verified_tool");
validate(data);           // true
compact(data);            // canonical compact string
serialize(data);          // application/lar+json
```

## Integration

| Platform | How |
|----------|-----|
| **A2A** | `Content-Type: application/lar+json`, [extension descriptor](SPEC/extension-v0.2.json) |
| **MCP** | `_meta["lar-1"]` on tools, resources, results |
| **LangGraph** | `additional_kwargs["lar-1"]` — see [demo](demos/langgraph-synthesis/) |

## Documentation

- **[SPEC.md](SPEC.md)** — full field tables and wire formats
- **[ROADMAP.md](ROADMAP.md)** — development phases
- **[ALTERNATIVES.md](ALTERNATIVES.md)** — competitive landscape
- **[GOVERNANCE.md](GOVERNANCE.md)** — versioning and change process
- **[HOSTING.md](HOSTING.md)** — URI strategy (GitHub raw vs custom domain)
- **[PUBLISHING.md](PUBLISHING.md)** — npm and PyPI publish steps

## Sister protocol

**[`/3` (Third Protocol)](https://github.com/carlsonchik/third)** — minimal signal language for position and intent.  
LAR-1 handles the **semantic layer**; `/3` handles the **signal layer**.

## Status

**Stable draft v0.3** — dual SDK (TypeScript + Python), CLI, conformance suite.  
Open for community contribution.

## License

MIT
