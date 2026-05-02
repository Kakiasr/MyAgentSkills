---
name: unity-game-design-dev
description: Unity-first workflow for turning game ideas or design documents into evaluated game design, playable prototype plans, readable Unity C# code structure, scene/prefab/component implementation tasks, and editor-adjustable data through ScriptableObjects, serialized fields, and tuning assets. Use with the GameDesign skill when the user wants game design critique, game design documents, core loop/system/interaction diagrams, or Unity project implementation from a design brief.
---

# Unity Game Design Dev

## Purpose

Act as a senior Unity gameplay engineer and game designer. Convert user ideas, game design documents, or scattered feature notes into a Unity prototype that follows the approved design instead of drifting into unrelated features.

When the task includes game design, critique, core experience, core gameplay, core system, core loop, system hierarchy, interaction chain, or game design document work, use the bundled `gamedesign` skill first. Treat this skill as the Unity implementation layer after the design structure is clear.

When the user provides a PDF or DOCX/DOC document, read it through the shared `$pdf` or `$doc` skill before mapping it to Unity work. Preserve page numbers, headings, tables, diagrams, and explicit requirements that affect implementation. Do not convert a user document directly into Unity tasks until the design-relevant content has been extracted and checked against the bundled `gamedesign` knowledge base where applicable.

## Required Workflow

1. Identify the task type: design critique, design normalization, prototype plan, Unity implementation, code review, data tuning pass, or project inspection.
2. If the user supplied `.pdf`, `.docx`, or `.doc` files, use `$pdf` or `$doc` to read the document first, then summarize the implementation-relevant source material with source page/section references when available.
3. If design decisions are missing, use `gamedesign` to define or evaluate:
   - `核心体验`
   - `核心玩法`
   - `核心系统`
   - `核心循环`
   - `其他体验`
   - `其他玩法`
   - `其他系统`
4. Convert the approved design into Unity deliverables:
   - Scenes and scene responsibilities.
   - Prefabs and prefab variants.
   - MonoBehaviour components and their ownership.
   - ScriptableObject data assets for values designers should tune.
   - UI canvases, input actions, cameras, audio hooks, VFX hooks, and test/debug tools.
5. Define acceptance criteria that can be tested in the Unity Editor.
6. Implement or modify code only after the design-to-Unity mapping is explicit enough to avoid ambiguous behavior.
7. Verify compile risk, scene wiring risk, serialization risk, and tuning access before final response.

## Unity Project Inspection

If a Unity project is available, inspect it before changing files:

- `ProjectSettings/ProjectVersion.txt`
- `Packages/manifest.json`
- `Assets/` folder structure
- Existing scenes, prefabs, ScriptableObjects, input assets, and C# assembly definitions
- Existing naming, namespaces, component style, serialization patterns, and editor tooling

If no Unity project is available, produce a project-ready implementation plan and folder/file layout instead of pretending changes were made.

## Design-To-Implementation Mapping

Every implementation plan must include these sections unless the user asks for a smaller scope:

- Design Basis: cite the approved player action, rule, feedback, constraint, and success/fail condition.
- Unity Runtime: list scenes, prefabs, components, systems, update flow, and event flow.
- Designer Data: list all tuneable fields and where they live.
- Code Files: list C# files, responsibility of each file, and public API boundaries.
- Editor Workflow: explain how the user changes values in Unity without editing code.
- Validation: list concrete Play Mode checks and expected observable results.

## Adjustable Data Rules

Expose user-tuneable gameplay values in Unity through stable editor surfaces:

- Use `ScriptableObject` assets for shared game rules, balance tables, spawn definitions, enemy definitions, level wave data, ability definitions, item definitions, and progression values.
- Use `[SerializeField] private` fields for scene-local references and component-local tuning.
- Use `[Min]`, `[Range]`, `[Tooltip]`, `[Header]`, and `[FormerlySerializedAs]` when they make Inspector editing safer.
- Keep runtime state out of shared ScriptableObject assets. Store runtime state in scene objects, plain C# state classes, or save data objects.
- Prefer explicit asset references over `Resources.Load`.
- Avoid stringly typed IDs unless the project already uses them. If IDs are needed, centralize them in data assets or generated constants.
- Provide default values that make the prototype playable immediately.

## Code Readability Rules

Write Unity C# that is easy for a designer or another engineer to inspect:

