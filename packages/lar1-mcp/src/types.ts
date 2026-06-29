import type { Lar1Data } from "@lar-1/core";
import { validate } from "@lar-1/core";

export const LAR1_META_KEY = "lar-1" as const;

export const LAR1_EXTENSION_URI =
  "https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.2.json" as const;

export interface McpMetaCarrier {
  _meta?: Record<string, unknown>;
}

export interface McpToolResultLike {
  content: Array<Record<string, unknown>>;
  structuredContent?: unknown;
  _meta?: Record<string, unknown>;
}

export type ToolHandler<TArgs = unknown, TResult = McpToolResultLike> = (
  args: TArgs
) => TResult | Promise<TResult>;
