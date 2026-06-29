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
├── packages/lar1-core/        # Reference TypeScript SDK
├── demos/langgraph-synthesis/ # Multi-agent demo
├── ROADMAP.md
├── ALTERNATIVES.md
└── GOVERNANCE.md
```

## Reference SDK

```bash
cd packages/lar1-core
npm install && npm test   # 74 conformance + round-trip tests
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
| **A2A** | `Content-Type: application/lar+json`, extension `https://lar-1.dev/ext/v0.2` |
| **MCP** | `_meta["lar-1"]` on tools, resources, results |
| **LangGraph** | `additional_kwargs["lar-1"]` — see [demo](demos/langgraph-synthesis/) |

## Documentation

- **[SPEC.md](SPEC.md)** — full field tables and wire formats
- **[ROADMAP.md](ROADMAP.md)** — development phases
- **[ALTERNATIVES.md](ALTERNATIVES.md)** — competitive landscape
- **[GOVERNANCE.md](GOVERNANCE.md)** — versioning and change process

## Sister protocol

**[`/3` (Third Protocol)](https://github.com/carlsonchik/third)** — minimal signal language for position and intent.  
LAR-1 handles the **semantic layer**; `/3` handles the **signal layer**.

## Status

**Stable draft v0.2** — normative schema, conformance suite, reference SDK.  
Open for community contribution.

## License

MIT
