#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dependencies = JSON.parse(fs.readFileSync(path.join(root, "dependencies.json"), "utf8"));
const release = JSON.parse(fs.readFileSync(path.join(root, "scripts", "rea", "release.json"), "utf8"));
const requirements = fs.readFileSync(path.join(root, "requirements-dev.txt"), "utf8");

const node = dependencies.required.find((item) => item.id === "node");
const rea = dependencies.managed.find((item) => item.id === "rea-agents");
const pyyaml = dependencies.development.find((item) => item.id === "pyyaml");

assert.ok(node, "required Node.js dependency is missing");
assert.equal(node.version, release.node, "Node.js range must match the REA release contract");
assert.ok(rea, "managed rea-agents dependency is missing");
assert.equal(rea.version, release.version, "REA dependency version must match release.json");
assert.ok(pyyaml, "PyYAML development dependency is missing");
assert.match(requirements, /^PyYAML>=6\.0,<7\.0$/m, "requirements-dev.txt must contain the declared PyYAML range");

for (const section of ["required", "managed", "featureOptional", "development", "analysisProviders"]) {
  assert.ok(Array.isArray(dependencies[section]), `dependency section must be an array: ${section}`);
}

console.log("dependency manifest tests passed");
