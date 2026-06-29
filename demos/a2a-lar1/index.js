import {
  agentCardLar1Capability,
  createLar1Part,
  extractLar1,
  withLar1Extension,
  LAR1_EXTENSION_URI,
  LAR1_MEDIA_TYPE,
} from "@lar-1/a2a";

const fields = {
  T: "now",
  S: "here",
  C: "obs",
  E: "direct",
  L: 0.92,
  V: "verified_tool",
};

const part = createLar1Part(fields);

const message = withLar1Extension({
  role: "agent",
  parts: [
    { kind: "text", text: "Database latency is 42ms (p95)." },
    part,
  ],
});

console.log("=== LAR-1 A2A integration demo ===\n");
console.log("Extension URI:", LAR1_EXTENSION_URI);
console.log("Media type:", LAR1_MEDIA_TYPE);
console.log("\nAgent card capability:");
console.log(JSON.stringify(agentCardLar1Capability(), null, 2));
console.log("\nMessage with LAR-1 part:");
console.log(JSON.stringify(message, null, 2));
console.log("\nExtracted LAR-1:");
console.log(JSON.stringify(extractLar1(message), null, 2));
