/** Minimal A2A shapes — no full SDK dependency */

import type { Lar1Data } from "@lar-1/core";

/** Canonical extension URI (resolves to JSON descriptor on GitHub) */
export const LAR1_EXTENSION_URI =
  "https://raw.githubusercontent.com/carlsonchik/larone/main/SPEC/extension-v0.2.json" as const;

export const LAR1_MEDIA_TYPE = "application/lar+json" as const;

export const LAR1_CAPABILITY_KEY = "LAR-1" as const;

export interface A2ADataPart {
  kind: "data";
  mimeType: typeof LAR1_MEDIA_TYPE;
  data: { "LAR-1": Lar1Data };
}

export interface A2AMessageLike {
  parts?: Array<{ kind?: string; mimeType?: string; data?: unknown; text?: string }>;
  extensions?: string[];
  metadata?: Record<string, unknown>;
}

export interface A2AAgentCardCapabilities {
  [LAR1_CAPABILITY_KEY]?: {
    version: string;
    extension: string;
    fields: string[];
  };
}
