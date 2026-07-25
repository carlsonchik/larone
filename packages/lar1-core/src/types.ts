/** LAR-1 field enums (v0.4 — includes R-register) */

export type TemporalFrame = "now" | "past" | "recall" | "future";
export type SpatialFrame = "here" | "there" | "meta";
export type CognitionStance =
  | "obs"
  | "hyp"
  | "mem"
  | "det"
  | "inf"
  | "rev";
export type EvidenceGrounding =
  | "direct"
  | "derived"
  | "aggregated"
  | "reported";
export type VerificationStatus =
  | "unverified"
  | "verified_human"
  | "verified_tool"
  | "verified_crossref";

// --- R-Register (Harness Control Primitives) ---

export type RRegisterRouting = "passive" | "moderate" | "aggressive" | "contextual";
export type RRegisterTool = "passthrough" | "structured" | "validated";
export type RRegisterScale = "single" | "chain" | "parallel" | "graph" | "adaptive";
export type RRegisterMemory = "none" | "ephemeral" | "persistent" | "semantic" | "relational";
export type RRegisterStrategy = "deterministic" | "temperature" | "top_p" | "beam" | "adaptive";
export type RRegisterPlausibility = "none" | "confidence" | "consistency" | "crossref";

/** Inner LAR-1 object (semantic fields + R-register) */
export interface Lar1Fields {
  // Semantic overlay
  T?: TemporalFrame;
  S?: SpatialFrame;
  C?: CognitionStance;
  E?: EvidenceGrounding;
  L?: number;
  V?: VerificationStatus;

  // R-Register (harness control)
  R?: RRegisterRouting;
  R_raw?: RRegisterTool;
  R_scale?: RRegisterScale;
  R_label?: RRegisterMemory;
  R_strategy?: RRegisterStrategy;
  R_plausibility?: RRegisterPlausibility;
}

/** application/lar+json envelope */
export interface Lar1Envelope {
  "LAR-1": Lar1Fields;
}

export type Lar1Data = Lar1Fields;

export type Lar1ErrorCode =
  | "EMPTY_INPUT"
  | "MISSING_PREFIX"
  | "NO_PAIRS"
  | "UNKNOWN_KEY"
  | "INVALID_ENUM"
  | "INVALID_LIKELIHOOD"
  | "DUPLICATE_KEY"
  | "MALFORMED_PAIR"
  | "EMPTY_OBJECT";

export class Lar1ParseError extends Error {
  constructor(
    public readonly code: Lar1ErrorCode,
    message?: string
  ) {
    super(message ?? code);
    this.name = "Lar1ParseError";
  }
}

export const ENUMS = {
  T: ["now", "past", "recall", "future"] as const,
  S: ["here", "there", "meta"] as const,
  C: ["obs", "hyp", "mem", "det", "inf", "rev"] as const,
  E: ["direct", "derived", "aggregated", "reported"] as const,
  V: [
    "unverified",
    "verified_human",
    "verified_tool",
    "verified_crossref",
  ] as const,
  R: ["passive", "moderate", "aggressive", "contextual"] as const,
  R_raw: ["passthrough", "structured", "validated"] as const,
  R_scale: ["single", "chain", "parallel", "graph", "adaptive"] as const,
  R_label: ["none", "ephemeral", "persistent", "semantic", "relational"] as const,
  R_strategy: ["deterministic", "temperature", "top_p", "beam", "adaptive"] as const,
  R_plausibility: ["none", "confidence", "consistency", "crossref"] as const,
} as const;

export type Lar1Key = keyof typeof ENUMS | "L";