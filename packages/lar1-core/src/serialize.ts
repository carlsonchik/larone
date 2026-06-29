import { Lar1Data, Lar1Envelope } from "./types.js";

const FIELD_ORDER: (keyof Lar1Data)[] = ["T", "S", "C", "E", "L", "V"];

/** Serialize inner fields to application/lar+json JSON string */
export function serialize(data: Lar1Data): string {
  const envelope: Lar1Envelope = { "LAR-1": data };
  return JSON.stringify(envelope);
}

/** Serialize envelope object to JSON string */
export function serializeEnvelope(envelope: Lar1Envelope): string {
  return JSON.stringify(envelope);
}

/** Serialize inner fields to LAR-1 compact string */
export function compact(data: Lar1Data): string {
  const parts: string[] = [];

  for (const key of FIELD_ORDER) {
    const value = data[key];
    if (value === undefined) continue;
    parts.push(`${key}=${value}`);
  }

  if (parts.length === 0) {
    throw new Error("Cannot compact empty LAR-1 object");
  }

  return `${"LAR:"}${parts.join(",")}`;
}
