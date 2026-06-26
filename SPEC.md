# LAR-1 — Specification v0.1 (Discussion Draft)

> **Latent Agent Register** — Semantic Overlay for Agent Communication

## 1. Problem

Agent messages are routable before they are semantically legible.  
A task can be delegated and a tool called, yet downstream systems lack a compact representation of:

- Is this an observation or an inference?
- Is it grounded in current context or retrieved memory?
- Does it reflect ambiguity or final decision?
- What is the confidence level?

## 2. The Five Dimensions

### T — Temporal Frame

| Value | Meaning |
|-------|---------|
| `now` | Current, live, present moment |
| `recall:<id>` | Retrieved from memory/context |
| `spec:<range>` | Predictive, forward-looking |
| `static` | Timeless fact, invariant |
| `continuous` | Ongoing process |

### S — Spatial / Contextual Frame

| Value | Meaning |
|-------|---------|
| `workspace:<name>` | Specific workspace or project |
| `channel:<id>` | Communication channel |
| `agent:<id>` | Origin agent identifier |
| `external:<source>` | External source reference |

### C — Cognitive Stance

| Value | Meaning |
|-------|---------|
| `obs` | Observation — raw, unfiltered |
| `inf` | Inference — derived from observations |
| `dec` | Decision — committed choice |
| `exp` | Exploration — provisional, tentative |
| `meta` | About the conversation or cognition itself |
| `unc` | Uncertain — explicitly undecided |

### E — Evidential Grounding

| Value | Meaning |
|-------|---------|
| `direct:<source>` | Direct observation from source |
| `derived:<chain>` | Derived through reasoning chain |
| `speculative` | No direct evidence |
| `consensus:<agents>` | Agreement across multiple agents |
| `proxy:<indicator>` | Indirect evidence |

### L — Confidence / Uncertainty

| Value | Meaning |
|-------|---------|
| `0.0`–`1.0` | Floating-point confidence score |
| `high`/`medium`/`low` | Qualitative labels |
| `unknown` | Confidence not assessed |
| `contested:<agent>` | Disputed by another agent |

## 3. Wire Formats

### JSON (recommended for A2A)
```json
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

### Compact string
```
LAR:T=now,S=workspace-monograph,C=inf,E=derived-third_protocol,L=0.78
```

### MCP extension profile
```
experimental-ext-lar:
  T: now
  S: workspace:monograph
  C: inf
```

## 4. Integration with A2A

As typed message part:
```
Content-Type: application/lar+json
```

A2A agent cards include LAR-1 capability:
```json
{
  "capabilities": {
    "LAR-1": {
      "version": "0.1",
      "fields": ["T", "S", "C", "E", "L"]
    }
  }
}
```

## 5. Integration with MCP

Via `experimental-ext-lar` extension profile on:
- **resources** — annotate context with temporal/cognitive frame
- **tools** — tag tool calls with confidence and evidence
- **prompts** — describe cognitive stance of generated content

## 6. Design Principles

1. **Overlay, not replacement** — enriches existing protocols without modifying them
2. **Optional** — messages without LAR-1 continue to work normally
3. **Progressive** — agents can use 1 field or all 5
4. **Machine-readable** — designed for parsing, routing, filtering, auditing
5. **Human-readable** — all values are meaningful plain text

## 7. Status

Discussion Draft v0.1. Not yet adopted by any working group.  
Open for community feedback, implementation experiments, and real-world testing.

## 8. Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-06-22 | Initial discussion draft |
