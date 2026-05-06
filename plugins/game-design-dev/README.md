# 游戏开发

Local Codex plugin for game design critique, game design document landing, and Unity or Godot prototype implementation planning.

This plugin bundles the `gamedesign` skill and uses it as the first step for game design, design critique, game design documents, core loop diagrams, system hierarchy diagrams, interaction-chain diagrams, and engine-specific prototype planning.

When users provide PDF or DOCX/DOC design documents, the plugin workflow now routes document reading through the shared `$pdf` and `$doc` skills before applying the bundled game-design knowledge base. User documents are treated as source briefs; bundled `references/` files remain the terminology, template, and evaluation standard.

## Local Installation

This plugin is installed as a home-local plugin:

```text
/Users/kakiasr/Documents/MyAgentSkills/plugins/game-design-dev
/Users/kakiasr/Documents/MyAgentSkills/.agents/plugins/marketplace.json
```

The marketplace entry points to:

```json
{
  "name": "game-design-dev",
    "source": {
      "source": "local",
      "path": "./Documents/MyAgentSkills/plugins/game-design-dev"
    }
}
```

## Cross-Project Use

Because the plugin lives under `/Users/kakiasr/Documents/MyAgentSkills/plugins`, it is available across different project workspaces on the same machine. Compatibility links may still point from `~/plugins/unity-game-design-dev` to this canonical directory while the new canonical plugin id is `game-design-dev`.

## Cross-Device Use

To use this plugin on another device:

1. Copy or clone this repository to `/Users/kakiasr/Documents/MyAgentSkills`.
2. Add the same plugin entry to `~/.agents/plugins/marketplace.json`.
3. Keep `.codex-plugin/plugin.json`, `skills/`, `scripts/`, and `assets/` together.

Recommended sync approach:

```bash
cd /Users/kakiasr/Documents/MyAgentSkills
git init
git add .
git commit -m "Update game development plugin"
```

Push that repository to a private or public Git remote, then clone it into `/Users/kakiasr/Documents/MyAgentSkills` on each device.

## Main Skill

The main skills are:

```text
skills/gamedesign/SKILL.md
skills/game-system-spec/SKILL.md
skills/unity-game-design-dev/SKILL.md
skills/godot-game-design-dev/SKILL.md
```

Use `gamedesign` first to structure and evaluate the game design, then use `game-system-spec` when a programmer-facing system spec is needed. Use `unity-game-design-dev` to translate the approved design into Unity scenes, prefabs, MonoBehaviours, ScriptableObject data assets, and editor-adjustable prototype deliverables. Use `godot-game-design-dev` to translate the approved design into Godot scenes, nodes, scripts, resources, signals, input actions, and exported tuning variables.

For knowledge-base lookup, use `skills/gamedesign/scripts/search_knowledge_base.py`. It refreshes stale `.txt` caches when a bundled PDF is newer and preserves page markers in search output.
