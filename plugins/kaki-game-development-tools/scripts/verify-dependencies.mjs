#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "dependencies.json"), "utf8"));
const requireDevelopment = process.argv.includes("--dev");

function run(command, args) {
  const result = spawnSync(command, args, { encoding: "utf8", windowsHide: true });
  return {
    available: result.status === 0,
    status: result.status,
    value: (result.stdout || result.stderr || "").trim(),
  };
}

function firstAvailable(candidates, args) {
  for (const command of candidates) {
    const result = run(command, args);
    if (result.available) return { command, ...result };
  }
  return { command: null, available: false, status: null, value: "" };
}

const nodeMajor = Number(process.versions.node.split(".")[0]);
const nodeMinor = Number(process.versions.node.split(".")[1]);
const nodeSupported =
  (nodeMajor === 22 && nodeMinor >= 19) ||
  (nodeMajor === 24 && nodeMinor >= 11) ||
  nodeMajor >= 26;

const python = firstAvailable(process.platform === "win32" ? ["py", "python", "python3"] : ["python3", "python"], ["--version"]);
const pythonPrefix = python.command === "py" ? ["-3"] : [];
const yamlProbe = python.available
  ? run(python.command, [...pythonPrefix, "-c", "import importlib.util,sys; s=importlib.util.find_spec('yaml'); print('available' if s else 'missing'); sys.exit(0 if s else 1)"])
  : { available: false, status: null, value: "missing" };
const yaml = yamlProbe.available
  ? run(python.command, [...pythonPrefix, "-c", "import yaml; print(yaml.__version__)"])
  : yamlProbe;

const report = {
  manifestVersion: manifest.schemaVersion,
  required: {
    node: { available: true, supported: nodeSupported, version: process.versions.node },
  },
  development: {
    python: { available: python.available, command: python.command, version: python.value },
    pyyaml: { available: yaml.available, version: yaml.value },
  },
};

const ok = nodeSupported && (!requireDevelopment || (python.available && yaml.available));
console.log(JSON.stringify({ ok, mode: requireDevelopment ? "development" : "runtime", ...report }, null, 2));
process.exit(ok ? 0 : 1);
