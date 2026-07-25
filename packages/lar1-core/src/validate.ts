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

/** Validate inner LAR-1 fields against v0.4 schema rules (includes R-register) */
export function validate(data: Lar1Data): boolean {
  if (data === null || typeof data !== "object") {
    return false;
  }

  const keys = Object.keys(data);
  if (keys.length === 0) {
    return false;
  }

  const enumKeys: (keyof typeof ENUMS)[] = [
    "T", "S", "C", "E", "V",
    "R", "R_raw", "R_scale", "R_label", "R_strategy", "R_plausibility",
  ];

  for (const key of keys) {
    switch (key) {
      // Semantic overlay
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
      // R-Register
      case "R":
        if (!hasEnumValue("R", data.R)) return false;
        break;
      case "R_raw":
        if (!hasEnumValue("R_raw", data.R_raw)) return false;
        break;
      case "R_scale":
        if (!hasEnumValue("R_scale", data.R_scale)) return false;
        break;
      case "R_label":
        if (!hasEnumValue("R_label", data.R_label)) return false;
        break;
      case "R_strategy":
        if (!hasEnumValue("R_strategy", data.R_strategy)) return false;
        break;
      case "R_plausibility":
        if (!hasEnumValue("R_plausibility", data.R_plausibility)) return false;
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