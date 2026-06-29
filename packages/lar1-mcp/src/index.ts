import type { Lar1Data } from "@lar-1/core";
import { validate } from "@lar-1/core";
import {
  LAR1_EXTENSION_URI,
  LAR1_META_KEY,
  McpMetaCarrier,
  McpToolResultLike,
  ToolHandler,
} from "./types.js";

/** Merge LAR-1 fields into `_meta["lar-1"]` */
export function attachLar1Meta<T extends McpToolResultLike>(
  target: T,
  fields: Lar1Data
): T {
  if (!validate(fields)) {
    throw new Error("Invalid LAR-1 fields");
  }
  const meta: Record<string, unknown> = { ...target._meta, [LAR1_META_KEY]: fields };
  if (!meta["lar-1.extension"]) {
    meta["lar-1.extension"] = LAR1_EXTENSION_URI;
  }
  return { ...target, _meta: meta };
}

/** Read LAR-1 from `_meta` */
export function readLar1Meta(
  target: (McpMetaCarrier & Partial<McpToolResultLike>) | undefined
): Lar1Data | null {
  if (!target?._meta) return null;
  const block = target._meta[LAR1_META_KEY];
  if (block && validate(block as Lar1Data)) {
    return block as Lar1Data;
  }
  return null;
}

/** Default LAR-1 tags for read-only tool results */
export function defaultObservedResult(likelihood = 0.85): Lar1Data {
  return {
    T: "now",
    S: "here",
    C: "obs",
    E: "direct",
    L: likelihood,
    V: "verified_tool",
  };
}

/** Wrap an MCP tool handler to attach LAR-1 metadata to results */
export function withLar1Result<TArgs>(
  handler: ToolHandler<TArgs, McpToolResultLike>,
  lar1: Lar1Data | ((args: TArgs, result: McpToolResultLike) => Lar1Data)
): ToolHandler<TArgs, McpToolResultLike> {
  return async (args: TArgs) => {
    const result = await handler(args);
    const fields =
      typeof lar1 === "function" ? lar1(args, result) : lar1;
    return attachLar1Meta(result, fields);
  };
}

/** Annotate a tool definition with LAR-1 hints in _meta */
export function annotateToolDefinition<T extends McpMetaCarrier>(
  tool: T,
  fields: Lar1Data
): T {
  if (!validate(fields)) {
    throw new Error("Invalid LAR-1 fields");
  }
  return {
    ...tool,
    _meta: {
      ...tool._meta,
      [LAR1_META_KEY]: fields,
      "lar-1.extension": LAR1_EXTENSION_URI,
    },
  };
}

export { LAR1_EXTENSION_URI, LAR1_META_KEY } from "./types.js";
export type { McpMetaCarrier, McpToolResultLike, ToolHandler } from "./types.js";
