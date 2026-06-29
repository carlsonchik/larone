import { Lar1Data, Lar1Envelope } from "./types.js";
import { validate, validateEnvelope } from "./validate.js";

/** Parse application/lar+json string into envelope */
export function deserialize(json: string): Lar1Envelope {
  let parsed: unknown;
  try {
    parsed = JSON.parse(json);
  } catch {
    throw new Error("Invalid JSON");
  }

  if (!validateEnvelope(parsed as Lar1Envelope)) {
    throw new Error("Invalid LAR-1 envelope");
  }

  return parsed as Lar1Envelope;
}

/** Parse application/lar+json string into inner fields */
export function deserializeFields(json: string): Lar1Data {
  return deserialize(json)["LAR-1"];
}
