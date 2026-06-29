import type { Lar1Data, Lar1Envelope } from "@lar-1/core";
import { validate, validateEnvelope } from "@lar-1/core";
import {
  A2ADataPart,
  A2AMessageLike,
  LAR1_CAPABILITY_KEY,
  LAR1_EXTENSION_URI,
  LAR1_MEDIA_TYPE,
} from "./types.js";

const FIELD_NAMES = ["T", "S", "C", "E", "L", "V"] as const;

/** Build an A2A typed data part carrying LAR-1 overlay */
export function createLar1Part(fields: Lar1Data): A2ADataPart {
  if (!validate(fields)) {
    throw new Error("Invalid LAR-1 fields");
  }
  return {
    kind: "data",
    mimeType: LAR1_MEDIA_TYPE,
    data: { "LAR-1": fields },
  };
}

/** Extract LAR-1 from message parts (first matching application/lar+json part) */
export function extractLar1FromParts(
  parts: A2AMessageLike["parts"]
): Lar1Data | null {
  if (!parts) return null;

  for (const part of parts) {
    if (part.mimeType !== LAR1_MEDIA_TYPE) continue;

    const envelope = part.data as Lar1Envelope;
    if (validateEnvelope(envelope)) {
      return envelope["LAR-1"];
    }
  }

  return null;
}

/** Extract LAR-1 from message metadata.lar-1 shorthand */
export function extractLar1FromMetadata(
  metadata: Record<string, unknown> | undefined
): Lar1Data | null {
  if (!metadata) return null;
  const block = metadata["lar-1"] ?? metadata[LAR1_CAPABILITY_KEY];
  if (block && validate(block as Lar1Data)) {
    return block as Lar1Data;
  }
  return null;
}

/** Extract from parts first, then metadata */
export function extractLar1(message: A2AMessageLike): Lar1Data | null {
  return (
    extractLar1FromParts(message.parts) ??
    extractLar1FromMetadata(message.metadata)
  );
}

/** Ensure Message.extensions includes the LAR-1 extension URI */
export function withLar1Extension<T extends { extensions?: string[] }>(
  message: T
): T {
  const extensions = message.extensions ?? [];
  if (extensions.includes(LAR1_EXTENSION_URI)) {
    return message;
  }
  return { ...message, extensions: [...extensions, LAR1_EXTENSION_URI] };
}

/** Agent card capability block for LAR-1 v0.2 */
export function agentCardLar1Capability(version = "0.2") {
  return {
    [LAR1_CAPABILITY_KEY]: {
      version,
      extension: LAR1_EXTENSION_URI,
      fields: [...FIELD_NAMES],
    },
  };
}

/** Attach LAR-1 as metadata shorthand on SendMessageRequest-style objects */
export function attachLar1Metadata<T extends { metadata?: Record<string, unknown> }>(
  request: T,
  fields: Lar1Data
): T {
  if (!validate(fields)) {
    throw new Error("Invalid LAR-1 fields");
  }
  return {
    ...request,
    metadata: { ...request.metadata, "lar-1": fields },
  };
}

export {
  LAR1_CAPABILITY_KEY,
  LAR1_EXTENSION_URI,
  LAR1_MEDIA_TYPE,
} from "./types.js";
export type { A2ADataPart, A2AAgentCardCapabilities, A2AMessageLike } from "./types.js";
