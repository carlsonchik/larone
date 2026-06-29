import { ENUMS, Lar1Data, Lar1Envelope } from "./types.js";

function isLikelihood(n: unknown): n is number {
  return typeof n === "number" && !Number.isNaN(n) && n >= 0 && n <= 1;
}

function hasEnumValue<K extends keyof typeof ENUMS>(
  key: K,
  value: unknown
): value is (typeof ENUMS)[K][number] {
  return (
    typeof value === "string" &&
    (ENUMS[key] as readonly string[]).includes(value)
  );
}

/** Validate inner LAR-1 fields against v0.2 schema rules */
export function validate(data: Lar1Data): boolean {
  if (data === null || typeof data !== "object") {
    return false;
  }

  const keys = Object.keys(data);
  if (keys.length === 0) {
    return false;
  }

  for (const key of keys) {
    switch (key) {
      case "T":
        if (!hasEnumValue("T", data.T)) return false;
        break;
      case "S":
        if (!hasEnumValue("S", data.S)) return false;
        break;
      case "C":
        if (!hasEnumValue("C", data.C)) return false;
        break;
      case "E":
        if (!hasEnumValue("E", data.E)) return false;
        break;
      case "V":
        if (!hasEnumValue("V", data.V)) return false;
        break;
      case "L":
        if (!isLikelihood(data.L)) return false;
        break;
      default:
        return false;
    }
  }

  return true;
}

/** Validate application/lar+json envelope */
export function validateEnvelope(envelope: Lar1Envelope): boolean {
  if (
    envelope === null ||
    typeof envelope !== "object" ||
    !("LAR-1" in envelope)
  ) {
    return false;
  }
  return validate(envelope["LAR-1"]);
}
