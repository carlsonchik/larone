# LAR-1 Conformance Fixtures

Machine-readable test vectors for compact-string parsing and JSON validation.

## Layout

| Directory   | Purpose                                      |
|-------------|----------------------------------------------|
| `valid/`    | Compact string → expected `LAR-1` JSON       |
| `enum/`     | One fixture per allowed enum value (T,S,C,E,V) and L edge (0, 0.5, 1) |
| `invalid/`  | Compact string → expected error code/message |
| `boundary/` | Edge cases (limits, empty input, unknowns)   |

## Fixture format

Each file is JSON:

```json
{
  "id": "valid-01-full",
  "input": "LAR:T=now,S=here,C=obs,E=direct,L=0.95,V=verified_tool",
  "expected": {
    "LAR-1": {
      "T": "now",
      "S": "here",
      "C": "obs",
      "E": "direct",
      "L": 0.95,
      "V": "verified_tool"
    }
  }
}
```

Invalid/boundary fixtures use `error` instead of `expected`:

```json
{
  "id": "invalid-01-bad-prefix",
  "input": "T=now,C=obs",
  "error": "MISSING_PREFIX"
}
```

## Running (with lar1-core)

```bash
cd packages/lar1-core && npm test
```
