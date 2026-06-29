# @lar-1/mcp

LAR-1 integration for [Model Context Protocol](https://modelcontextprotocol.io/) via `_meta["lar-1"]`.

```ts
import { attachLar1Meta, withLar1Result, annotateToolDefinition } from "@lar-1/mcp";

server.tool(
  "ping",
  annotateToolDefinition({ description: "..." }, { C: "obs", L: 1, V: "verified_tool" }),
  withLar1Result(async () => ({ content: [...] }), { C: "obs", L: 1, V: "verified_tool" })
);
```

See [demos/mcp-lar1](../../demos/mcp-lar1/).
