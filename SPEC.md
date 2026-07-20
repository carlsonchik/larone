# LAR-1 — Specification v0.4 (Discussion Draft)

> **Latent Agent Register** — Semantic Overlay for Agent Communication

**Normative artifacts:**

| Artifact | Path |
|----------|------|
| JSON Schema | [`SPEC/lar1-schema.json`](SPEC/lar1-schema.json) |
| Conformance fixtures | [`SPEC/conformance/`](SPEC/conformance/) |
| Extension descriptor | [`SPEC/extension-v0.4.json`](SPEC/extension-v0.4.json) |
| Reference implementation | [`packages/lar1-core/`](packages/lar1-core/) |

**Extension URI (A2A `extensions[]`):** `https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.4.json`  
**Media type:** `application/lar+json`

---

## 1. Problem

Agent messages are routable before they are semantically legible.  
A task can be delegated and a tool called, yet downstream systems lack a compact representation of:

- Is this an observation or an inference?
- Is it grounded in current context or retrieved memory?
- Does it reflect ambiguity or a committed judgment?
- What is the confidence level — and has it been verified?
- **How much reasoning effort was invested in producing this claim?**

Modern LLMs (GPT-5.6, DeepSeek-R1, Claude) support multiple reasoning-effort levels. Without an explicit field, a downstream agent cannot distinguish between a quick heuristic answer and a deeply reasoned one — even when both carry high confidence.

## 2. The Seven Dimensions

All fields are **optional**; send one or more (progressive disclosure). At least one field is required per message overlay.

### T — Temporal Frame

| Value | Meaning |
|-------|---------|
| `now` | Current, live, present moment |
| `past` | Historical, already occurred |
| `recall` | Retrieved from memory or context store |
| `future` | Predictive, forward-looking |

### S — Spatial / Contextual Frame

| Value | Meaning |
|-------|---------|
| `here` | Current workspace, session, or local context |
| `there` | External or remote context |
| `meta` | About the conversation, protocol, or cognition itself |

### C — Cognitive Stance

| Value | Meaning |
|-------|---------|
| `obs` | Observation — raw, unfiltered |
| `hyp` | Hypothesis — provisional, testable |
| `mem` | Memory — recalled content |
| `det` | Detection — pattern or signal identified |
| `inf` | Inference — derived from other observations |
| `rev` | Review — critical evaluation of prior claims |

### E — Evidential Grounding

| Value | Meaning |
|-------|---------|
| `direct` | Direct observation or primary source |
| `derived` | Derived through reasoning chain |
| `aggregated` | Combined from multiple sources |
| `reported` | Relayed from another party without direct verification |

### L — Likelihood / Confidence

| Value | Meaning |
|-------|---------|
| `0.0`–`1.0` | Floating-point confidence score (inclusive) |

`L` is numeric only in v0.2. Qualitative labels (`high`/`low`) were removed for machine-parseability.

### V — Verification Status

| Value | Meaning |
|-------|---------|
| `unverified` | Default — confidence/evidence not independently checked |
| `verified_human` | Confirmed by a human reviewer |
| `verified_tool` | Confirmed by an automated tool or test |
| `verified_crossref` | Confirmed by cross-reference with another source |
| `verified_peer` | Validated by peer agent(s) via reputation, tipping, or interaction history |

> **Note:** Research on multi-agent provenance (e.g. LDP) shows that self-reported confidence without verification can mislead downstream agents. Always pair meaningful `L` values with an accurate `V`.

### R — Reasoning Effort (new in v0.4)

| Sub-field | Type | Required | Description |
|-----------|------|----------|-------------|
| `R` | float (0.0–1.0) | ✅ yes | Normalized reasoning effort, relative to the model's maximum |
| `R_raw` | int | ❌ | Original value on the model's native scale |
| `R_scale` | int | ❌ | Maximum of the model's native scale |
| `R_label` | string | ❌ | Human-readable label (e.g. `low`, `medium`, `high`, `max`, `ultra`) |
| `R_strategy` | string | ❌ | Reasoning method used to produce the claim. See table below. |

**R_strategy values:**

| Value | Meaning |
|-------|---------|
| `cot` | Chain-of-thought — sequential reasoning |
| `tot` | Tree-of-thought — branching, path exploration |
| `debate` | Multi-perspective debate or dialogue |
| `tool-use` | Tool invocation and result aggregation |
| `reflection` | Iterative self-check, self-correction |
| `intuition` | Direct response without explicit intermediate reasoning |

