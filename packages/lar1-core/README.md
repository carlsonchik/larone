# @lar-1/core

Reference TypeScript implementation of **LAR-1** (Latent Agent Register) v0.2.

Parse, validate, and serialize the semantic overlay for agent messages — compatible with `application/lar+json` and the compact `LAR:` wire format.

## Install

```bash
npm install @lar-1/core
# or from monorepo root:
cd packages/lar1-core && npm install && npm run build
```

## API

| Function | Description |
|----------|-------------|
| `parse(compact)` | Compact string → inner `Lar1Fields` |
| `validate(data)` | Returns `true` if fields match v0.2 schema |
| `serialize(data)` | Inner fields → `application/lar+json` string |
| `deserialize(json)` | JSON string → inner `Lar1Fields` |
| `compact(data)` | Inner fields → `LAR:...` compact string |

## Examples

### 1. Parse a compact string

```ts
import { parse } from "@lar-1/core";

const data = parse("LAR:T=now,S=here,C=obs,E=direct,L=0.95,V=verified_tool");
// { T: "now", S: "here", C: "obs", E: "direct", L: 0.95, V: "verified_tool" }
```

### 2. Validate before routing

```ts
import { validate } from "@lar-1/core";

const ok = validate({ C: "inf", L: 0.72, V: "unverified" }); // true
const bad = validate({ C: "guess", L: 0.5 }); // false
```

### 3. Serialize to JSON (A2A / MCP)

```ts
import { serialize } from "@lar-1/core";

const json = serialize({ T: "recall", C: "mem", L: 0.55 });
// '{"LAR-1":{"T":"recall","C":"mem","L":0.55}}'
```

### 4. Compact for inline use

```ts
import { compact } from "@lar-1/core";

compact({ C: "hyp", T: "future", L: 0.33, V: "unverified" });
// "LAR:T=future,C=hyp,L=0.33,V=unverified"
```

### 5. Round-trip (compact and JSON)

```ts
import { compact, deserializeFields, parse, serialize } from "@lar-1/core";

const input = "LAR:C=det,E=direct,L=0.99,V=verified_tool";
const data = parse(input);

// compact: parse → compact → parse
const roundCompact = parse(compact(data));
console.assert(JSON.stringify(roundCompact) === JSON.stringify(data));

// json: parse → serialize → deserialize → parse
const roundJson = deserializeFields(serialize(data));
console.assert(JSON.stringify(roundJson) === JSON.stringify(data));
```

## Conformance tests

```bash
npm test
```

Runs fixtures in `SPEC/conformance/` (valid, enum, invalid, boundary) plus round-trip tests.

## Spec

- JSON Schema: [`SPEC/lar1-schema.json`](../../SPEC/lar1-schema.json)
- Full spec: [`SPEC.md`](../../SPEC.md)

## License

MIT
