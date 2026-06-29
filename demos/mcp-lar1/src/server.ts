import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { attachLar1Meta, defaultObservedResult } from "@lar-1/mcp";

const server = new McpServer({
  name: "lar1-demo",
  version: "0.4.0",
});

server.tool(
  "ping",
  "Health check — read-only observation (LAR-1: C=obs, V=verified_tool)",
  async () =>
    attachLar1Meta(
      {
        content: [{ type: "text" as const, text: "pong" }],
      },
      defaultObservedResult(1)
    )
);

server.tool(
  "estimate",
  "Capacity estimate — unverified inference (LAR-1: C=inf, V=unverified)",
  async () =>
    attachLar1Meta(
      {
        content: [{ type: "text" as const, text: "~1200 RPS at current load" }],
      },
      {
        T: "now",
        C: "inf",
        E: "derived",
        L: 0.55,
        V: "unverified",
      }
    )
);

const transport = new StdioServerTransport();
await server.connect(transport);
