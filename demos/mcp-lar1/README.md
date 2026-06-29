# MCP + LAR-1 reference server

MCP server that attaches LAR-1 `_meta` to tool definitions and results.

```bash
cd demos/mcp-lar1
npm install
npm start
```

Add to Cursor MCP config:

```json
{
  "mcpServers": {
    "lar1-demo": {
      "command": "node",
      "args": ["/absolute/path/to/larone/demos/mcp-lar1/dist/server.js"]
    }
  }
}
```

## Tools

| Tool | LAR-1 on result |
|------|-----------------|
| `ping` | `C=obs`, `V=verified_tool` |
| `estimate` | `C=inf`, `V=unverified` |
