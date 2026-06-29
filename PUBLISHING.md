# Publishing LAR-1 packages

## npm (`@lar-1/*`)

Published packages:

| Package | Install |
|---------|---------|
| `@lar-1/core` | `npm install @lar-1/core` |
| `@lar-1/cli` | `npm install -g @lar-1/cli` |
| `@lar-1/a2a` | `npm install @lar-1/a2a` |
| `@lar-1/mcp` | `npm install @lar-1/mcp` |

### Prerequisites

1. [npm](https://www.npmjs.com/) account
2. Create `@lar-1` organization on npmjs.com
3. `npm login` or `NPM_TOKEN` with publish rights

### Publish order

`core` must be published before dependents (`cli`, `a2a`, `mcp`).

```bash
# 1. Core
cd packages/lar1-core
npm install && npm run build && npm test
npm publish --access public

# 2. CLI
cd ../lar1-cli
npm install && npm run build
npm publish --access public

# 3. A2A
cd ../lar1-a2a
npm install && npm run build && npm test
npm publish --access public

# 4. MCP
cd ../lar1-mcp
npm install && npm run build && npm test
npm publish --access public
```

### Local dev (monorepo, without publish)

```bash
cd packages/lar1-core && npm install && npm run build
cd ../lar1-cli && npm install file:../lar1-core && npm run build
node dist/cli.js validate "LAR:C=obs,L=0.9"
```

For local work you can temporarily set `"@lar-1/core": "file:../lar1-core"` in dependent `package.json` files.

---

## PyPI (`lar1semantic`)

The Python package is published as **`lar1semantic`** (import name remains `lar1`).

```bash
pip install lar1semantic
```

### Build and upload

```bash
cd packages/lar1-python
pip install build twine
python -m build
twine upload dist/*
```

### Local install test

```bash
cd packages/lar1-python
pip install -e ".[dev]"
pytest -q
lar1 validate "LAR:C=obs,L=0.9"
```

---

## Release checklist

1. Bump versions in `package.json` / `pyproject.toml`
2. Run full CI locally
3. Publish npm (`core` → `cli` → `a2a` → `mcp`) then PyPI if needed
4. Tag `git tag v0.3.x` and create GitHub Release
