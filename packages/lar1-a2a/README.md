# @lar-1/a2a

LAR-1 integration profile for [Google A2A](https://a2a-protocol.org/).

```ts
import {
  createLar1Part,
  extractLar1,
  withLar1Extension,
  agentCardLar1Capability,
} from "@lar-1/a2a";

const message = withLar1Extension({
  parts: [
    { kind: "text", text: "..." },
    createLar1Part({ C: "obs", L: 0.9, V: "verified_tool" }),
  ],
});
```

See [demos/a2a-lar1](../../demos/a2a-lar1/) and [A2A issue #1974](https://github.com/a2aproject/A2A/issues/1974).
