# Cursor hooks — LAR-1 audit example

Project hooks that log LAR-1-compatible semantic hints on agent tool use.

## Install into a project

Copy to your repo root:

```bash
cp -r examples/cursor-hooks/.cursor /path/to/your/project/
```

Or symlink:

```bash
ln -s /path/to/larone/examples/cursor-hooks/.cursor .cursor
```

## What it does

| Hook | Event | Behavior |
|------|-------|----------|
| `lar1-audit.sh` | `postToolUse` | Logs tool name + suggests LAR-1 `C`/`E` tags to stderr |

This is an **audit-only** hook (fail-open). Extend to inject `lar-1` metadata into MCP payloads in `beforeMCPExecution`.

## Files

```
examples/cursor-hooks/
├── README.md
└── .cursor/
    ├── hooks.json
    └── hooks/
        └── lar1-audit.sh
```

See [Cursor hooks docs](https://cursor.com/docs/agent/hooks).