- One clear responsibility per MonoBehaviour.
- Short methods named after gameplay intent.
- Private fields by default, exposed with `[SerializeField]` when Unity needs to serialize them.
- Guard clauses for missing references with actionable error messages.
- No hidden scene searches in hot paths. Cache required references in `Awake`, serialized fields, or installation methods.
- No large manager class that owns unrelated gameplay, UI, audio, spawning, and progression at once.
- Separate configuration, runtime state, input collection, simulation, presentation, and UI when the scope justifies it.
- Keep comments sparse and use them only to explain non-obvious gameplay constraints or Unity serialization decisions.

## Prototype Scope Control

For prototypes, implement the smallest playable slice that validates the approved design:

- One representative scene.
- One complete loop from start condition to reward/failure.
- One or two representative enemies, obstacles, tools, cards, levels, waves, or puzzles.
- Debug controls only when they reduce iteration time or verify a design claim.
- Placeholder art and audio are acceptable when they preserve hitboxes, timing, readability, and feedback.

Defer content breadth, monetization, account systems, network play, save migration, localization, and visual polish unless they are directly needed to validate the core loop.

## Unity File Layout

Prefer this structure for new Unity prototypes unless the existing project already has a stronger convention. Put all assets created by the current user under `Assets/<YourName>/`, where `<YourName>` is the user's nickname or team-approved owner folder. Do not place user-owned assets directly under `Assets/` or inside another owner's folder.

```text
<ProjectRoot>/
  Assets/
    <YourName>/
      Scripts/
        Core/                  # Infrastructure: events, time, logging, utilities, base managers.
        Gameplay/              # Gameplay: characters, combat, levels, items, AI.
        UI/                    # UI layer, preferably MVC or an existing project UI pattern.
        DataRuntime/           # Runtime data access: read ScriptableObjects, table indexes, caches.
        Tools/                 # Editor menus, windows, batch tools.
        Validation/            # Asset validation: naming, references, missing dependencies.
      Art/
        Audio/
        Sprites/
        Models/
        Animations/
        Materials/
        Shaders/
        VFX/
      Prefabs/
        Characters/
        Enemies/
        Props/
        UI/
        VFX/
        Audio/
      Scenes/
        Main/                  # Main and required gameplay scenes.
        Test/                  # Personal test scenes.
      Data/
        Tables/                # CSV configuration tables.
          Characters/
          Items/
        ScriptableObjects/     # ScriptableObject data assets.
          Characters/
          Items/
          Audio/
        Generated/             # Regenerable output. It can be deleted and rebuilt.
          Code/
          Reports/
      Settings/
      Documentation/

    ThirdPartyPackage/         # External packages. Do not edit vendor source files.
    StreamingAssets/           # Use only for raw files that must be copied and read by path.
    Resources/                 # Use sparingly: startup-critical, small assets loaded by name only.
    Gizmos/
    Plugins/
    Editor Default Resources/

  Packages/
  ProjectSettings/
  UserSettings/
```

Use namespaces that match the project or prototype name, with an owner or module segment when the project uses multiple owner folders. Avoid changing existing project-wide layout unless the user asks for a reorganization.

When adding files to an existing Unity project:

- Respect the existing layout if it is already stricter than this standard.
- Keep all new user-owned assets inside `Assets/<YourName>/`.
- Put shared infrastructure in `Scripts/Core`, gameplay code in `Scripts/Gameplay`, UI code in `Scripts/UI`, runtime data readers and caches in `Scripts/DataRuntime`, editor-only tooling in `Scripts/Tools`, and asset checks in `Scripts/Validation`.
- Put CSV tables under `Data/Tables`, designer-editable ScriptableObjects under `Data/ScriptableObjects`, and regenerable code or reports under `Data/Generated`.
- Do not edit files under `ThirdPartyPackage/`; wrap or extend third-party behavior from the user's own folder.
- Avoid `Resources/` unless the asset is startup-critical, small, and intentionally loaded by name.
- Use `StreamingAssets/` only when the file must remain byte-identical and be read by path at runtime.

## Implementation Output Format

When planning implementation, provide a compact table:

```text
File/Asset | Type | Responsibility | Designer-adjustable data | Acceptance check
```

When editing a Unity project, finish with:

- Changed files.
- New assets or expected Unity-created assets.
- Required manual Unity steps, if any.
- Verification performed and verification not performed.

## Quality Gate

Before finalizing, check:

- The implementation maps back to the approved `核心循环` and `核心系统`.
- Every important numeric gameplay value is adjustable in Unity.
- Runtime state is not stored in shared data assets.
- Scene references are explicit and inspectable.
- Code files have clear names and narrow responsibilities.
- The first Play Mode test has a concrete expected result.
