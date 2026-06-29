import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import {
  compact,
  deserializeFields,
  parse,
  serialize,
} from "../index.js";
import { ENUMS } from "../types.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFORMANCE_ROOT = join(__dirname, "../../../../SPEC/conformance");

interface Fixture {
  id: string;
  input: string;
  expected?: { "LAR-1": Record<string, unknown> };
}

function loadFixtures(subdir: string): Fixture[] {
  const dir = join(CONFORMANCE_ROOT, subdir);
  return readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .map((f) => JSON.parse(readFileSync(join(dir, f), "utf8")) as Fixture);
}

function assertRoundTripCompact(input: string): void {
  const first = parse(input);
  const second = parse(compact(first));
  assert.deepEqual(second, first);
}

function assertRoundTripJson(input: string): void {
  const first = parse(input);
  const second = deserializeFields(serialize(first));
  assert.deepEqual(second, first);
}

function assertFullRoundTrip(input: string): void {
  const fromCompact = parse(input);
  const viaJson = deserializeFields(serialize(fromCompact));
  assert.deepEqual(viaJson, fromCompact);

  const recompact = compact(fromCompact);
  const fromRecompact = parse(recompact);
  assert.deepEqual(fromRecompact, fromCompact);

  const viaJsonAgain = deserializeFields(serialize(fromRecompact));
  assert.deepEqual(viaJsonAgain, fromRecompact);
}

test("compact round-trip: programmatic enum coverage", () => {
  for (const [key, values] of Object.entries(ENUMS)) {
    for (const value of values) {
      assertRoundTripCompact(`LAR:${key}=${value}`);
    }
  }
  for (const l of [0, 0.5, 1]) {
    assertRoundTripCompact(`LAR:L=${l}`);
  }
});

test("json round-trip: programmatic enum coverage", () => {
  for (const [key, values] of Object.entries(ENUMS)) {
    for (const value of values) {
      assertRoundTripJson(`LAR:${key}=${value}`);
    }
  }
  for (const l of [0, 0.5, 1]) {
    assertRoundTripJson(`LAR:L=${l}`);
  }
});

test("full round-trip: compact → json → compact", () => {
  const samples = [
    "LAR:T=now,S=here,C=obs,E=direct,L=0.95,V=verified_tool",
    "LAR:C=inf,L=0.72,V=unverified",
    "LAR:T=recall,S=there,C=mem,E=reported,L=0.55,V=verified_crossref",
  ];
  for (const input of samples) {
    assertFullRoundTrip(input);
  }
});

for (const subdir of ["valid", "enum", "boundary"]) {
  for (const fixture of loadFixtures(subdir)) {
    if (!fixture.expected) continue;
    test(`round-trip/${subdir}/${fixture.id}`, () => {
      assertRoundTripCompact(fixture.input);
      assertRoundTripJson(fixture.input);
      assertFullRoundTrip(fixture.input);
    });
  }
}
