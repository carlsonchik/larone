# LAR-1 — Specification v0.3 (Discussion Draft)

> **Latent Agent Register** — Semantic Overlay for Agent Communication

**Normative artifacts:**

| Artifact | Path |
|----------|------|
| JSON Schema | [`SPEC/lar1-schema.json`](SPEC/lar1-schema.json) |
| Conformance fixtures | [`SPEC/conformance/`](SPEC/conformance/) |
| Extension descriptor | [`SPEC/extension-v0.2.json`](SPEC/extension-v0.2.json) |
| Reference implementation | [`packages/lar1-core/`](packages/lar1-core/) |

**Extension URI (A2A `extensions[]`):** `https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.2.json`  
**Media type:** `application/lar+json`

---

## 1. Problem

Agent messages are routable before they are semantically legible.  
A task can be delegated and a tool called, yet downstream systems lack a compact representation of:

- Is this an observation or an inference?
- Is it grounded in current context or retrieved memory?
- Does it reflect ambiguity or a committed judgment?
- What is the confidence level — and has it been verified?

## 2. The Six Dimensions

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
    "provenance_key": "0xABC...123"
  }
}
```

Content-Type: `application/lar+json`

### 3.2 Compact string

```
LAR:T=now,S=here,C=inf,E=derived,L=0.78,V=unverified,PK=0xABC123
```

**Grammar (v0.3):**

```
compact  ::= "LAR:" pair ( "," pair )*
pair     ::= KEY "=" VALUE
KEY      ::= "T" | "S" | "C" | "E" | "L" | "V" | "PK"
VALUE    ::= enum-literal | number | string
```

Rules:

- Prefix `LAR:` is required (case-sensitive).
- Pairs may appear in any order.
- Duplicate keys **must be rejected** by parsers.
- At least one pair is required.
- Canonical serialization order (recommended): `T`, `S`, `C`, `E`, `L`, `V`, `PK`.
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
      "V": "verified_tool"
    }
  }
}
```

Extension URI: `https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.2.json`

---

## 4. Integration with A2A

### Typed message part

```
Content-Type: application/lar+json
```

Include extension URI in `Message.extensions`:

```json
{
  "extensions": ["https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.2.json"],
  "parts": [
    {
      "kind": "data",
      "data": {
        "LAR-1": {
          "T": "now",
          "C": "obs",
          "L": 0.85,
          "V": "verified_tool"
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
      "version": "0.3",
      "extension": "https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.3.json",
      "fields": ["T", "S", "C", "E", "L", "V"],
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
    "lar-1": {"C": "obs", "L": 0.85, "V": "verified_tool"}
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
    "provenance_key": "0xSunfishLoopAgent7F3A"
  }
}
```

## 7. Design Principles

1. **Overlay, not replacement** — enriches existing protocols without modifying them
2. **Optional** — messages without LAR-1 continue to work normally
3. **Progressive** — agents may send one field or all six
4. **Machine-readable** — enums and numeric `L`; validated by JSON Schema
5. **Human-readable** — compact `LAR:` format for inline use
6. **Verifiable** — `V` makes confidence claims accountable

---

## 8. Conformance

Implementations **should** pass all fixtures in [`SPEC/conformance/`](SPEC/conformance/).

Reference SDK: [`@lar-1/core`](packages/lar1-core/) (TypeScript, 74 tests).

Round-trip requirements:

- `parse(compact)` → `compact()` → `parse()` → identical object
- `parse(compact)` → `serialize()` → `deserialize()` → identical object

---

## 8. Governance

See **[GOVERNANCE.md](GOVERNANCE.md)** for versioning, change process, and deprecation policy.

---

## 9. Status

**Stable draft v0.2** — normative schema and conformance suite published.  
Open for community feedback and implementation experiments.

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-06-22 | Initial discussion draft |
| 0.2 | 2026-06-29 | Normative JSON Schema; enum refinement; field `V`; conformance suite; reference SDK |

### v0.1 → v0.2 breaking changes

| Area | v0.1 | v0.2 |
|------|------|------|
| `T` | `now`, `recall:<id>`, `spec:<range>`, … | `now`, `past`, `recall`, `future` |
| `S` | `workspace:<name>`, `channel:<id>`, … | `here`, `there`, `meta` |
| `C` | `obs`, `inf`, `dec`, `exp`, `meta`, `unc` | `obs`, `hyp`, `mem`, `det`, `inf`, `rev` |
| `E` | `direct:<source>`, `derived:<chain>`, … | `direct`, `derived`, `aggregated`, `reported` |
| `L` | float or `high`/`medium`/`low` | float `0.0`–`1.0` only |
| `V` | — | new field |
