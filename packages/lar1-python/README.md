# lar1semantic — LAR-1 Python SDK

Reference Python implementation of **LAR-1** semantic overlay.

## Install

```bash
pip install lar1semantic
# or from monorepo:
cd packages/lar1-python && pip install -e ".[dev]"
```

## API

```python
from lar1 import parse, validate, compact, serialize, deserialize_fields

data = parse("LAR:T=now,C=obs,L=0.9,V=verified_tool")
validate(data)  # True
compact(data)   # canonical LAR: string
serialize(data)  # application/lar+json
```

## CLI

```bash
lar1 validate 'LAR:C=obs,L=0.9'
lar1 compact message.json
lar1 json 'LAR:T=now,C=inf,L=0.7'
```

## Tests

```bash
pytest
```

Runs the same 74+ conformance fixtures as `@lar-1/core`.

## License

MIT