**R_strategy vs C (Cognitive Stance):** `C` answers *what kind of claim this is* (observation, inference, hypothesis, etc.). `R_strategy` answers *how the claim was produced* (chain-of-thought, tool-use, etc.). They are orthogonal:

| C | R_strategy | Meaning |
|---|-----------|---------|
| `obs` | `tool-use` | Observed via a tool |
| `obs` | `intuition` | Direct zero-shot observation |
| `inf` | `cot` | Inferred via chain of reasoning |
| `inf` | `tot` | Inferred via tree-of-thought exploration |
| `rev` | `debate` | Evaluated through multi-perspective debate |
| `inf` | `reflection` | Inferred, then verified through self-correction |

**Normalization rule:** `R = R_raw / R_scale`, where `R_scale` is the maximum reasoning effort the model is capable of. For continuous scales (0.0–1.0), `R = R_raw` and `R_scale = 1`.

**Comparison rule:** When two messages both carry `R`, compare by `R` directly. If only one carries `R`, the value is treated as unknown (no inference drawn).

**Examples:**

| Model | R | R_raw | R_scale | R_label | Meaning |
|-------|---|-------|---------|---------|---------|
| GPT-5.6 | 1.0 | 6 | 6 | ultra | Maximum effort |
| GPT-5.6 | 0.5 | 3 | 6 | high | Half of maximum |
| 3-level model | 1.0 | 3 | 3 | max | Maximum for this model |
| 3-level model | 0.67 | 2 | 3 | medium | Two-thirds of maximum |
| Continuous model | 0.7 | 0.7 | 1 | — | 70% of maximum |

### provenance_key — Cryptographic Identity (optional)

A field pointing to the signer's public key or wallet address, making the semantic annotation independently verifiable without a separate trust registry.

| Format | Example |
|--------|---------|
| ETH address | `0xABC...123` |
| SOL address | `ABC...123` |
| BTC address | `bc1q...` |
| PGP key ID | `0xDEADBEEF` |
| `/llms.txt` URL | `https://agent.example/llms.txt` |

When present, `provenance_key` allows any recipient to:
1. Verify that the LAR-1 annotation was signed by the claimed agent
2. Independently confirm the agent's identity without a central registry
3. Build trust graphs based on signed interaction history

This field is designed to complement existing decentralized identity layers (e.g. wallet-based agent networks). LAR-1 does not reinvent identity — it rides on top of existing signed descriptors.

---

## 3. Wire Formats

### 3.1 JSON (recommended for A2A)

```json
{
  "LAR-1": {
    "T": "now",
    "S": "here",
    "C": "inf",
    "E": "derived",
    "L": 0.78,
    "V": "unverified",
    "R": 0.83,
    "R_raw": 5,
    "R_scale": 6,
    "R_label": "high",
    "provenance_key": "0xABC...123"
  }
}
```

Content-Type: `application/lar+json`

### 3.2 Compact string

```
LAR:T=now,S=here,C=inf,E=derived,L=0.78,V=unverified,R=0.83,R_raw=5,R_scale=6,R_label=high,PK=0xABC123
```

**Grammar (v0.4):**

```
compact  ::= "LAR:" pair ( "," pair )*
pair     ::= KEY "=" VALUE
KEY      ::= "T" | "S" | "C" | "E" | "L" | "V" | "R" | "R_raw" | "R_scale" | "R_label" | "R_strategy" | "PK"
VALUE    ::= enum-literal | number | string
```

Rules:

- Prefix `LAR:` is required (case-sensitive).
- Pairs may appear in any order.
- Duplicate keys **must be rejected** by parsers.
- At least one pair is required.
- Canonical serialization order (recommended): `T`, `S`, `C`, `E`, `L`, `V`, `R`, `R_raw`, `R_scale`, `R_label`, `R_strategy`, `PK`.
- `PK` (provenance_key) is optional; when present, it SHOULD be the last field.

### 3.3 MCP `_meta` profile

Attach LAR-1 fields under `_meta["lar-1"]` on resources, tools, prompts, and tool results:

