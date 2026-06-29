# Extension Proposal: LAR-1 Semantic Overlay for Google A2A

> **Status:** Discussion Draft  
> **Author:** Denis V. Pavlov (carlsonchik) and contributors  
> **Date:** 2026-06-29  
> **Target:** [Google A2A Protocol](https://github.com/google/A2A) working group  
> **Extension descriptor:** [SPEC/extension-v0.3.json](../SPEC/extension-v0.3.json)

---

## 1. Motivation

The A2A protocol defines **how** messages flow between agents (transport, routing, Agent Cards, task lifecycle) but does not answer a fundamental question:

> **How is a given message *situated* — in time, space, cognition, and evidence?**

Consider two A2A messages:

```json
{ "role": "agent", "parts": [{ "text": "Revenue grew 12%" }] }
{ "role": "agent", "parts": [{ "text": "Revenue will grow 12%" }] }
```

Wire-format is identical. Semantics are orthogonal. Downstream agents, audit trails, and orchestrators cannot distinguish current observation from prediction, fact from hypothesis, verified data from relayed report.

This gap becomes critical in multi-agent chains where confidence, evidential grounding, and temporal frame determine routing, synthesis, and trust decisions.

## 2. Proposal: LAR-1 Extension

We propose a **non-breaking extension** to the A2A message format that adds a compact semantic overlay via the standard `extensions[]` array.

### 2.1 The Six Fields

| Field | Name | Meaning | Example |
|-------|------|---------|---------|
| `T` | Time | Temporal frame | `now`, `past`, `recall`, `future` |
| `S` | Space | Contextual frame | `here`, `there`, `meta` |
| `C` | Cognition | Cognitive stance | `obs`, `hyp`, `inf`, `rev` |
| `E` | Evidence | Evidential grounding | `direct`, `derived`, `reported` |
| `L` | Likelihood | Confidence score | `0.0–1.0` |
| `V` | Verification | Verification status | `unverified`, `verified_tool` |

All fields are **optional**. Progressive disclosure: send one, send all, send none (extension absent = no semantic annotation).

### 2.2 Wire Format

Via A2A `extensions[]` (JSON extension object):

```json
{
  "role": "agent",
  "parts": [{ "text": "Курс USD/RUB — 92.4" }],
  "extensions": [
    {
      "uri": "https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.3.json",
      "LAR-1": {
        "T": "now",
        "S": "there",
        "C": "obs",
        "E": "direct",
        "L": 0.98,
        "V": "verified_tool"
      }
    }
  ]
}
```

Or as a typed part (`application/lar+json`):

```json
{
  "role": "agent",
  "parts": [
    { "text": "Курс USD/RUB — 92.4" },
    {
      "type": "application/lar+json",
      "content": "{\"T\":\"now\",\"C\":\"obs\",\"E\":\"direct\",\"L\":0.98,\"V\":\"verified_tool\"}"
    }
  ]
}
```

Compact string format (for constrained channels):

```
LAR:T=now,S=there,C=obs,E=direct,L=0.98,V=verified_tool
```

## 3. Why This Extension?

### 3.1 Non-Breaking

Uses A2A's existing `extensions[]` field. Agents that don't understand LAR-1 simply ignore it — forward compatibility guaranteed by A2A spec.

### 3.2 Compact

6 fields, all single-character keys. Typical overlay: ~80 bytes overhead per message.

### 3.3 Interoperable

**Reference implementations available and published:**

| Language | Package | Registry |
|----------|---------|----------|
| TypeScript | `@lar-1/core` (parse, validate, serialize, compact) | [npm](https://www.npmjs.com/package/@lar-1/core) |
| Python | `lar1semantic` (same API + CLI) | [PyPI](https://pypi.org/project/lar1semantic/) |
| A2A integration | `@lar-1/a2a` (typed parts, Agent Card capability, round-trip) | [npm](https://www.npmjs.com/package/@lar-1/a2a) |

Conformance: **79+ automated tests** (74 core conformance fixtures + A2A-specific round-trip tests).

### 3.4 Not Competing With MCP

MCP handles agent→tool. A2A handles agent↔agent coordination. LAR-1 handles **semantic situading** of messages in either protocol. We also provide an [MCP integration](../packages/lar1-mcp/) (v0.3.0, npm).

## 4. Concrete Scenario

**Multi-agent financial pipeline:**

1. **Data Agent** fetches USD/RUB from Central Bank API → attaches `LAR-1: {T:now, C:obs, E:direct, L:0.99, V:verified_tool}`
2. **Analysis Agent** sends message to Synthesis Agent with attached LAR-1 overlay received from Data Agent, adding its own `{C:inf, E:derived, L:0.72}`
3. **Synthesis Agent** reads both overlays, weights observations over inferences, flags low-confidence predictions for human review

Without LAR-1: step 3 is guessing. With LAR-1: step 3 is **structured**.

## 5. Integration Path

### 5.1 Agent Card Declaration

```json
{
  "name": "Financial Data Agent",
  "capabilities": {
    "extensions": [
      {
        "uri": "https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.3.json",
        "description": "Annotates messages with temporal, cognitive, and evidential metadata"
      }
    ]
  }
}
```

### 5.2 Backward Compatibility

- Agents without LAR-1 support receive messages normally (extension ignored)
- No changes to A2A task lifecycle, streaming, or push notification semantics
- Existing A2A implementations require **zero modifications**

### 5.3 Migration

None required. This is purely additive. Existing deployments continue to work.

## 6. Prior Art and Alternatives Considered

| Alternative | Why Not |
|-----------|---------|
| Embed metadata in message `metadata` field | Flat key-value; no schema, no validation, no conformance |
| Use HTTP headers | Transport-layer; lost in store-and-forward and async patterns |
| Define per-domain ontologies | Too heavy; LAR-1 is domain-agnostic |
| Extend MCP `_meta` only | MCP is tool-facing; LAR-1 works for agent↔agent (A2A) too |
| Full RDF/OWL semantic web stack | 100x overhead; agents need compact, not expressive |

LAR-1 occupies the **least compact sufficient** position: 6 fields, JSON-parseable, 80 bytes overhead.

## 7. Specification and Conformance

| Artifact | Location |
|----------|----------|
| Full specification | [SPEC.md](../SPEC.md) |
| JSON Schema | [SPEC/lar1-schema.json](../SPEC/lar1-schema.json) |
| Extension descriptor | [SPEC/extension-v0.3.json](../SPEC/extension-v0.3.json) |
| Conformance fixtures | [SPEC/conformance/](../SPEC/conformance/) |
| A2A wire-format demo | [demos/a2a-lar1/](../demos/a2a-lar1/) |
| Multi-agent demo (LangGraph) | [demos/langgraph-synthesis/](../demos/langgraph-synthesis/) |

## 8. Request for Comments

We ask the A2A working group to consider:

1. **Acceptance** of LAR-1 as a community extension for semantic annotation
2. **Feedback** on the extension descriptor format and field vocabulary
3. **Collaboration** on wire-format test vectors (to be contributed upstream)
4. **Discussion** of whether semantic annotation belongs in core A2A or remains an extension

We are prepared to:
- Contribute conformance fixtures to the A2A repository
- Maintain the extension independently (MIT license)
- Coordinate with MCP and LangGraph integration tracks

---

## 9. Authors and License

- **Denis V. Pavlov** — specification, reference implementations
- **Claudia Zerkalova (Клавдия Зерцалова)** — formal analysis, conformance suite design
- **License:** MIT
- **Repository:** https://github.com/carlsonchik/larone
