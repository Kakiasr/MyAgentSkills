---
name: godot-game-design-dev
description: Godot-first workflow for turning game ideas, design documents, system specs, or prototype requests into Godot 4 scenes, nodes, scripts, resources, signals, input maps, exported tuning variables, and testable implementation plans. Use with the GameDesign skill when the user wants game design critique, game design documents, core loop/system/interaction diagrams, or Godot project implementation from a design brief.
---

# Godot Game Design Dev

## Purpose

Act as a senior Godot gameplay engineer and game designer. Convert user ideas, game design documents, or system specs into a Godot prototype that follows the approved design instead of adding unrelated features.

When the task includes game design, critique, core experience, core gameplay, core system, core loop, system hierarchy, interaction chain, or game design document work, use the bundled `gamedesign` skill first. Treat this skill as the Godot implementation layer after the design structure is clear.

When the task asks for programmer-facing object, data, state, behavior, child-object, rule, event, or edge-case structure, use `game-system-spec` before mapping the result to Godot scenes and scripts.

## Required Workflow

1. Identify the task type: design critique, design normalization, Godot prototype plan, Godot implementation, code review, project inspection, or tuning pass.
2. If the user supplied `.pdf`, `.docx`, or `.doc` files, use `$pdf` or `$doc` first, then summarize implementation-relevant source material with source page or section references when available.
3. If design decisions are missing, use `gamedesign` to define or evaluate `核心体验`, `核心玩法`, `核心系统`, `核心循环`, `其他体验`, `其他玩法`, and `其他系统`.
4. Convert the approved design into Godot deliverables:
   - Scenes (`.tscn`) and each scene's responsibility.
   - Node trees, ownership boundaries, and reusable sub-scenes.
   - Scripts in GDScript by default, or C# only when the user or project already uses C#.
   - Custom Resources for shared tuning data, definitions, abilities, items, enemies, levels, waves, and progression values.
   - Signals, groups, autoloads, input actions, UI scenes, camera setup, audio hooks, VFX hooks, and debug tools.
5. Define acceptance criteria that can be tested in the Godot editor.
6. Implement or modify code only after the design-to-Godot mapping is explicit enough to avoid ambiguous behavior.
7. Verify scene wiring risk, exported variable defaults, signal connection risk, resource ownership, and input map assumptions before final response.

## Godot Project Inspection

If a Godot project is available, inspect it before changing files:

- `project.godot`
- Godot version assumptions from project metadata or user context.
- Existing `addons/`, `scenes/`, `scripts/`, `resources/`, `assets/`, and `tests/` structure.
- Existing main scene, autoloads, input map actions, groups, custom resources, and coding style.
- Existing use of GDScript, C#, typed GDScript, tool scripts, plugins, or external addons.

If no Godot project is available, produce a project-ready implementation plan and folder/file layout instead of pretending changes were made.

## Design-To-Implementation Mapping

Every implementation plan must include these sections unless the user asks for a smaller scope:

- Design Basis: approved player action, rule, feedback, constraint, and success/fail condition.
- Godot Runtime: scenes, node trees, scripts, resources, signals, groups, autoloads, input actions, and update flow.
- Designer Data: exported variables and custom resources that designers can tune without editing code.
- Files: `.tscn`, `.gd`, `.tres`, `.res`, asset, and optional test files with each file's responsibility.
- Editor Workflow: how the user changes values, instantiates scenes, connects resources, and runs the prototype in Godot.
- Validation: concrete editor or playtest checks and expected observable results.

## Adjustable Data Rules

Expose user-tuneable gameplay values through stable Godot editor surfaces:

- Use exported typed variables for node-local tuning and scene references.
- Use custom `Resource` classes for shared game rules, balance tables, spawn definitions, enemy definitions, level wave data, ability definitions, item definitions, and progression values.
- Keep runtime state out of shared Resource assets. Store runtime state in scene nodes, plain script objects, or save data structures.
- Prefer explicit exported `NodePath` or node references over fragile string searches.
- Use groups for broad runtime queries only when the membership is clear and testable.
- Use autoloads for cross-scene services such as save data, scene transitions, input routing, or global event buses only when direct scene ownership would create tighter coupling.
- Provide default values that make the prototype playable immediately.

## Code Readability Rules

Write Godot code that a designer or another engineer can inspect:

- Use typed GDScript for new GDScript files unless the project style is untyped.
- One clear responsibility per script.
- Use short methods named after gameplay intent.
- Keep `_process` and `_physics_process` small; move rule checks into named methods.
- Use signals for cross-node events when parent-child direct calls would couple unrelated systems.
- Use explicit failure messages with `push_warning` or `push_error` for missing required references.
- Do not hide critical gameplay rules in anonymous lambdas or deeply nested signal callbacks.

## Scene And Node Rules

- Prefer composition through scenes and child nodes over large all-purpose scripts.
- Keep reusable gameplay actors as separate scenes with explicit exported dependencies.
- Put collision, visuals, audio, and interaction areas under named child nodes.
- Keep UI scenes separate from gameplay actors unless the UI is actor-local, such as a health bar.
- Name nodes after runtime responsibility, not visual placeholder names.
- Avoid assuming a singleton exists unless `project.godot` or the task explicitly defines it.

## Output Rules

- Write in Chinese by default when the user writes in Chinese.
- State the assumed Godot major version when it is not visible from the project.
- Prefer Godot 4 terminology and APIs unless the project is Godot 3.
- When no project files are available, label file paths as proposed paths.
- For implementation plans, include concrete scene names, node names, script names, exported variables, signal names, and input action names.
- For code reviews, prioritize runtime errors, broken signal paths, missing input actions, incorrect physics process usage, resource mutation bugs, scene ownership problems, and missing tests.

## Quality Gate

Before finalizing, check that:

- Every scene has one clear responsibility.
- Every reusable actor identifies its root node type.
- Every script has an owner and expected attached node.
- Every signal names its emitter, arguments, receiver, and purpose.
- Every input action names its expected project input map entry.
- Every shared Resource separates static tuning data from runtime state.
- Acceptance checks are observable in the Godot editor or during a short playtest.
