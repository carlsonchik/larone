# LAR-1 URI Hosting

## Was `lar-1.dev` real?

**No** — it was a **namespace placeholder**, a common pattern in protocol specs (like `https://example.com` in RFCs).  
Extension URIs in A2A are **identifiers**; they do not have to resolve to a live website.

For a better developer experience, this repo now uses **GitHub-hosted URLs** that resolve to real JSON files.

## Canonical URIs (v0.2)

| Purpose | URI |
|---------|-----|
| **A2A extension** | `https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.2.json` |
| **JSON Schema** | `https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/lar1-schema.json` |
| **Human docs** | https://github.com/carlsonchik/larone |

After tagging releases, pin to a version:

```
https://raw.githubusercontent.com/carlsonchik/larone/v0.2.0/SPEC/lar1-schema.json
```

## Free hosting options

| Option | Cost | Best for |
|--------|------|----------|
| **raw.githubusercontent.com** | Free | Schema & extension JSON (current choice) |
| **GitHub Pages** | Free | Landing page, docs site (`carlsonchik.github.io/larone`) |
| **jsDelivr / unpkg** | Free | CDN mirror after npm publish |
| **Read the Docs** | Free | Long-form documentation |
| **Custom `.dev` domain** | ~$12+/year | Branding (`lar-1.dev`) — optional later |

### GitHub Pages (optional upgrade)

1. Repo → Settings → Pages → Source: `main` / `/docs` or root
2. Add `docs/index.html` or use Jekyll
3. Extension URI becomes: `https://carlsonchik.github.io/larone/ext/v0.2.json`

No domain purchase required.

## Recommendation

1. **Now:** GitHub raw URLs (already wired in spec)
2. **After npm publish:** schema also at `https://unpkg.com/@lar-1/core@0.2.0/schema.json` (optional)
3. **Later:** buy `lar-1.dev` only if you want a short public brand
