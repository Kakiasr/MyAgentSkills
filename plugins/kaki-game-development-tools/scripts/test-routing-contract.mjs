#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function read(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

const routing = read("references/skill-routing-and-handoff.md");
const workflow = read("skills/game-development-workflow/SKILL.md");
const analysis = read("skills/game-analysis/SKILL.md");
const document = read("skills/game-design-document/SKILL.md");
const documentAgent = read("skills/game-design-document/agents/openai.yaml");
const programmingRouter = read("skills/game-programming-development/SKILL.md");

const programmingSkills = [
  "game-software-architecture",
  "gameplay-programming",
  "unity-project-foundation",
  "unity-data-and-editor-tooling",
  "game-testing-and-validation",
];

const artSkills = [
  "game-art-direction",
  "game-character-and-prop-design",
  "game-environment-art-design",
  "game-ui-visual-design",
  "game-animation-design",
  "game-vfx-design",
  "game-2d-asset-production",
  "game-3d-asset-production",
  "game-rendering-technical-art",
  "game-art-pipeline",
  "game-graphics-performance",
];

for (const phrase of ["拆解一次", "完整拆解", "game-design-document", "document-set.json"]) {
  assert.ok(routing.includes(phrase), `routing contract missing: ${phrase}`);
}

assert.match(
  workflow,
  /完整游戏[^\n]*拆解[^\n]*game-design-document|拆解一次[^\n]*game-design-document/,
  "workflow must route whole-game teardown to the document-set entrypoint",
);
assert.match(
  analysis,
  /不得用一篇静态分析概览直接结束整个任务/,
  "analysis skill must not terminate a whole-game teardown after evidence gathering",
);

for (const deliverable of [
  "游戏体验与玩法拆解",
  "游戏循环",
  "系统文档",
  "需求与配置",
  "document-set.json",
]) {
  assert.ok(document.includes(deliverable), `document skill missing mandatory deliverable: ${deliverable}`);
}

assert.match(
  document,
  /聊天回复[^\n]*不能替代[^\n]*目录与文件/,
  "document skill must reject chat summaries as the default artifact",
);
assert.match(
  documentAgent,
  /整款游戏拆解总入口/,
  "agent metadata must advertise the whole-game teardown route",
);

for (const skill of programmingSkills) {
  const skillText = read(`skills/${skill}/SKILL.md`);
  const agentText = read(`skills/${skill}/agents/openai.yaml`);
  assert.match(skillText, new RegExp(`name: ${skill}`), `${skill} frontmatter name mismatch`);
  assert.ok(programmingRouter.includes(`\`${skill}\``), `programming router missing: ${skill}`);
  assert.ok(agentText.includes(`$${skill}`), `${skill} default prompt must name the skill`);
}

assert.match(
  programmingRouter,
  /兼容路由器|保留原调用ID/,
  "legacy programming skill must remain a compatibility router",
);

for (const skill of artSkills) {
  const skillText = read(`skills/${skill}/SKILL.md`);
  const agentText = read(`skills/${skill}/agents/openai.yaml`);
  assert.match(skillText, new RegExp(`name: ${skill}`), `${skill} frontmatter name mismatch`);
  assert.ok(routing.includes(`\`${skill}\``), `art routing contract missing: ${skill}`);
  assert.ok(agentText.includes(`$${skill}`), `${skill} default prompt must name the skill`);
}

for (const removed of ["game-art-design", "game-art-asset-creation", "game-technical-art"]) {
  assert.equal(fs.existsSync(path.join(root, "skills", removed)), false, `removed art skill still exists: ${removed}`);
  assert.equal(routing.includes(`\`${removed}\``), false, `routing contract still references removed art skill: ${removed}`);
  assert.equal(workflow.includes(`\`${removed}\``), false, `workflow still references removed art skill: ${removed}`);
}

console.log("routing contract tests passed");
