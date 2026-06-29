import {
  ENUMS,
  Lar1Data,
  Lar1Envelope,
  Lar1Key,
  Lar1ParseError,
} from "./types.js";

const PREFIX = "LAR:";
const VALID_KEYS = new Set<string>(["T", "S", "C", "E", "L", "V"]);

function assertEnum<K extends keyof typeof ENUMS>(
  key: K,
  value: string
): (typeof ENUMS)[K][number] {
  const allowed = ENUMS[key] as readonly string[];
  if (!allowed.includes(value)) {
    throw new Lar1ParseError("INVALID_ENUM", `Invalid ${key}=${value}`);
  }
  return value as (typeof ENUMS)[K][number];
}

function parseLikelihood(raw: string): number {
  const n = Number(raw);
  if (raw === "" || Number.isNaN(n)) {
    throw new Lar1ParseError("INVALID_LIKELIHOOD", `Invalid L=${raw}`);
  }
  if (n < 0 || n > 1) {
    throw new Lar1ParseError("INVALID_LIKELIHOOD", `L out of range: ${n}`);
  }
  return n;
}

/**
 * Parse a LAR-1 compact string into inner fields (no envelope).
 * @example parse("LAR:T=now,C=obs,L=0.9")
 */
export function parse(compact: string): Lar1Data {
  const trimmed = compact.trim();
  if (trimmed === "") {
    throw new Lar1ParseError("EMPTY_INPUT");
  }
  if (!trimmed.startsWith(PREFIX)) {
    throw new Lar1ParseError("MISSING_PREFIX");
  }

  const body = trimmed.slice(PREFIX.length);
  if (body === "") {
    throw new Lar1ParseError("NO_PAIRS");
  }

  const pairs = body.split(",");
  if (pairs.length === 0 || (pairs.length === 1 && pairs[0] === "")) {
    throw new Lar1ParseError("NO_PAIRS");
  }

  const seen = new Set<string>();
  const data: Lar1Data = {};

  for (const pair of pairs) {
    const eq = pair.indexOf("=");
    if (eq === -1) {
      throw new Lar1ParseError("MALFORMED_PAIR", `Missing '=': ${pair}`);
    }

    const key = pair.slice(0, eq).trim();
    const value = pair.slice(eq + 1).trim();

    if (!VALID_KEYS.has(key)) {
      throw new Lar1ParseError("UNKNOWN_KEY", `Unknown key: ${key}`);
    }
    if (seen.has(key)) {
      throw new Lar1ParseError("DUPLICATE_KEY", `Duplicate key: ${key}`);
    }
    seen.add(key);

    switch (key as Lar1Key) {
      case "T":
        data.T = assertEnum("T", value);
        break;
      case "S":
        data.S = assertEnum("S", value);
        break;
      case "C":
        data.C = assertEnum("C", value);
        break;
      case "E":
        data.E = assertEnum("E", value);
        break;
      case "V":
        data.V = assertEnum("V", value);
        break;
      case "L":
        data.L = parseLikelihood(value);
        break;
    }
  }

  return data;
}

/** Parse compact string and wrap as application/lar+json envelope */
export function parseEnvelope(compact: string): Lar1Envelope {
  return { "LAR-1": parse(compact) };
}