```json
{
  "_meta": {
    "lar-1": {
      "T": "now",
      "C": "obs",
      "L": 0.9,
      "V": "verified_tool",
      "R": 0.5,
      "R_label": "medium"
    }
  }
}
```

Extension URI: `https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.4.json`

---

## 4. Integration with A2A

### Typed message part

```
Content-Type: application/lar+json
```

Include extension URI in `Message.extensions`:

```json
{
  "extensions": ["https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.4.json"],
  "parts": [
    {
      "kind": "data",
      "data": {
        "LAR-1": {
          "T": "now",
          "C": "obs",
          "L": 0.85,
          "V": "verified_tool",
          "R": 0.83,
          "R_label": "high"
        }
      }
    }
  ]
}
```

### Agent card capability

```json
{
  "capabilities": {
    "LAR-1": {
      "version": "0.4",
      "extension": "https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.4.json",
      "fields": ["T", "S", "C", "E", "L", "V", "R"],
      "provenance": true
    }
  }
}
```

---

## 5. Integration with LangGraph / LangChain

Convention: store overlay in `additional_kwargs["lar-1"]`:

```python
AIMessage(
  content="...",
  additional_kwargs={
    "lar-1": {"C": "obs", "L": 0.85, "V": "verified_tool", "R": 0.5}
  },
)
```

See [`demos/langgraph-synthesis/`](demos/langgraph-synthesis/) for a working example.

---

## 6. Integration with Wallet-Based Identity Systems

LAR-1 is designed to complement existing decentralized identity layers:

- **Wallet-based agent networks** (e.g. SunfishLoop): wallet address as `provenance_key` + signed capability descriptors (`/llms.txt`) + on-chain tipping reputation → feeds into `V:verified_peer`
- **On-chain tips as verification**: when peer agents tip an agent for useful output, this becomes machine-validated `V:verified_peer` — harder to game than self-reported `L` alone
- **No central registry needed**: `provenance_key` + signature allows independent verification by any recipient without a trusted third party

### Example: LAR-1 over a wallet-signed agent message

```json
{
  "LAR-1": {
    "T": "now",
    "S": "here",
    "C": "obs",
    "E": "direct",
    "L": 0.92,
    "V": "verified_peer",
    "R": 1.0,
    "R_label": "ultra",
    "provenance_key": "0xSunfishLoopAgent7F3A"
  }
}
```

## 7. Design Principles

1. **Overlay, not replacement** — enriches existing protocols without modifying them
2. **Optional** — messages without LAR-1 continue to work normally
3. **Progressive** — agents may send one field or all seven
4. **Machine-readable** — enums and numeric `L`, `R`; validated by JSON Schema
5. **Human-readable** — compact `LAR:` format for inline use
6. **Verifiable** — `V` makes confidence claims accountable
7. **Cross-model comparable** — `R` normalized to 0.0–1.0, enabling comparison across heterogeneous models

---

## 8. Conformance

Implementations **should** pass all fixtures in [`SPEC/conformance/`](SPEC/conformance/).

Reference SDK: [`@lar-1/core`](packages/lar1-core/) (TypeScript, 74+ tests).

Round-trip requirements:

- `parse(compact)` → `compact()` → `parse()` → identical object
- `parse(compact)` → `serialize()` → `deserialize()` → identical object

---

## 8. Governance

See **[GOVERNANCE.md](GOVERNANCE.md)** for versioning, change process, and deprecation policy.

---

## 9. Status

**Stable draft v0.4** — normative schema and conformance suite published.  
Open for community feedback and implementation experiments.

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-06-22 | Initial discussion draft |
| 0.2 | 2026-06-29 | Normative JSON Schema; enum refinement; field `V`; conformance suite; reference SDK |
| 0.3 | 2026-07-09 | A2A integration; provenance_key; compact format grammar |
| 0.4 | 2026-07-20 | Field `R` (Reasoning Effort) with normalization; cross-model comparison |

### v0.3 → v0.4 changes

| Area | v0.3 | v0.4 |
|------|------|------|
| Dimensions | Six | Seven (added `R`) |
| Compact keys | `T`, `S`, `C`, `E`, `L`, `V`, `PK` | Added `R`, `R_raw`, `R_scale`, `R_label` |
| Schema | Six fields | Seven fields |
| Extension URI | `extension-v0.3.json` | `extension-v0.4.json` |