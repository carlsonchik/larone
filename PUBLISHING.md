# Publishing LAR-1 packages

## npm (`@lar-1/core`, `@lar-1/cli`)

### Prerequisites

1. [npm](https://www.npmjs.com/) account
2. Access to the `@lar-1` scope (create org on npm or publish as unscoped `lar1-core`)

### Publish `@lar-1/core`

```bash
cd packages/lar1-core
npm login
npm publish --access public
```

### Publish `@lar-1/cli`

```bash
cd packages/lar1-cli
# Ensure @lar-1/core is published first, or use file:../lar1-core for local test
npm install
npm publish --access public
```

### Local CLI test (without publish)

```bash
cd packages/lar1-core && npm install && npm run build
cd ../lar1-cli && npm install file:../lar1-core && npm run build
node dist/cli.js validate "LAR:C=obs,L=0.9"
```

---

## PyPI (`lar-1`)

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
