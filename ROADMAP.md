# LAR-1 Development Roadmap

> **Latent Agent Register** — semantic overlay for agent communication  
> Status: v0.2 (schema + reference SDK skeleton)

## Vision

LAR-1 is **not** a transport or orchestration protocol. It is a compact, machine-readable semantic layer that answers: *how is this message situated?* — before routing, synthesis, or audit.

```mermaid
flowchart LR
  subgraph transport [Transport]
    A2A[A2A]
    MCP[MCP]
  end
  subgraph lar1 [LAR-1 overlay]
    T[T] --> S[S] --> C[C] --> E[E] --> L[L] --> V[V]
  end
  A2A --> lar1
  MCP --> lar1
```

---

## Phase 0 — Stabilize specification (v0.2) ✅ in progress

**Goal:** Turn the discussion draft into a normative, testable spec.

| Deliverable | Status |
|-------------|--------|
| JSON Schema (`SPEC/lar1-schema.json`) | ✅ |
| Compact format grammar | ✅ |
| Conformance fixtures (`SPEC/conformance/`) | ✅ |
| Field `V` (verification) | ✅ |
| Extension URI `https://lar-1.dev/ext/v0.2` | 🔲 |
| Update root `SPEC.md` to v0.2 enums | 🔲 |
| Governance / versioning doc | 🔲 |

**Exit criteria:** Two independent implementations parse the same compact string to identical JSON.

---

## Phase 1 — Reference SDK (v0.3)

**Goal:** Minimal library — not a framework.

```
packages/
  lar1-core/     ✅ TypeScript — parse, validate, serialize, compact
  lar1-python/   🔲 Python mirror
```

| Deliverable | Status |
|-------------|--------|
| `@lar-1/core` TypeScript package | ✅ skeleton |
| Conformance test runner | ✅ |
| Publish to npm | 🔲 |
| CLI: `lar1 validate`, `lar1 compact` | 🔲 |
| Python package on PyPI | 🔲 |

**Exit criteria:** `npm install @lar-1/core` → annotate a message in ≤10 lines.

---

## Phase 2 — Integration profiles (v0.4)

**Goal:** Show exactly how LAR-1 attaches to real protocols.

### A2A

- Typed `Part` with `Content-Type: application/lar+json`
- Agent card capability block
- Extension registration in [a2aproject/A2A](https://github.com/a2aproject/A2A) discussions

### MCP

- `_meta` profile on tools, resources, prompts, tool results
- Reference middleware for MCP servers

### LangGraph / LangChain

- `additional_kwargs["lar-1"]` convention
- Middleware auto-tagging `C` and `E` by node type

| Deliverable | Status |
|-------------|--------|
| `lar1-a2a` adapter package | 🔲 |
| `lar1-mcp` adapter package | 🔲 |
| LangGraph demo | ✅ skeleton (`demos/langgraph-synthesis/`) |
| Cursor hooks example | 🔲 |

**Exit criteria:** Working demo in at least two ecosystems (LangGraph + MCP or A2A).

---

## Phase 3 — Prove value

**Goal:** Demonstrate that LAR-1 changes outcomes — not just metadata.

| Scenario | What it proves |
|----------|----------------|
| **Multi-agent synthesis** | Synthesizer weights by `L`, `C`, `V` → fewer bad merges |
| **Audit trail** | Filter `E=direct` before destructive tool calls |
| **Memory routing** | `T=recall` vs `T=now` → correct RAG context |

| Deliverable | Status |
|-------------|--------|
| LangGraph synthesis demo | ✅ skeleton |
| Noisy-`L` experiment (verification matters) | 🔲 |
| Blog post + reproducible repo | 🔲 |

**Exit criteria:** Published comparison showing measurable difference with vs without LAR-1.

---

## Phase 4 — Ecosystem & governance

**Goal:** Community adoption and stable evolution.

- RFC process (GitHub Discussions → SPEC PR)
- Conformance badge: "LAR-1 compatible v0.x"
- Stack documentation with sister protocol [`/3`](https://github.com/carlsonchik/third) (position/signal layer)
- awesome-mcp / awesome-a2a list PRs
- MCP Registry entry for reference server
- Optional: short arXiv note if experiments exist

---

## 30-day priorities

1. ✅ JSON Schema + conformance fixtures
2. ✅ `@lar-1/core` skeleton + tests
3. ✅ LangGraph demo skeleton
4. 🔲 Update `SPEC.md` to v0.2 field tables
5. 🔲 Python `lar1-core` package
6. 🔲 npm publish `@lar-1/core@0.2.0`

---

## Version history

| Version | Target | Focus |
|---------|--------|-------|
| 0.1 | 2026-06 | Initial discussion draft |
| 0.2 | 2026-06 | JSON Schema, V field, conformance |
| 0.3 | TBD | SDK stable, npm/PyPI |
| 0.4 | TBD | A2A/MCP/LangGraph profiles |

---

## Related

- [ALTERNATIVES.md](./ALTERNATIVES.md) — competitive landscape
- [SPEC/lar1-schema.json](./SPEC/lar1-schema.json) — normative schema
- Sister protocol: [/3 — Third Protocol](https://github.com/carlsonchik/third)
