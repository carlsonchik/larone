## Update: LAR-1 v0.2/v0.3 — canonical spec, dual SDK, and A2A integration package

Following up on this thread with an **implementation-ready** profile aligned with the discussion here.

### Canonical repository

**https://github.com/carlsonchik/larone**

| Artifact | Link |
|----------|------|
| Spec (v0.2) | [SPEC.md](https://github.com/carlsonchik/larone/blob/main/SPEC.md) |
| JSON Schema | [SPEC/lar1-schema.json](https://github.com/carlsonchik/larone/blob/main/SPEC/lar1-schema.json) |
| Extension descriptor | [SPEC/extension-v0.2.json](https://github.com/carlsonchik/larone/blob/main/SPEC/extension-v0.2.json) |
| Conformance (74+ fixtures) | [SPEC/conformance/](https://github.com/carlsonchik/larone/tree/main/SPEC/conformance) |

### Extension URI (for `Message.extensions[]`)

```
https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.2.json
```

Resolves to machine-readable JSON (no custom domain required). See [HOSTING.md](https://github.com/carlsonchik/larone/blob/main/HOSTING.md).

### Media type

`application/lar+json`

### Six fields (v0.2)

| Field | Meaning | Example values |
|-------|---------|----------------|
| `T` | Temporal frame | `now`, `past`, `recall`, `future` |
| `S` | Context frame | `here`, `there`, `meta` |
| `C` | Cognition | `obs`, `hyp`, `mem`, `det`, `inf`, `rev` |
| `E` | Evidence | `direct`, `derived`, `aggregated`, `reported` |
| `L` | Likelihood | `0.0`–`1.0` |
| `V` | Verification | `unverified`, `verified_human`, `verified_tool`, `verified_crossref` |

`V` addresses the noisy-confidence problem raised in this thread — self-reported `L` without verification can mislead downstream agents (see also [LDP research](https://arxiv.org/abs/2603.08852)).

### Concrete A2A integration (`@lar-1/a2a`)

```typescript
import {
  createLar1Part,
  extractLar1,
  withLar1Extension,
  agentCardLar1Capability,
  LAR1_MEDIA_TYPE,
} from "@lar-1/a2a";

const message = withLar1Extension({
  role: "agent",
  parts: [
    { kind: "text", text: "Latency is 42ms p95." },
    createLar1Part({ T: "now", C: "obs", E: "direct", L: 0.92, V: "verified_tool" }),
  ],
});

const card = { capabilities: agentCardLar1Capability("0.2") };
```

Demo: [demos/a2a-lar1](https://github.com/carlsonchik/larone/tree/main/demos/a2a-lar1)

### Answers to original questions

1. **Should A2A define `application/lar+json` as a typed message part?**  
   **Yes** — as an optional typed `data` part + extension URI. Backward compatible; progressive disclosure (1–6 fields).

2. **Should trust calibration metadata be part of A2A task payloads?**  
   **Partially** — LAR-1 covers per-message semantics (`L`, `V`, `E`). Inter-agent alignment / escalation is complementary; we propose [`/3` (Third Protocol)](https://github.com/carlsonchik/third) as the signal layer for position and dissent (related to the Треть follow-up in this issue).

3. **How should confidence and evidence be represented in multi-agent workflows?**  
   Typed overlay on each message part; synthesizers route/filter by `C`, weight by `L × V`, require `E=direct` before destructive actions. [LangGraph demo](https://github.com/carlsonchik/larone/tree/main/demos/langgraph-synthesis) shows weighted synthesis.

### Reference implementations

| Package | Language |
|---------|----------|
| `@lar-1/core` | TypeScript |
| `@lar-1/a2a` | TypeScript |
| `@lar-1/mcp` | TypeScript |
| `lar-1` | Python |

Both TS and Python pass the same conformance fixtures (round-trip tested).

### Request to WG

We'd welcome guidance on:

- Registering `application/lar+json` in the A2A media-type / part registry
- Whether `extensions[]` should reference the raw JSON descriptor URL above
- A sample agent card extension in `a2aproject/A2A` samples/

Happy to open a focused PR on samples or docs if useful.

---

*Maintainer: [@carlsonchik](https://github.com/carlsonchik) · Related: [A2A #1974](https://github.com/a2aproject/A2A/issues/1974)*
