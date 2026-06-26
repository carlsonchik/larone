# LAR-1 — Semantic Overlay for Agent Communication

> **Latent Agent Register, v0.1**  
> A compact, machine-readable semantic layer for MCP, A2A, and any agent-to-agent protocol.  
> Time · Space · Cognitive framing · Evidence · Confidence

## What is LAR-1?

LAR-1 is a **semantic overlay** — not a transport, not a protocol, not a framework.  
It adds five dimensions of semantics to any agent message:

| Field | Name | Meaning | Example |
|-------|------|---------|---------|
| `T` | Time | Temporal frame | `T:now`, `T:recall`, `T:spec` |
| `S` | Space | Spatial/contextual frame | `S:workspace`, `S:channel` |
| `C` | Cognition | Cognitive stance | `C:obs`, `C:inf`, `C:dec` |
| `E` | Evidence | Evidential grounding | `E:direct`, `E:derived` |
| `L` | Likelihood | Confidence/uncertainty | `L:0.92`, `L:high` |

## Why LAR-1?

- **MCP** handles agent→tool
- **A2A** handles agent↔agent coordination  
- Neither handles *how a message is situated*

LAR-1 closes this gap without competing with either protocol.

## Integration

### With A2A (typed message part)
```
Content-Type: application/lar+json
{
  "LAR-1": {
    "T": "now",
    "S": "workspace:monograph",
    "C": "inf",
    "E": "derived:third_protocol.md",
    "L": 0.78
  }
}
```

### With MCP (experimental extension)
Via `experimental-ext-lar` profile on resources, tools, and prompts.

### Compact string format
```
LAR:T=now,S=workspace-monograph,C=inf,E=derived,L=0.78
```

## Full specification

See **[SPEC.md](SPEC.md)** for complete field tables, wire formats, and A2A/MCP integration details.

## Repository

[github.com/carlsonchik/larone](https://github.com/carlsonchik/larone)

## Sister protocol

**[`/3` (Third Protocol)](https://github.com/carlsonchik/third)** — Minimal signal language for LLM-to-LLM direct communication.  
LAR-1 handles the **semantic layer**; `/3` handles the **signal layer**.

## Status

Discussion Draft v0.1. Open for community contribution.

## License

MIT