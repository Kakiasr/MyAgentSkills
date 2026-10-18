#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

const validator = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:[A-Za-z]:)/, (m) => m.slice(1))), "validate_document_set.mjs");
const temp = fs.mkdtempSync(path.join(os.tmpdir(), "gdd-validator-"));

try {
  fs.mkdirSync(path.join(temp, "systems"));
  fs.writeFileSync(path.join(temp, "00-index-and-decisions.md"), "# Index\nSYS-CORE\n");
  fs.writeFileSync(path.join(temp, "04-system-index.md"), "# Systems\nSYS-CORE\n");
  fs.writeFileSync(path.join(temp, "systems", "SYS-CORE-core.md"), "# SYS-CORE\nACT-CORE CFG-CORE REQ-CORE AC-CORE\n");
  const valid = {
    schemaVersion: "1.0",
    project: { name: "test", baseline: "test", status: "draft" },
    documents: [
      { path: "00-index-and-decisions.md", kind: "index" },
      { path: "04-system-index.md", kind: "system-index" },
      { path: "systems/SYS-CORE-core.md", kind: "system", systemId: "SYS-CORE" }
    ],
    entities: [
      { id: "SYS-CORE", type: "system", definedIn: "systems/SYS-CORE-core.md", refs: [] },
      { id: "ACT-CORE", type: "action", systemId: "SYS-CORE", definedIn: "systems/SYS-CORE-core.md", refs: ["CFG-CORE"], acceptance: ["AC-CORE"] },
      { id: "CFG-CORE", type: "config", systemId: "SYS-CORE", definedIn: "systems/SYS-CORE-core.md", refs: [], consumers: ["ACT-CORE"] },
      { id: "REQ-CORE", type: "requirement", systemId: "SYS-CORE", definedIn: "systems/SYS-CORE-core.md", refs: ["ACT-CORE"], acceptance: ["AC-CORE"] },
      { id: "AC-CORE", type: "acceptance", systemId: "SYS-CORE", definedIn: "systems/SYS-CORE-core.md", refs: ["REQ-CORE"] }
    ]
  };
  fs.writeFileSync(path.join(temp, "document-set.json"), JSON.stringify(valid, null, 2));
  const pass = spawnSync(process.execPath, [validator, temp, "--json"], { encoding: "utf8" });
  assert.equal(pass.status, 0, pass.stderr || pass.stdout);
  assert.equal(JSON.parse(pass.stdout).ok, true);

  valid.entities.find((entity) => entity.id === "CFG-CORE").consumers = [];
  fs.writeFileSync(path.join(temp, "document-set.json"), JSON.stringify(valid, null, 2));
  const fail = spawnSync(process.execPath, [validator, temp, "--json"], { encoding: "utf8" });
  assert.equal(fail.status, 1);
  assert.ok(JSON.parse(fail.stdout).errors.some((item) => item.code === "CONFIG_WITHOUT_CONSUMER"));
  console.log("validate_document_set tests passed");
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}
