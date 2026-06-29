import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { compact, parse, validate } from "../index.js";
import { Lar1ParseError } from "../types.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFORMANCE_ROOT = join(__dirname, "../../../../SPEC/conformance");

interface Fixture {
  id: string;
  input: string;
  expected?: { "LAR-1": Record<string, unknown> };
  error?: string;
}

function loadFixtures(subdir: string): Fixture[] {
  const dir = join(CONFORMANCE_ROOT, subdir);
  return readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .map((f) => JSON.parse(readFileSync(join(dir, f), "utf8")) as Fixture);
}

for (const subdir of ["valid", "enum"]) {
  for (const fixture of loadFixtures(subdir)) {
    test(`${subdir}/${fixture.id}`, () => {
      const parsed = parse(fixture.input);
      assert.deepEqual({ "LAR-1": parsed }, fixture.expected);
      assert.equal(validate(parsed), true);
      assert.equal(compact(parsed), fixture.input);
    });
  }
}

for (const fixture of loadFixtures("invalid")) {
  test(`invalid/${fixture.id}`, () => {
    assert.throws(
      () => parse(fixture.input),
      (err: unknown) => {
        assert.ok(err instanceof Lar1ParseError);
        assert.equal(err.code, fixture.error);
        return true;
      }
    );
  });
}

for (const fixture of loadFixtures("boundary")) {
  if (fixture.expected) {
    test(`boundary/${fixture.id}`, () => {
      const parsed = parse(fixture.input);
      assert.deepEqual({ "LAR-1": parsed }, fixture.expected);
      assert.equal(validate(parsed), true);
    });
  } else if (fixture.error) {
    test(`boundary/${fixture.id}`, () => {
      assert.throws(
        () => parse(fixture.input),
        (err: unknown) => {
          assert.ok(err instanceof Lar1ParseError);
          assert.equal(err.code, fixture.error);
          return true;
        }
      );
    });
  }
}
