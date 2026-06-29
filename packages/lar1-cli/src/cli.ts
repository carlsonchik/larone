#!/usr/bin/env node
import { readFileSync } from "node:fs";
import {
  compact,
  deserializeFields,
  parse,
  serialize,
  validate,
} from "@lar-1/core";
import { Lar1ParseError } from "@lar-1/core";

function readInput(arg: string | undefined): string {
  if (!arg || arg === "-") {
    return readFileSync(0, "utf8").trim();
  }
  if (arg.startsWith("LAR:") || arg.startsWith("{")) {
    return arg.trim();
  }
  return readFileSync(arg, "utf8").trim();
}

function usage(): never {
  console.error(`Usage:
  lar1 validate [file|-]   Validate compact or JSON input
  lar1 compact [file|-]    Output canonical compact string
  lar1 json [file|-]       Convert compact to application/lar+json`);
  process.exit(2);
}

const [, , command, file] = process.argv;

if (!command) usage();

try {
  const raw = readInput(file);

  if (command === "validate") {
    const data = raw.startsWith("{")
      ? deserializeFields(raw)
      : parse(raw);
    if (!validate(data)) {
      console.error("INVALID");
      process.exit(1);
    }
    console.log("OK");
    process.exit(0);
  }

  if (command === "compact") {
    const data = raw.startsWith("{")
      ? deserializeFields(raw)
      : parse(raw);
    console.log(compact(data));
    process.exit(0);
  }

  if (command === "json") {
    const data = parse(raw);
    console.log(serialize(data));
    process.exit(0);
  }

  usage();
} catch (err) {
  if (err instanceof Lar1ParseError) {
    console.error(err.code);
  } else {
    console.error(err instanceof Error ? err.message : String(err));
  }
  process.exit(1);
}
