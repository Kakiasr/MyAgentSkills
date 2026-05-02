# Unity Game Design Dev

Local Codex plugin for Unity game design critique, game design document landing, and Unity prototype implementation planning.

This plugin bundles the `gamedesign` skill and uses it as the first step for game design, design critique, game design documents, core loop diagrams, system hierarchy diagrams, interaction-chain diagrams, and Unity-first prototype planning.

When users provide PDF or DOCX/DOC design documents, the plugin workflow now routes document reading through the shared `$pdf` and `$doc` skills before applying the bundled game-design knowledge base. User documents are treated as source briefs; bundled `references/` files remain the terminology, template, and evaluation standard.

## Local Installation

This plugin is installed as a home-local plugin:

```text
~/plugins/unity-game-design-dev
~/.agents/plugins/marketplace.json
```

The marketplace entry points to:

```json
{
  "name": "unity-game-design-dev",
  "source": {
    "source": "local",
    "path": "./plugins/unity-game-design-dev"
  }
}
```

## Cross-Project Use

Because the plugin lives under `~/plugins`, it is available across different project workspaces on the same machine. It is not tied to the workspace where it was created.

## Cross-Device Use

To use this plugin on another device:

1. Copy or clone this directory to `~/plugins/unity-game-design-dev`.
2. Add the same plugin entry to `~/.agents/plugins/marketplace.json`.
3. Keep `.codex-plugin/plugin.json`, `skills/`, `scripts/`, and `assets/` together.

Recommended sync approach:

```bash
cd ~/plugins/unity-game-design-dev
git init
git add .
git commit -m "Create Unity game design development plugin"
```

Push that repository to a private or public Git remote, then clone it into `~/plugins/unity-game-design-dev` on each device.

## Main Skill

The main skills are:

```text
skills/gamedesign/SKILL.md
skills/unity-game-design-dev/SKILL.md
```

Use `gamedesign` first to structure and evaluate the game design, then use `unity-game-design-dev` to translate the approved design into Unity scenes, prefabs, MonoBehaviours, ScriptableObject data assets, and editor-adjustable prototype deliverables.

For knowledge-base lookup, use `skills/gamedesign/scripts/search_knowledge_base.py`. It refreshes stale `.txt` caches when a bundled PDF is newer and preserves page markers in search output.
