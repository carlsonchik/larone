# LAR-1 Governance

How the LAR-1 specification evolves, versions, and accepts contributions.

---

## Principles

1. **Spec first** — normative behavior lives in `SPEC/lar1-schema.json` and `SPEC.md`; code follows spec.
2. **Testable changes** — every normative change adds or updates conformance fixtures.
3. **Overlay discipline** — LAR-1 must not require changes to A2A, MCP, or other transports.
4. **Backward awareness** — breaking enum or field changes require a major version bump.

---

## Versioning

LAR-1 uses **semantic versioning** on the specification:

| Bump | When |
|------|------|
| **MAJOR** | Breaking wire-format or enum changes; removed fields |
| **MINOR** | New optional fields; new enum values; new integration profiles |
| **PATCH** | Clarifications, fixture additions, documentation fixes |

Current version: **0.2**

### Artifact versioning

| Artifact | Version identifier |
|----------|-------------------|
| JSON Schema | [`SPEC/lar1-schema.json`](SPEC/lar1-schema.json) · [raw URL](https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/lar1-schema.json) |
| A2A extension | [raw URL](https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.2.json) |
| Media type | `application/lar+json` (version in payload optional) |
| Reference SDK | `@lar-1/core` package version tracks spec (currently `0.2.x`) |

---

## Change process

### 1. Proposal

Open a **GitHub Discussion** or **Issue** with:

- Problem statement
- Proposed field/enum/wire change
- Backward compatibility impact
- Example fixtures

### 2. Draft

- Update `SPEC/lar1-schema.json`
- Update `SPEC.md`
- Add conformance fixtures under `SPEC/conformance/`
- Update `packages/lar1-core` reference implementation
- Ensure `npm test` passes

### 3. Review

- At least one maintainer reviews schema diff and fixtures
- Breaking changes require explicit migration notes in `SPEC.md` § Version History

### 4. Release

- Tag: `v0.x.0`
- Update `ROADMAP.md` status
- Publish SDK if applicable

---

## Extension URI registry

| Version | URI | Descriptor |
|---------|-----|------------|
| 0.2 | [extension raw URL](https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.2.json) | [`SPEC/extension-v0.2.json`](SPEC/extension-v0.2.json) |

When registering with **A2A**, include the extension URI in `Message.extensions` and declare capability in the agent card (see [SPEC.md](SPEC.md) §4).

---

## Conformance

An implementation is **LAR-1 v0.2 compatible** if it:

1. Parses all `SPEC/conformance/valid/` and `SPEC/conformance/enum/` fixtures
2. Rejects all `SPEC/conformance/invalid/` fixtures with documented error codes
3. Passes round-trip: compact ↔ JSON

Reference implementation: [`packages/lar1-core/`](packages/lar1-core/).

Independent implementations are encouraged; report compatibility via Issues.

---

## Deprecation

1. Mark field/enum as `deprecated` in schema `description` for one MINOR release.
2. Remove in next MAJOR release.
3. Keep fixtures for deprecated values in `SPEC/conformance/deprecated/` until removal.

---

## Maintainers

Currently maintained by the repository owner.  
Contributions via Pull Request are welcome.

---

## Related documents

- [SPEC.md](SPEC.md) — normative specification
- [ROADMAP.md](ROADMAP.md) — planned phases
- [ALTERNATIVES.md](ALTERNATIVES.md) — positioning vs other standards
