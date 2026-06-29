# Publishing LAR-1 packages

## npm (`@lar-1/core`, `@lar-1/cli`, `@lar-1/a2a`, `@lar-1/mcp`)

### Prerequisites

1. [npm](https://www.npmjs.com/) account
2. Create `@lar-1` organization on npmjs.com
3. `npm login`

### Publish order (core first — others depend on it)

```bash
# 1. Core — foundation
cd packages/lar1-core
npm install && npm run build && npm test
npm publish --access public

# 2. CLI (depends on core)
cd ../lar1-cli
npm install && npm run build
npm publish --access public

# 3. A2A integration (depends on core)
cd ../lar1-a2a
npm install && npm run build && npm test
npm publish --access public

# 4. MCP integration (depends on core)
cd ../lar1-mcp
npm install && npm run build && npm test
npm publish --access public
```

### Local test (without publish)

Uses `file:` for local dev dependency on core:

```bash
cd packages/lar1-core && npm install && npm run build
cd ../lar1-cli && npm install file:../lar1-core && npm run build
node dist/cli.js validate "LAR:C=obs,L=0.9"
```

---

## PyPI (`lar1semantic`)

### Prerequisites

1. [PyPI](https://pypi.org/) account
2. `pip install build twine`

### Build and upload

```bash
cd packages/lar1-python
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

1. Bump versions in `package.json` / `pyproject.toml` / `__version__`
2. Update `ROADMAP.md` and tag `git tag v0.3.0`
3. Run full CI locally
4. Publish npm → PyPI
5. Create GitHub Release with notes
