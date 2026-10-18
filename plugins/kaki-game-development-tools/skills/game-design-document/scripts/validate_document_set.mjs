#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const rootArg = process.argv[2];
const jsonOutput = process.argv.includes("--json");
if (!rootArg) {
  console.error("Usage: node validate_document_set.mjs <document-set-directory> [--json]");
  process.exit(2);
}

const root = path.resolve(rootArg);
const errors = [];
const warnings = [];
const add = (list, code, message, details = {}) => list.push({ code, message, ...details });
const manifestPath = path.join(root, "document-set.json");

if (!fs.existsSync(manifestPath)) {
  add(errors, "MANIFEST_MISSING", "document-set.json does not exist", { path: manifestPath });
  finish();
}

let manifest;
try {
  manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
} catch (error) {
  add(errors, "MANIFEST_INVALID_JSON", error.message, { path: manifestPath });
  finish();
}

if (manifest.schemaVersion !== "1.0") add(errors, "SCHEMA_VERSION", "schemaVersion must be 1.0");
if (!Array.isArray(manifest.documents)) add(errors, "DOCUMENTS_TYPE", "documents must be an array");
if (!Array.isArray(manifest.entities)) add(errors, "ENTITIES_TYPE", "entities must be an array");
if (errors.length) finish();

const documents = new Map();
const systemDocs = new Map();
for (const doc of manifest.documents) {
  if (!doc || typeof doc.path !== "string" || typeof doc.kind !== "string") {
    add(errors, "DOCUMENT_INVALID", "Each document needs string path and kind");
    continue;
  }
  const normalized = doc.path.replaceAll("\\", "/");
  if (path.isAbsolute(doc.path) || normalized.split("/").includes("..")) {
    add(errors, "DOCUMENT_PATH_UNSAFE", `Document path must stay under the document set: ${doc.path}`);
    continue;
  }
  if (documents.has(normalized)) add(errors, "DOCUMENT_DUPLICATE", `Duplicate document path: ${normalized}`);
  documents.set(normalized, doc);
  const absolute = path.resolve(root, normalized);
  if (!absolute.startsWith(root + path.sep) && absolute !== root) add(errors, "DOCUMENT_PATH_ESCAPE", `Document escapes root: ${normalized}`);
  else if (!fs.existsSync(absolute)) add(errors, "DOCUMENT_MISSING", `Declared document does not exist: ${normalized}`);
  if (doc.kind === "system") {
    if (typeof doc.systemId !== "string" || !doc.systemId.startsWith("SYS-")) add(errors, "SYSTEM_ID_MISSING", `System document needs SYS-* systemId: ${normalized}`);
    if (!normalized.startsWith("systems/") || !normalized.endsWith(".md")) add(errors, "SYSTEM_PATH", `System document must be systems/*.md: ${normalized}`);
    if (doc.systemId && systemDocs.has(doc.systemId)) add(errors, "SYSTEM_DOCUMENT_DUPLICATE", `System ${doc.systemId} has multiple documents`);
    else if (doc.systemId) systemDocs.set(doc.systemId, normalized);
  }
}

for (const requiredKind of ["index", "system-index"]) {
  if (![...documents.values()].some((doc) => doc.kind === requiredKind)) add(errors, "REQUIRED_DOCUMENT_KIND", `Missing document kind: ${requiredKind}`);
}

const entities = new Map();
for (const entity of manifest.entities) {
  if (!entity || typeof entity.id !== "string" || typeof entity.type !== "string" || typeof entity.definedIn !== "string") {
    add(errors, "ENTITY_INVALID", "Each entity needs string id, type and definedIn");
    continue;
  }
  if (entities.has(entity.id)) add(errors, "ENTITY_DUPLICATE", `Duplicate entity id: ${entity.id}`);
  entities.set(entity.id, entity);
}

for (const entity of entities.values()) {
  const definedIn = entity.definedIn.replaceAll("\\", "/");
  if (!documents.has(definedIn)) add(errors, "ENTITY_DOCUMENT_UNKNOWN", `${entity.id} is defined in undeclared document ${definedIn}`);
  const refs = Array.isArray(entity.refs) ? entity.refs : [];
  for (const ref of refs) if (!entities.has(ref)) add(errors, "REFERENCE_UNRESOLVED", `${entity.id} references unknown ${ref}`);

  if (entity.systemId) {
    if (!systemDocs.has(entity.systemId)) add(errors, "ENTITY_SYSTEM_UNKNOWN", `${entity.id} belongs to unknown ${entity.systemId}`);
    else if (["system", "action", "config", "data", "state", "event", "requirement", "acceptance"].includes(entity.type) && definedIn !== systemDocs.get(entity.systemId)) {
      add(errors, "SYSTEM_OWNERSHIP", `${entity.id} must be defined in its system document ${systemDocs.get(entity.systemId)}`);
    }
  }

  if (entity.type === "requirement") {
    if (!Array.isArray(entity.acceptance) || entity.acceptance.length === 0) add(errors, "REQUIREMENT_WITHOUT_ACCEPTANCE", `${entity.id} has no acceptance IDs`);
    else for (const id of entity.acceptance) if (!entities.has(id) || entities.get(id).type !== "acceptance") add(errors, "ACCEPTANCE_UNRESOLVED", `${entity.id} acceptance is unknown or not acceptance: ${id}`);
  }
  if (entity.type === "config") {
    if (!Array.isArray(entity.consumers) || entity.consumers.length === 0) add(errors, "CONFIG_WITHOUT_CONSUMER", `${entity.id} has no consumers`);
    else for (const id of entity.consumers) if (!entities.has(id)) add(errors, "CONSUMER_UNRESOLVED", `${entity.id} consumer is unknown: ${id}`);
  }
  if (entity.type === "action" && (!Array.isArray(entity.acceptance) || entity.acceptance.length === 0)) add(warnings, "ACTION_WITHOUT_ACCEPTANCE", `${entity.id} has no direct acceptance coverage`);

  const absolute = path.resolve(root, definedIn);
  if (fs.existsSync(absolute) && absolute.endsWith(".md")) {
    const text = fs.readFileSync(absolute, "utf8");
    if (!text.includes(entity.id)) add(errors, "ENTITY_NOT_IN_DOCUMENT", `${entity.id} is not present in ${definedIn}`);
  }
}

for (const [systemId, docPath] of systemDocs) {
  const roots = [...entities.values()].filter((entity) => entity.type === "system" && entity.definedIn.replaceAll("\\", "/") === docPath);
  if (roots.length !== 1) add(errors, "SYSTEM_ROOT_COUNT", `${docPath} must define exactly one system entity; found ${roots.length}`);
  else if (roots[0].id !== systemId) add(errors, "SYSTEM_ROOT_MISMATCH", `${docPath} declares ${systemId} but defines ${roots[0].id}`);
}

finish();

function finish() {
  const report = { ok: errors.length === 0, errors, warnings };
  if (jsonOutput) console.log(JSON.stringify(report, null, 2));
  else {
    for (const item of errors) console.error(`ERROR ${item.code}: ${item.message}`);
    for (const item of warnings) console.warn(`WARN ${item.code}: ${item.message}`);
    console.log(`Validation ${report.ok ? "passed" : "failed"}: ${errors.length} error(s), ${warnings.length} warning(s)`);
  }
  process.exit(errors.length ? 1 : 0);
}
