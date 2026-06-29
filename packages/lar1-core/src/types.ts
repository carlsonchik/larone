/** LAR-1 field enums (v0.2) */

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

/** Inner LAR-1 object (semantic fields only) */
export interface Lar1Fields {
  T?: TemporalFrame;
  S?: SpatialFrame;
  C?: CognitionStance;
  E?: EvidenceGrounding;
  L?: number;
  V?: VerificationStatus;
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
} as const;

export type Lar1Key = keyof typeof ENUMS | "L";
