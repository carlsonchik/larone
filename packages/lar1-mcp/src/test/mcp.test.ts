import assert from "node:assert/strict";
import { test } from "node:test";
import {
  attachLar1Meta,
  readLar1Meta,
  withLar1Result,
} from "../index.js";

test("attach and read _meta lar-1", () => {
  const result = attachLar1Meta(
    { content: [{ type: "text", text: "ok" }] },
    { C: "obs", L: 0.9, V: "verified_tool" }
  );
  const read = readLar1Meta(result);
  assert.deepEqual(read, { C: "obs", L: 0.9, V: "verified_tool" });
});

test("withLar1Result middleware", async () => {
  const handler = withLar1Result(
    async () => ({ content: [{ type: "text", text: "ok" }] }),
    { C: "obs", L: 1, V: "verified_tool" }
  );
  const result = await handler({});
  assert.equal(readLar1Meta(result)?.C, "obs");
});
