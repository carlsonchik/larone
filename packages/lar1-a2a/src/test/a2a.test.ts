import assert from "node:assert/strict";
import { test } from "node:test";
import {
  agentCardLar1Capability,
  createLar1Part,
  extractLar1,
  withLar1Extension,
} from "../index.js";

test("createLar1Part and extractLar1 round-trip", () => {
  const fields = { T: "now" as const, C: "obs" as const, L: 0.9, V: "verified_tool" as const };
  const part = createLar1Part(fields);
  assert.equal(part.mimeType, "application/lar+json");
  const extracted = extractLar1({ parts: [part] });
  assert.deepEqual(extracted, fields);
});

test("withLar1Extension adds URI once", () => {
  const msg = withLar1Extension({ extensions: [] });
  assert.equal(msg.extensions?.length, 1);
  const again = withLar1Extension(msg);
  assert.equal(again.extensions?.length, 1);
});

test("agentCardLar1Capability", () => {
  const cap = agentCardLar1Capability();
  assert.equal(cap["LAR-1"].version, "0.2");
  assert.ok(cap["LAR-1"].fields.includes("V"));
});
