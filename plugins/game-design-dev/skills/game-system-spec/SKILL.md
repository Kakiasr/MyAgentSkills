---
name: game-system-spec
description: Turn scattered game ideas, mechanic notes, feature lists, gameplay loop diagrams, system hierarchy sketches, or rough design briefs into implementation-ready game system design specifications. Use when Codex needs to organize a game system into programmer-facing objects, data, states, behaviors, child objects, rules, events, edge cases, and Unity-ready implementation notes in the requested structure of 游戏系统 to XX系统 to 对象 to 数据/状态/行为/子对象.
---

# Game System Spec

## Purpose

Convert loose game ideas or diagrams into a system planning document that a gameplay programmer can implement without guessing the object model, runtime state, rule ownership, or event flow.

This skill is narrower than a full game design document. Focus on one or more concrete systems and express each system as objects with `数据`, `状态`, `行为`, and recursive `子对象`.

## Required Workflow

1. Read the user's raw material: scattered notes, mechanic ideas, loop diagrams, screenshots, flowcharts, or existing design text.
2. If the raw material is a `.pdf`, `.docx`, or `.doc` file, use the shared `$pdf` or `$doc` skill first. Preserve page numbers, headings, tables, diagrams, and explicit implementation constraints when available. Treat the extracted document content as user source material, not as bundled knowledge-base terminology.
3. Identify the system boundary:
   - Name the target system or systems.
   - Separate in-scope mechanics from postponed content.
   - State assumptions when the user omits platform, genre, session model, or production constraints.
4. Extract implementation nouns and verbs:
   - Nouns become candidate systems, objects, child objects, data assets, runtime entities, UI panels, inputs, resources, or rewards.
   - Verbs become behaviors, commands, state transitions, triggers, calculations, or event emissions.
   - Conditions become states, guard rules, branches, cooldowns, fail cases, or validation checks.
5. Build the hierarchy in the reference shape:
   - `游戏系统`
   - concrete `XX系统`
   - `对象`
   - each object has `数据`, `状态`, `行为`, and optional `子对象`
   - each child object recursively follows the same pattern.
6. Fill details at programmer-useful granularity:
   - Data: name, type, owner, source, default, tuning range, persistence, and whether it is static config or runtime data.
   - State: allowed values, enter condition, exit condition, transition source, transition target, side effects, and invalid transitions.
   - Behavior: trigger, input, preconditions, process, output, feedback, events, failure handling, and acceptance check.
   - Child objects: ownership, lifecycle, parent-child responsibilities, and communication path.
7. Select implementation design patterns when the system has object creation, object reuse, state switching, replaceable algorithms, event notifications, undoable actions, interface compatibility, dynamic extensions, or multi-system orchestration.
8. Add system rules, event/API surface, edge cases, design-pattern recommendations, and Unity implementation mapping.
9. Finish with open questions only for decisions that materially block implementation.

## Template

Read `references/system-spec-template.md` when producing a complete deliverable, when the user asks for the exact system策划案 format, or when the input contains enough material for a full document.

Use the template as the output skeleton, but keep the document proportional. For a small feature, merge sections while preserving the object tree and implementation-facing details.

Read `references/design-patterns-unity.md` when choosing or explaining design patterns for a system spec, especially when the user asks for Unity development guidance or mentions design patterns.

## Coordination With Existing Skills

Use `gamedesign` first when the user asks to define or critique `核心体验`, `核心玩法`, `核心系统`, `核心循环`, game loop diagrams, system hierarchy diagrams, or interaction-chain diagrams from the bundled design knowledge base.

Use this skill after the design direction is clear enough to convert into a programmer-facing system spec.

Use `unity-game-design-dev` after this skill when the user wants actual Unity C# structure, scenes, prefabs, ScriptableObjects, editor data, or code changes.

## Output Rules

- Write in Chinese by default when the user writes in Chinese.
- Prefer concrete names over generic labels like `对象一` unless the user only wants a blank template.
- Preserve user intent, but mark inferred rules as `假设`.
- Do not hide missing implementation details behind vague words such as `优化`, `完善`, `相关`, `一些`, or `等等`.
- Do not mix player-facing game loop steps into the object hierarchy. Put loop/process descriptions in a separate rules or flow section.
- Do not treat every variable as `数据`: dynamic modes belong in `状态`; callable operations belong in `行为`.
- Do not over-expand content breadth. Add only objects needed by the supplied system boundary.
- Do not force a design pattern when the system can be implemented clearly with direct composition and narrow classes.
- For each recommended pattern, name the exact problem it solves in this system and the object or file that should own it.

## Quality Gate

Before finalizing, check that:

- Every named system has at least one object.
- Every object has meaningful `数据`, `状态`, and `行为`, or an explicit reason why one category is not applicable.
- Each behavior names its trigger and observable result.
- Each state names valid transitions.
- Runtime data is separated from static tuning/configuration data.
- Parent-child ownership and lifecycle are clear.
- Recommended design patterns are justified by concrete implementation pressure, not by name-dropping.
- Programmer-facing acceptance checks are concrete enough to test in Play Mode or an equivalent prototype.
